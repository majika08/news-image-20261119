"""Shared drawing helpers for the 2026-11-19 news-image candidates.

Everything is drawn programmatically with PIL at 2x supersampling and
downscaled to 1024x1024, so text stays crisp. No AI-generated imagery.
"""
from PIL import Image, ImageDraw, ImageFont

SS = 2  # supersampling factor
W = 1024

NOTO = "/usr/share/fonts/truetype/noto/"
LIB = "/usr/share/fonts/truetype/liberation/"

FONTS = {
    "sans": NOTO + "NotoSans-Regular.ttf",
    "sans_b": NOTO + "NotoSans-Bold.ttf",
    "sans_xb": NOTO + "NotoSans-ExtraBold.ttf",
    "sans_blk": NOTO + "NotoSans-Black.ttf",
    "disp_blk": NOTO + "NotoSansDisplay-Black.ttf",
    "disp_xb": NOTO + "NotoSansDisplay-ExtraBold.ttf",
    "disp_b": NOTO + "NotoSansDisplay-Bold.ttf",
    "serif": NOTO + "NotoSerif-Regular.ttf",
    "serif_b": NOTO + "NotoSerif-Bold.ttf",
    "serif_blk": NOTO + "NotoSerifDisplay-Black.ttf",
    "serif_xb": NOTO + "NotoSerifDisplay-ExtraBold.ttf",
    "lib_sans": LIB + "LiberationSans-Regular.ttf",
    "lib_sans_b": LIB + "LiberationSans-Bold.ttf",
    "lib_serif": LIB + "LiberationSerif-Regular.ttf",
    "lib_serif_b": LIB + "LiberationSerif-Bold.ttf",
}

_cache = {}


def font(kind, size):
    """size is in final (1024-space) pixels."""
    key = (kind, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(FONTS[kind], int(size * SS))
    return _cache[key]


class C:
    """Canvas in 1024-space coordinates, rendered at 2x."""

    def __init__(self, bg):
        self.img = Image.new("RGB", (W * SS, W * SS), bg)
        self.d = ImageDraw.Draw(self.img, "RGBA")

    def s(self, v):
        return v * SS

    def rect(self, x, y, w, h, fill=None, outline=None, ow=1):
        self.d.rectangle([self.s(x), self.s(y), self.s(x + w), self.s(y + h)],
                         fill=fill, outline=outline, width=max(1, int(ow * SS)))

    def rrect(self, x, y, w, h, r, fill=None, outline=None, ow=1):
        self.d.rounded_rectangle([self.s(x), self.s(y), self.s(x + w), self.s(y + h)],
                                 radius=self.s(r), fill=fill, outline=outline,
                                 width=max(1, int(ow * SS)))

    def line(self, pts, fill, wdt=1):
        self.d.line([(self.s(a), self.s(b)) for a, b in pts], fill=fill,
                    width=max(1, int(wdt * SS)), joint="curve")

    def poly(self, pts, fill=None, outline=None, ow=1):
        p = [(self.s(a), self.s(b)) for a, b in pts]
        self.d.polygon(p, fill=fill, outline=outline)
        if outline and ow > 1:
            self.d.line(p + [p[0]], fill=outline, width=int(ow * SS), joint="curve")

    def ellipse(self, x, y, w, h, fill=None, outline=None, ow=1):
        self.d.ellipse([self.s(x), self.s(y), self.s(x + w), self.s(y + h)],
                       fill=fill, outline=outline, width=max(1, int(ow * SS)))

    def arc(self, x, y, w, h, a0, a1, fill, wdt=2):
        self.d.arc([self.s(x), self.s(y), self.s(x + w), self.s(y + h)],
                   a0, a1, fill=fill, width=max(1, int(wdt * SS)))

    def text_w(self, txt, kind, size):
        f = font(kind, size)
        return self.d.textlength(txt, font=f) / SS

    def text(self, x, y, txt, kind, size, fill, anchor="la", spacing=4):
        self.d.text((self.s(x), self.s(y)), txt, font=font(kind, size),
                    fill=fill, anchor=anchor, spacing=self.s(spacing))

    def fit_size(self, txt, kind, size, max_w):
        """Shrink font size until txt fits max_w (1024-space)."""
        while size > 8 and self.text_w(txt, kind, size) > max_w:
            size -= 1
        return size

    def text_fit(self, x, y, txt, kind, size, max_w, fill, anchor="la"):
        size = self.fit_size(txt, kind, size, max_w)
        self.text(x, y, txt, kind, size, fill, anchor=anchor)
        return size

    def wrap(self, txt, kind, size, max_w):
        words, lines, cur = txt.split(), [], ""
        for wd in words:
            t = (cur + " " + wd).strip()
            if self.text_w(t, kind, size) <= max_w or not cur:
                cur = t
            else:
                lines.append(cur)
                cur = wd
        if cur:
            lines.append(cur)
        return lines

    def para(self, x, y, txt, kind, size, max_w, fill, leading=1.28, align="left"):
        lines = self.wrap(txt, kind, size, max_w)
        for ln in lines:
            if align == "center":
                self.text(x + max_w / 2, y, ln, kind, size, fill, anchor="ma")
            elif align == "right":
                self.text(x + max_w, y, ln, kind, size, fill, anchor="ra")
            else:
                self.text(x, y, ln, kind, size, fill)
            y += size * leading
        return y

    def finish(self, path):
        out = self.img.resize((W, W), Image.LANCZOS)
        out.save(path, "PNG", optimize=True)
        return path


# ---------------------------------------------------------------- flags
def _clip_flag(c, x, y, w, h):
    mask = Image.new("L", (int(w * SS), int(h * SS)), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([0, 0, int(w * SS), int(h * SS)], radius=int(6 * SS), fill=255)
    return mask


def paste_flag(c, draw_fn, x, y, w, h):
    layer = Image.new("RGB", (int(w * SS), int(h * SS)), (255, 255, 255))
    ld = ImageDraw.Draw(layer)
    draw_fn(ld, w * SS, h * SS)
    mask = _clip_flag(c, x, y, w, h)
    c.img.paste(layer, (int(x * SS), int(y * SS)), mask)
    c.d = ImageDraw.Draw(c.img, "RGBA")
    c.rrect(x, y, w, h, 6, outline=(0, 0, 0, 90), ow=1)


def flag_us(d, w, h):
    sh = h / 7
    for i in range(7):
        d.rectangle([0, i * 2 * sh if i else 0, w, (2 * i + 1) * sh], fill=(178, 34, 52))
    d.rectangle([0, 0, w * 0.45, sh * 4], fill=(60, 59, 110))
    r = h * 0.045
    for row in range(4):
        for col in range(5):
            cx = w * 0.05 + col * w * 0.09
            cy = sh * 0.5 + row * sh
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255))


def flag_cn(d, w, h):
    d.rectangle([0, 0, w, h], fill=(222, 41, 16))

    def star(cx, cy, r, rot=-90):
        import math
        pts = []
        for i in range(10):
            rr = r if i % 2 == 0 else r * 0.42
            a = math.radians(rot + i * 36)
            pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
        d.polygon(pts, fill=(255, 222, 0))

    star(w * 0.17, h * 0.28, h * 0.17)
    for i, (sx, sy) in enumerate([(0.36, 0.12), (0.40, 0.30), (0.40, 0.48), (0.36, 0.64)]):
        star(w * sx, h * sy, h * 0.055)


def flag_ru(d, w, h):
    d.rectangle([0, 0, w, h / 3], fill=(245, 245, 245))
    d.rectangle([0, h / 3, w, 2 * h / 3], fill=(0, 57, 166))
    d.rectangle([0, 2 * h / 3, w, h], fill=(213, 0, 50))


def flag_ir(d, w, h):
    d.rectangle([0, 0, w, h / 3], fill=(35, 159, 64))
    d.rectangle([0, h / 3, w, 2 * h / 3], fill=(255, 255, 255))
    d.rectangle([0, 2 * h / 3, w, h], fill=(218, 0, 0))
    d.ellipse([w * 0.44, h * 0.40, w * 0.56, h * 0.60], outline=(218, 0, 0), width=max(2, int(h * 0.03)))


def flag_il(d, w, h):
    d.rectangle([0, 0, w, h], fill=(255, 255, 255))
    d.rectangle([0, h * 0.14, w, h * 0.30], fill=(0, 56, 184))
    d.rectangle([0, h * 0.70, w, h * 0.86], fill=(0, 56, 184))
    import math
    cx, cy, r = w / 2, h / 2, h * 0.17
    for rot in (90, 270):
        pts = []
        for i in range(3):
            a = math.radians(-rot + i * 120)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        d.polygon(pts, outline=(0, 56, 184))


def flag_et(d, w, h):
    d.rectangle([0, 0, w, h / 3], fill=(7, 137, 48))
    d.rectangle([0, h / 3, w, 2 * h / 3], fill=(252, 221, 9))
    d.rectangle([0, 2 * h / 3, w, h], fill=(218, 18, 26))
    d.ellipse([w * 0.40, h * 0.28, w * 0.60, h * 0.72], fill=(15, 71, 175))


def flag_er(d, w, h):
    d.polygon([(0, 0), (w, h / 2), (0, h)], fill=(67, 158, 42))
    d.polygon([(0, 0), (w, h / 2), (w, 0)], fill=(227, 41, 46))
    d.polygon([(0, h), (w, h / 2), (w, h)], fill=(58, 117, 196))
    d.ellipse([w * 0.10, h * 0.36, w * 0.30, h * 0.64], fill=(255, 210, 0))


def flag_jp(d, w, h):
    d.rectangle([0, 0, w, h], fill=(255, 255, 255))
    d.ellipse([w * 0.36, h * 0.22, w * 0.64, h * 0.78], fill=(188, 0, 45))


def flag_mm(d, w, h):
    d.rectangle([0, 0, w, h / 3], fill=(254, 203, 0))
    d.rectangle([0, h / 3, w, 2 * h / 3], fill=(52, 178, 51))
    d.rectangle([0, 2 * h / 3, w, h], fill=(234, 40, 57))
    import math
    cx, cy, r = w / 2, h / 2, h * 0.20
    pts = []
    for i in range(10):
        rr = r if i % 2 == 0 else r * 0.45
        a = math.radians(-90 + i * 36)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=(255, 255, 255))


FLAGS = {"us": flag_us, "cn": flag_cn, "ru": flag_ru, "ir": flag_ir,
         "il": flag_il, "et": flag_et, "er": flag_er, "jp": flag_jp, "mm": flag_mm}


def flag(c, name, x, y, w, h):
    paste_flag(c, FLAGS[name], x, y, w, h)


# ---------------------------------------------------------------- icons
def icon(c, name, x, y, size, col, col2=None):
    """Simple flat pictograms drawn inside a size x size box at (x, y)."""
    d = c.d
    S = SS
    cx, cy = x + size / 2, y + size / 2
    if name == "missile":
        c.rrect(x + size * .20, y + size * .38, size * .50, size * .24, size * .10, fill=col)
        c.poly([(x + size * .70, y + size * .34), (x + size * .96, y + size * .50),
                (x + size * .70, y + size * .66)], fill=col)
        c.poly([(x + size * .24, y + size * .38), (x + size * .40, y + size * .38),
                (x + size * .30, y + size * .18)], fill=col)
        c.poly([(x + size * .24, y + size * .62), (x + size * .40, y + size * .62),
                (x + size * .30, y + size * .82)], fill=col)
        c.poly([(x + size * .20, y + size * .42), (x + size * .04, y + size * .50),
                (x + size * .20, y + size * .58)], fill=col2 or (240, 140, 40))
    elif name == "ship":
        c.poly([(x + size * .05, y + size * .62), (x + size * .95, y + size * .62),
                (x + size * .85, y + size * .85), (x + size * .18, y + size * .85)], fill=col)
        c.rect(x + size * .38, y + size * .42, size * .24, size * .20, fill=col)
        c.rect(x + size * .62, y + size * .50, size * .20, size * .12, fill=col)
        c.line([(x + size * .02, y + size * .95), (x + size * .98, y + size * .95)], col2 or col, 3)
    elif name == "flame":
        c.poly([(cx, y + size * .05), (x + size * .72, y + size * .45),
                (x + size * .78, y + size * .68), (x + size * .66, y + size * .92),
                (x + size * .34, y + size * .92), (x + size * .22, y + size * .68),
                (x + size * .30, y + size * .42)], fill=col)
        c.poly([(cx, y + size * .45), (x + size * .60, y + size * .68),
                (x + size * .56, y + size * .90), (x + size * .44, y + size * .90),
                (x + size * .40, y + size * .68)], fill=col2 or (255, 205, 60))
    elif name == "burst":
        import math
        pts = []
        for i in range(16):
            rr = size * (0.48 if i % 2 == 0 else 0.24)
            a = math.radians(i * 22.5)
            pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
        c.poly(pts, fill=col)
        c.ellipse(cx - size * .12, cy - size * .12, size * .24, size * .24, fill=col2 or (255, 220, 90))
    elif name == "dome":  # capitol
        c.arc(x + size * .28, y + size * .02, size * .44, size * .44, 180, 360, col, 5)
        c.poly([(x + size * .28, y + size * .24), (x + size * .72, y + size * .24),
                (x + size * .66, y + size * .34), (x + size * .34, y + size * .34)], fill=col)
        c.rect(x + size * .46, y + size * .0, size * .08, size * .10, fill=col)
        for i in range(4):
            c.rect(x + size * (.22 + i * .15), y + size * .40, size * .07, size * .36, fill=col)
        c.rect(x + size * .12, y + size * .78, size * .76, size * .09, fill=col)
        c.rect(x + size * .08, y + size * .90, size * .84, size * .08, fill=col)
    elif name == "chart":
        c.line([(x + size * .12, y + size * .10), (x + size * .12, y + size * .88),
                (x + size * .92, y + size * .88)], col, 4)
        c.line([(x + size * .20, y + size * .68), (x + size * .42, y + size * .50),
                (x + size * .55, y + size * .60), (x + size * .82, y + size * .26)], col2 or col, 5)
        c.poly([(x + size * .82, y + size * .14), (x + size * .90, y + size * .34),
                (x + size * .68, y + size * .32)], fill=col2 or col)
    elif name == "controller":
        c.rrect(x + size * .06, y + size * .26, size * .88, size * .50, size * .22, fill=col)
        c.rect(x + size * .20, y + size * .42, size * .20, size * .08, fill=(255, 255, 255))
        c.rect(x + size * .26, y + size * .36, size * .08, size * .20, fill=(255, 255, 255))
        c.ellipse(x + size * .66, y + size * .36, size * .10, size * .10, fill=(255, 255, 255))
        c.ellipse(x + size * .78, y + size * .50, size * .10, size * .10, fill=(255, 255, 255))
    elif name == "gavel":
        c.poly([(x + size * .30, y + size * .18), (x + size * .52, y + size * .08),
                (x + size * .62, y + size * .20), (x + size * .40, y + size * .30)], fill=col)
        c.poly([(x + size * .44, y + size * .30), (x + size * .86, y + size * .72),
                (x + size * .74, y + size * .84), (x + size * .32, y + size * .42)], fill=col)
        c.rect(x + size * .12, y + size * .84, size * .62, size * .08, fill=col)
    elif name == "scales":
        c.rect(cx - size * .03, y + size * .12, size * .06, size * .62, fill=col)
        c.rect(x + size * .14, y + size * .16, size * .72, size * .06, fill=col)
        for px in (x + size * .17, x + size * .77):
            c.line([(px + size * .03, y + size * .22), (px - size * .06, y + size * .52)], col, 3)
            c.line([(px + size * .03, y + size * .22), (px + size * .12, y + size * .52)], col, 3)
            c.arc(px - size * .11, y + size * .40, size * .28, size * .24, 0, 180, col, 4)
        c.rect(x + size * .32, y + size * .80, size * .36, size * .08, fill=col)
        c.ellipse(cx - size * .06, y + size * .02, size * .12, size * .12, fill=col)
    elif name == "globe":
        c.ellipse(x + size * .06, y + size * .06, size * .88, size * .88, outline=col, ow=4)
        c.ellipse(cx - size * .18, y + size * .06, size * .36, size * .88, outline=col, ow=3)
        c.line([(x + size * .08, cy), (x + size * .92, cy)], col, 3)
        c.line([(x + size * .16, y + size * .26), (x + size * .84, y + size * .26)], col, 2)
        c.line([(x + size * .16, y + size * .74), (x + size * .84, y + size * .74)], col, 2)
    elif name == "satellite":  # Voyager-like probe
        c.ellipse(x + size * .30, y + size * .30, size * .52, size * .52, outline=col, ow=4)
        c.ellipse(cx + size * .02, cy + size * .02, size * .10, size * .10, fill=col)
        c.line([(x + size * .34, y + size * .66), (x + size * .10, y + size * .90)], col, 4)
        c.line([(x + size * .80, y + size * .34), (x + size * .94, y + size * .12)], col, 3)
        c.rect(x + size * .06, y + size * .06, size * .16, size * .10, fill=col)
    elif name == "painting":
        c.rect(x + size * .08, y + size * .10, size * .84, size * .80, outline=col, ow=6)
        import math
        pts = []
        for i in range(41):
            a = i / 40 * math.pi * 5
            rr = size * (0.05 + 0.16 * i / 40)
            pts.append((cx + rr * math.cos(a), cy - size * .08 + rr * math.sin(a) * .7))
        c.line(pts, col2 or col, 3)
        c.poly([(x + size * .14, y + size * .84), (x + size * .38, y + size * .58),
                (x + size * .55, y + size * .84)], fill=col)
        c.poly([(x + size * .44, y + size * .84), (x + size * .68, y + size * .62),
                (x + size * .86, y + size * .84)], fill=col)
    elif name == "pencil":
        c.poly([(x + size * .22, y + size * .66), (x + size * .66, y + size * .22),
                (x + size * .78, y + size * .34), (x + size * .34, y + size * .78)], fill=col)
        c.poly([(x + size * .22, y + size * .66), (x + size * .14, y + size * .86),
                (x + size * .34, y + size * .78)], fill=col2 or col)
        c.line([(x + size * .10, y + size * .92), (x + size * .90, y + size * .92)], col, 4)
    elif name == "quake":
        pts = [(x + size * .04, cy), (x + size * .26, cy), (x + size * .34, y + size * .16),
               (x + size * .44, y + size * .84), (x + size * .54, y + size * .30),
               (x + size * .62, cy), (x + size * .96, cy)]
        c.line(pts, col, 5)
    elif name == "handshake":  # three-star summit mark
        import math
        for k, a0 in enumerate((-90, 30, 150)):
            a = math.radians(a0)
            sx, sy = cx + size * .30 * math.cos(a), cy + size * .30 * math.sin(a)
            pts = []
            for i in range(10):
                rr = size * (0.13 if i % 2 == 0 else 0.055)
                aa = math.radians(-90 + i * 36)
                pts.append((sx + rr * math.cos(aa), sy + rr * math.sin(aa)))
            c.poly(pts, fill=col)
    elif name == "people":
        for i, px in enumerate((0.22, 0.5, 0.78)):
            c.ellipse(x + size * (px - .09), y + size * .14, size * .18, size * .18, fill=col)
            c.rrect(x + size * (px - .11), y + size * .36, size * .22, size * .34, size * .08, fill=col)
        c.line([(x + size * .10, y + size * .88), (x + size * .90, y + size * .88)], col, 3)
    elif name == "tank":
        c.rrect(x + size * .08, y + size * .55, size * .72, size * .26, size * .10, fill=col)
        c.rrect(x + size * .30, y + size * .36, size * .34, size * .22, size * .06, fill=col)
        c.line([(x + size * .58, y + size * .44), (x + size * .94, y + size * .32)], col, 6)
        c.ellipse(x + size * .14, y + size * .72, size * .60, size * .20, fill=col2 or col)
    elif name == "microphone":
        c.rrect(cx - size * .10, y + size * .06, size * .20, size * .42, size * .10, fill=col)
        c.arc(cx - size * .22, y + size * .22, size * .44, size * .44, 0, 180, col, 4)
        c.line([(cx, y + size * .68), (cx, y + size * .84)], col, 4)
        c.line([(x + size * .30, y + size * .86), (x + size * .70, y + size * .86)], col, 4)
