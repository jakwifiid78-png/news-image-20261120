# news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/jakwifiid78-png/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/jakwifiid78-png/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

Entry for the make.fun competition **news-image-20261120** — "Sum up 20
November's world news in one image" ($250, top 50 paid).

`main.ts` (Node 22, standard library only) copies the committed
`entry.png` to `/output/entry.png`. The image is a 1024×1024 newspaper
front page — "THE WORLD — Friday, 20 November 2026" — rendered
programmatically with Python + PIL (`gen.py`, deterministic: re-running
it produces byte-identical output).

## The day's news (all verified 20 November 2026)

1. **World Court: Myanmar committed genocide against the Rohingya** —
   the International Court of Justice rules 9–6, the first genocide
   finding against a state, over the 2017 crackdown that drove 730,000
   Rohingya to Bangladesh. (One Turn, Bangladesh Chronicle)
2. **Trump, Xi and Putin meet face to face** — first three-way summit
   in Shenzhen; a joint peace declaration. (One Turn, Bangladesh
   Chronicle)
3. **Missile damages Riyadh's tallest tower** — a Houthi missile hits
   the capital's financial district, damaging the Saudi sovereign wealth
   fund tower. (One Turn)
4. **Cyclone Akvan hits India** — landfall near Gopalpur, Odisha, winds
   70–80 km/h gusting to 90; the third cyclone in a month. (Reuters)
5. **Anthropic soars on debut** — shares close ~$97, up 17% on the $83
   offer price in the Nasdaq debut. (One Turn)
6. **Stocks slide, Nikkei −4.8%** — the S&P 500 falls for a fifth
   straight day. (One Turn)

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```
