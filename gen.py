#!/usr/bin/env python3
"""news-image-20261120 generator.

Renders entry.png (1024x1024 newspaper front page, "THE WORLD —
Friday 20 November 2026") with PIL. Deterministic: same input always
produces byte-identical output (no timestamps, no randomness).

News mix, all verified 20 Nov 2026 from real sources (see SOURCES.md):
 1. LEAD — ICJ rules Myanmar committed genocide against the Rohingya,
    9-6 vote, first such finding against a state (ruling 19 Nov, reported
    20 Nov). Sources: One Turn, Bangladesh Chronicle, news.inbox.eu.
 2. Trump, Xi and Putin hold first three-way summit in Shenzhen, joint
    peace declaration after ~70 minutes of talks. Sources: One Turn,
    Bangladesh Chronicle.
 3. Houthi missile damages Riyadh's Public Investment Fund tower in the
    capital's financial district. Sources: One Turn, Morning Briefing.
 4. Cyclone Akvan makes landfall on Odisha-Andhra Pradesh coast, winds
    70-80 km/h gusting to 90; third cyclone in a month. Source: Reuters.
 5. Anthropic Nasdaq debut: shares close ~$97, 17% above the $83 offer
    price. Source: One Turn.
 6. Markets: S&P 500 falls for a fifth straight day; Nikkei drops 4.8%.
    Source: One Turn.
"""
import hashlib
import math

from PIL import Image, ImageDraw, ImageFont

OUT = "/home/hatch/workspace/makefun/entries/news-image-20261120/entry.png"
W, H = 1024, 1024

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

PAPER = (246, 241, 229)
CARD = (255, 255, 255)
INK = (22, 33, 62)
NAVY = (22, 33, 62)
GOLD = (233, 161, 59)
RED = (178, 34, 34)
DECK = (58, 67, 88)
GREY = (110, 110, 110)
TEAL = (14, 120, 110)

MARGIN = 36


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if d.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_text_block(d, x, y, max_w, text, fnt, fill, leading=None):
    """Draw wrapped text; return y just below last line."""
    lines = wrap(d, text, fnt, max_w)
    lh = leading or int(fnt.size * 1.28)
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def kicker(d, x, y, text, color=RED):
    d.text((x, y), text, font=font(SANS_B, 19), fill=color)
    return y + 26


def rule(d, x0, x1, y, fill=INK, w=2):
    d.line([(x0, y), (x1, y)], fill=fill, width=w)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------- Masthead ----------
d.text((W // 2, 26), "THE WORLD", font=font(SERIF_B, 84), fill=INK,
       anchor="ma")
d.text((W // 2, 126), "FRIDAY, 20 NOVEMBER 2026  •  THE DAY'S NEWS IN ONE PAGE",
       font=font(SANS_B, 21), fill=INK, anchor="ma")
rule(d, MARGIN, W - MARGIN, 158, INK, 3)
rule(d, MARGIN, W - MARGIN, 164, INK, 1)

# ---------- Lead card: ICJ ruling ----------
lx0, ly0, lx1, ly1 = MARGIN, 178, W - MARGIN, 470
d.rectangle([lx0, ly0, lx1, ly1], fill=CARD, outline=INK, width=2)
# visual panel on the right: navy with scales of justice
vx0, vy0, vx1, vy1 = lx1 - 250, ly0, lx1, ly1
d.rectangle([vx0, vy0, vx1, vy1], fill=NAVY)
cx, top = (vx0 + vx1) // 2, vy0 + 52
# scales glyph: post, crossbar, two pans
d.line([(cx, top), (cx, top + 130)], fill=GOLD, width=7)
d.line([(cx - 62, top + 14), (cx + 62, top + 14)], fill=GOLD, width=6)
d.ellipse([cx - 8, top - 10, cx + 8, top + 6], fill=GOLD)
for sx in (cx - 62, cx + 62):
    d.line([(sx, top + 14), (sx - 26, top + 66)], fill=GOLD, width=4)
    d.line([(sx, top + 14), (sx + 26, top + 66)], fill=GOLD, width=4)
    d.arc([sx - 30, top + 52, sx + 30, top + 92], 0, 180, fill=GOLD, width=5)
d.rectangle([cx - 42, top + 130, cx + 42, top + 140], fill=GOLD)
d.text((cx, vy1 - 52), "THE HAGUE", font=font(SANS_B, 20), fill=(255, 255, 255),
       anchor="ma")

tx = lx0 + 24
ty = ly0 + 16
ty = kicker(d, tx, ty, "JUSTICE  •  THE HAGUE")
ty = draw_text_block(d, tx, ty, vx0 - tx - 24,
                     "WORLD COURT: MYANMAR COMMITTED GENOCIDE AGAINST THE ROHINGYA",
                     font(SERIF_B, 36), INK, leading=44)
ty = draw_text_block(d, tx, ty + 10, vx0 - tx - 24,
                     "The International Court of Justice rules 9–6 — the first "
                     "genocide finding against a state — over the 2017 crackdown "
                     "that drove 730,000 Rohingya to Bangladesh.",
                     font(SANS, 20), DECK, leading=27)
assert ty <= ly1 - 12, f"lead deck overflow: {ty} > {ly1 - 12}"

# ---------- Row 2: two cards ----------
ry0, ry1 = 484, 706
rw = (W - 2 * MARGIN - 16) // 2
cards2 = [
    ("SUMMIT  •  SHENZHEN, CHINA", "TRUMP, XI AND PUTIN MEET FACE TO FACE",
     "The three leaders hold their first three-way summit and sign a "
     "joint peace declaration.", "flags"),
    ("CONFLICT  •  RIYADH", "MISSILE DAMAGES RIYADH'S TALLEST TOWER",
     "A Houthi missile hits the financial district, damaging the Saudi "
     "wealth fund tower.", "tower"),
]
for i, (kick, head, deck, vis) in enumerate(cards2):
    x0 = MARGIN + i * (rw + 16)
    x1 = x0 + rw
    d.rectangle([x0, ry0, x1, ry1], fill=CARD, outline=INK, width=2)
    # visual strip at top of card
    d.rectangle([x0, ry0, x1, ry0 + 48], fill=NAVY)
    if vis == "flags":
        # three flag bars: US stars&stripes hint, China red, Russia tricolour
        bw = (x1 - x0 - 48) // 3
        for j, cols in enumerate([((30, 60, 140), (255, 255, 255)),
                                  ((200, 30, 30), (255, 215, 0)),
                                  ((255, 255, 255), (0, 60, 160))]):
            bx = x0 + 24 + j * bw
            d.rectangle([bx, ry0 + 8, bx + bw - 8, ry0 + 40], fill=cols[0])
            d.rectangle([bx, ry0 + 8, bx + bw - 8, ry0 + 20], fill=cols[1])
        d.text(((x0 + x1) // 2, ry0 + 12), "", font=font(SANS_B, 10),
               fill=(255, 255, 255))
    else:
        # tower silhouette + burst
        txc = (x0 + x1) // 2
        d.rectangle([txc - 14, ry0 + 10, txc + 14, ry0 + 48], fill=GOLD)
        d.rectangle([txc - 22, ry0 + 40, txc + 22, ry0 + 48], fill=GOLD)
        for ang in range(0, 360, 45):
            a = math.radians(ang)
            d.line([(txc + 52 * math.cos(a), ry0 + 24 + 16 * math.sin(a)),
                    (txc + 66 * math.cos(a), ry0 + 24 + 16 * math.sin(a))],
                   fill=(255, 220, 90), width=3)
        d.ellipse([txc - 7, ry0 + 17, txc + 7, ry0 + 31], fill=(255, 220, 90))
    ty = ry0 + 62
    ty = kicker(d, x0 + 18, ty, kick)
    ty = draw_text_block(d, x0 + 18, ty, rw - 36, head,
                         font(SERIF_B, 27), INK, leading=33)
    ty = draw_text_block(d, x0 + 18, ty + 6, rw - 36, deck,
                         font(SANS, 19), DECK, leading=25)
    assert ty <= ry1 - 10, f"row2 card {i} overflow: {ty} > {ry1 - 10}"

# ---------- Row 3: three cards ----------
ry0, ry1 = 720, 962
rw = (W - 2 * MARGIN - 2 * 14) // 3
cards3 = [
    ("WEATHER  •  INDIA", "CYCLONE AKVAN HITS INDIA",
     "Akvan makes landfall near Gopalpur, winds 70–80 km/h "
     "gusting to 90.", "spiral"),
    ("TECH  •  NEW YORK", "ANTHROPIC SOARS ON DEBUT",
     "Shares close ~$97, up 17% on the $83 offer in the Nasdaq "
     "debut.", "up"),
    ("MARKETS", "STOCKS SLIDE, NIKKEI -4.8%",
     "S&P 500 falls again; Japan's Nikkei drops 4.8% in a global "
     "sell-off.", "down"),
]
for i, (kick, head, deck, vis) in enumerate(cards3):
    x0 = MARGIN + i * (rw + 14)
    x1 = x0 + rw
    d.rectangle([x0, ry0, x1, ry1], fill=CARD, outline=INK, width=2)
    # icon disc
    icx, icy = (x0 + x1) // 2, ry0 + 40
    d.ellipse([icx - 26, icy - 26, icx + 26, icy + 26], fill=NAVY)
    if vis == "spiral":
        pts = []
        for t in range(0, 540, 12):
            r = 4 + t / 540 * 22
            a = math.radians(t)
            pts.append((icx + r * math.cos(a), icy + r * math.sin(a)))
        d.line(pts, fill=(255, 255, 255), width=3)
    elif vis == "up":
        d.line([(icx - 20, icy + 14), (icx - 6, icy + 2), (icx + 4, icy + 8),
                (icx + 20, icy - 14)], fill=(255, 255, 255), width=4)
        d.line([(icx + 20, icy - 14), (icx + 10, icy - 14)], fill=(255, 255, 255), width=4)
        d.line([(icx + 20, icy - 14), (icx + 20, icy - 4)], fill=(255, 255, 255), width=4)
    else:
        d.line([(icx - 20, icy - 14), (icx - 6, icy - 2), (icx + 4, icy - 8),
                (icx + 20, icy + 14)], fill=(255, 255, 255), width=4)
        d.line([(icx + 20, icy + 14), (icx + 10, icy + 14)], fill=(255, 255, 255), width=4)
        d.line([(icx + 20, icy + 14), (icx + 20, icy + 4)], fill=(255, 255, 255), width=4)
    ty = ry0 + 72
    ty = kicker(d, x0 + 16, ty, kick)
    ty = draw_text_block(d, x0 + 16, ty, rw - 32, head,
                         font(SERIF_B, 22), INK, leading=27)
    ty = draw_text_block(d, x0 + 16, ty + 6, rw - 32, deck,
                         font(SANS, 17), DECK, leading=23)
    assert ty <= ry1 - 10, f"row3 card {i} overflow: {ty} > {ry1 - 10}"

# ---------- Footer ----------
rule(d, MARGIN, W - MARGIN, 978, INK, 1)
d.text((W // 2, 988), "Sources: Reuters  •  One Turn  •  Bangladesh Chronicle  •  20 November 2026",
       font=font(SANS, 15), fill=GREY, anchor="ma")

img.save(OUT, optimize=True)
print("saved", OUT)
print("sha256", hashlib.sha256(open(OUT, "rb").read()).hexdigest())
import os
print("bytes", os.path.getsize(OUT))
