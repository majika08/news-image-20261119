// entry.png verifier and publisher for the news-image-20261119 entry.
//
// The artwork itself is produced ahead of time by the Python scripts under
// tools/; this program is the gatekeeper that runs at submission time. It
// loads the PNG sitting next to this file, proves the file is a sound PNG
// inside the bounty's limits (no more than 1024x1024 pixels, no more than
// 1 MiB on disk), hashes it, and only then publishes the exact same bytes
// to the output directory as entry.png. A one-line JSON manifest of what
// was published goes to stdout. Any validation failure aborts the run with
// a non-zero exit code and nothing is published.
//
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { createHash } from 'node:crypto';
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const MAX_DIMENSION = 1024;
const MAX_BYTES = 1_048_576;

// The eight magic bytes every PNG stream opens with.
const PNG_SIGNATURE = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];

// An IEND chunk is always the last 12 bytes of a complete PNG: a zero
// length field, the type bytes "IEND", and its fixed CRC.
const IEND_TRAILER = [
  0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4e, 0x44, 0xae, 0x42, 0x60, 0x82,
];

function reject(reason) {
  console.error(`entry.png rejected: ${reason}`);
  process.exit(1);
}

function hasPngSignature(bytes) {
  if (bytes.length < PNG_SIGNATURE.length) return false;
  return PNG_SIGNATURE.every((value, index) => bytes[index] === value);
}

// The IHDR chunk must come first: bytes 8..11 hold its data length (always
// 13), bytes 12..15 its type, and the width and height follow as big-endian
// uint32 values at offsets 16 and 20.
function readIhdrDimensions(bytes) {
  if (bytes.length < 24) reject('file too short to contain an IHDR chunk');
  if (bytes.readUInt32BE(8) !== 13 || bytes.toString('ascii', 12, 16) !== 'IHDR') {
    reject('first chunk is not a 13-byte IHDR');
  }
  return { width: bytes.readUInt32BE(16), height: bytes.readUInt32BE(20) };
}

function endsWithIend(bytes) {
  if (bytes.length < IEND_TRAILER.length) return false;
  const tail = bytes.subarray(bytes.length - IEND_TRAILER.length);
  return IEND_TRAILER.every((value, index) => tail[index] === value);
}

// Walk the chunk list that follows the signature. Each chunk is a 4-byte
// big-endian length, a 4-byte type, `length` data bytes and a 4-byte CRC.
// The walk must land exactly on the end of the buffer, and the final chunk
// must be IEND; anything else means the stream is malformed or truncated.
// Returns the chunk types in order of appearance.
function walkChunkTypes(bytes) {
  const types = [];
  let offset = PNG_SIGNATURE.length;
  while (offset < bytes.length) {
    if (offset + 8 > bytes.length) reject('chunk header runs past the end of the file');
    const length = bytes.readUInt32BE(offset);
    const type = bytes.toString('ascii', offset + 4, offset + 8);
    const next = offset + 8 + length + 4;
    if (next > bytes.length) reject(`chunk ${type} overruns the end of the file`);
    types.push(type);
    offset = next;
    if (type === 'IEND') break;
  }
  if (offset !== bytes.length) reject('trailing garbage after the IEND chunk');
  if (types[types.length - 1] !== 'IEND') reject('chunk walk never reached an IEND chunk');
  return types;
}

const sourcePath = new URL('./entry.png', import.meta.url);
const png = readFileSync(sourcePath);

if (png.length > MAX_BYTES) {
  reject(`file is ${png.length} bytes, over the ${MAX_BYTES}-byte limit`);
}
if (!hasPngSignature(png)) {
  reject('missing the PNG signature');
}

const { width, height } = readIhdrDimensions(png);
if (width < 1 || height < 1) {
  reject(`nonsensical dimensions ${width}x${height}`);
}
if (width > MAX_DIMENSION || height > MAX_DIMENSION) {
  reject(`dimensions ${width}x${height} exceed ${MAX_DIMENSION}x${MAX_DIMENSION}`);
}
if (!endsWithIend(png)) {
  reject('no IEND chunk at the end of the file (truncated PNG?)');
}
const chunkTypes = walkChunkTypes(png);

const sha256 = createHash('sha256').update(png).digest('hex');

const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outputDir, { recursive: true });
const outputPath = join(outputDir, 'entry.png');
writeFileSync(outputPath, png);

// Prove the published copy is the very same bytes that were validated:
// re-read what landed on disk and compare digests before declaring success.
const published = readFileSync(outputPath);
const copySha256 = createHash('sha256').update(published).digest('hex');
if (copySha256 !== sha256) {
  reject('published copy does not match the validated source bytes');
}

console.log(
  JSON.stringify({
    file: 'entry.png',
    width,
    height,
    bytes: png.length,
    chunks: chunkTypes.length,
    sha256,
    output: outputPath,
    copyVerified: true,
    ok: true,
  }),
);
