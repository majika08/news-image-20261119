# news-image-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/majika08/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/majika08/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

One image that sums up the world news of **Thursday, November 19, 2026**, drawn entirely
by a program: every letter, flag and pictogram in `entry.png` is rendered in code
(Python/PIL), so the text is crisp and nothing is left to an image model.

The day's eight main stories, in one 1024×1024 panel grid:

1. **Trump, Xi & Putin hold the first-ever US–China–Russia trilateral summit** in
   Shenzhen, on the sidelines of APEC — nuclear arms control, the Ukraine war and Iran
   on the agenda; the Xi–Putin meeting was their 50th.
2. **Iran widens attacks on Gulf neighbours** — a US air base in Kuwait and targets in
   Bahrain hit, drones repelled, three oil tankers afire after mines near Hormuz.
3. **Israel launches a ground operation in central Gaza**; residents flee.
4. **Democrats nominate Hakeem Jeffries for House Speaker** — set to become the first
   African-American Speaker after the midterm sweep; the Senate taken 56–44.
5. **Anthropic's record-breaking IPO** — a reported $107 billion raised, topping
   SpaceX's record debut; Nasdaq ticker ANT.
6. **'Grand Theft Auto VI' launches worldwide** to near-perfect reviews.
7. **The World Court (ICJ) delivers its ruling** in Myanmar's Rohingya genocide case.
8. **Ethiopia–Eritrea clashes raise war fears** — plus Voyager 1 reaching one
   light-day from Earth.

The program itself is the kit's starter pattern: the repository holds the finished
image and `main.ts` copies it to the output directory, byte for byte, on every run.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

This writes `out/entry.png` (1024×1024 PNG, 305,683 bytes), identical to the
`entry.png` in this repository.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
