#!/usr/bin/env python3
"""Render 'THE WORLD IN ONE DAY - Sunday 22 November 2026' front page.

Reads data/stories.json (49 verified 22-Nov-2026 stories), draws a
1024x1024 PNG with PIL. Deterministic: bundled fonts from assets/, fixed
layout, no randomness, no clock. Run: python3 render.py  -> entry.png
"""
import json
import os
import hashlib
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE, "assets")
DATA = os.path.join(BASE, "data", "stories.json")

W, H = 1024, 1024
MARGIN = 16
CW = W - 2 * MARGIN  # 992 content width

# ---- palette: cool blue-grey paper, navy ink, teal accent.
# Red is used ONLY for the sub-headline, DATE CHECK and map pins.
PAPER = (237, 239, 242)
PAPER2 = (226, 230, 236)
INK = (16, 30, 51)
TEAL = (14, 107, 107)
TEAL_DK = (9, 74, 74)
RED = (217, 72, 28)
GOLD = (201, 162, 39)
WHITE = (255, 255, 255)
CARD = (252, 253, 253)
MUTED = (74, 85, 104)
RULE = (185, 194, 206)
SKY = (12, 25, 46)
SKY2 = (20, 38, 66)


def font(name, size):
    return ImageFont.truetype(os.path.join(ASSETS, name), size)


def f_serif_b(s):
    return font("DejaVuSerif-Bold.ttf", s)


def f_serif(s):
    return font("DejaVuSerif.ttf", s)


def f_sans(s):
    return font("DejaVuSans.ttf", s)


def f_sans_b(s):
    return font("DejaVuSans-Bold.ttf", s)


# ---- story data -------------------------------------------------------
with open(DATA, encoding="utf-8") as fh:
    ALL_STORIES = json.load(fh)
BY_TITLE = {s["title"]: s for s in ALL_STORIES}

HERO = "Russian drone strike collapses apartment block in Dymer near Kyiv"
BIG = [
    "COP31 climate talks collapse without a deal over fossil fuels",
    "Houthis say they struck Saudi Arabia's Rabigh oil refinery",
]
MEDIUM = [
    "Australia criticises US report saying AUKUS will shrink submarine fleet",
    "Candy factory fire in Indonesia kills 3, dozens missing",
    "Molly Meldrum, Countdown host, dies at 83",
    "Explosion damages Russian ship docked at Benghazi port",
    "Drone strikes kill five children in Khartoum and Omdurman",
    "Boca Juniors beat Atletico Mineiro to win Copa Sudamericana",
    "Democrats clinch 258 House seats, largest majority since 1992",
    "Settlers torch vehicles and homes in West Bank villages",
    "Iran unveils underground missile facility amid tensions with US",
    "Liverpool thrash Manchester United 4-0",
]
ALSO = [
    "Twenty-one killed in cattle camp attack in Tonj East, South Sudan",
    "Argentina approves $50 billion LNG project",
    "Trump voices concern over China's rapid nuclear expansion",
    "NFL Sunday: Lions, Bears, Bills and Cowboys all win",
    "Albanese meets Xi, defends call for Russia to end war",
    "Zelensky presses US to release paid-for Patriot missiles",
    "Ten thousand rally in Perth against Woodside Scott Reef drilling",
    "Taiwan warns Canada over deepening trade ties with China",
    "Soldiers rescue 18 abducted Kaduna children in Nigeria",
    "China's spy agency reportedly ran campaign to obtain AI chips",
    "Saudi-led coalition says it intercepted Houthi missile",
    "Botswana's President Boko pledges to scrap visas for Africans",
    "Barcelona edge Villarreal 3-2",
    "Argentina asks court to block Falklands Sea Lion drilling",
    "ExxonMobil group approves $4 billion Angola oil project",
    "Codelco admits 42,100 tonnes of copper were fictitious",
    "Nigeria closes Ebola follow-up with no spread found",
    "ANC scrambles to hold South Africa's major cities after poor vote",
    "Almost 600 women slain in South Africa during one quarter",
    "Seventeen dead in two separate mass shootings in South Africa",
    "Atalanta fight back from 2-4 down to draw 4-4 with Inter",
    "Heat scorches Sydney as officials warn of record power demand",
    "Iran begins rationing electricity",
]

SELECTED = [HERO] + BIG + MEDIUM + ALSO
assert len(SELECTED) == 36, len(SELECTED)
for t in SELECTED:
    assert t in BY_TITLE, "missing story: " + t

# Display overrides: condensed titles/summaries (accurate, from the data).
SHORT = {
    "Australia criticises US report saying AUKUS will shrink submarine fleet":
        "Australia hits back at US report on AUKUS",
    "Candy factory fire in Indonesia kills 3, dozens missing":
        "Candy factory fire kills 3, dozens missing",
    "Molly Meldrum, Countdown host, dies at 83":
        "Molly Meldrum, Countdown host, dies at 83",
    "Explosion damages Russian ship docked at Benghazi port":
        "Blast damages Russian ship docked at Benghazi",
    "Drone strikes kill five children in Khartoum and Omdurman":
        "Drone strikes kill five children in Khartoum",
    "Boca Juniors beat Atletico Mineiro to win Copa Sudamericana":
        "Boca Juniors win Copa Sudamericana",
    "Democrats clinch 258 House seats, largest majority since 1992":
        "Democrats clinch 258 House seats",
    "Settlers torch vehicles and homes in West Bank villages":
        "Settlers torch vehicles and homes in West Bank",
    "Iran unveils underground missile facility amid tensions with US":
        "Iran unveils underground 'missile city'",
    "Liverpool thrash Manchester United 4-0":
        "Liverpool thrash Manchester United 4-0",
}
SUMM = {
    "Australia criticises US report saying AUKUS will shrink submarine fleet":
        "Canberra rejects a US report on the AUKUS submarine pact.",
    "Candy factory fire in Indonesia kills 3, dozens missing":
        "A blaze at a factory in Cikande, Banten, leaves 36 missing.",
    "Molly Meldrum, Countdown host, dies at 83":
        "The broadcaster who shaped Australian pop music dies aged 83.",
    "Explosion damages Russian ship docked at Benghazi port":
        "An explosion, suspected to be a drone attack, hits a ship in port.",
    "Drone strikes kill five children in Khartoum and Omdurman":
        "Attacks on Khartoum and Omdurman kill five children, injure 10.",
    "Boca Juniors beat Atletico Mineiro to win Copa Sudamericana":
        "Boca beat Atletico Mineiro 2-0, first continental title in 18 years.",
    "Democrats clinch 258 House seats, largest majority since 1992":
        "Largest House majority since 1992, sealed by a win in N. Carolina.",
    "Settlers torch vehicles and homes in West Bank villages":
        "Twelve vehicles and homes burn near Ramallah; an inquiry opens.",
    "Iran unveils underground missile facility amid tensions with US":
        "Tehran unveils a 'missile city' as tensions with the US rise.",
    "Liverpool thrash Manchester United 4-0":
        "A one-sided Premier League win at Anfield for the champions.",
}
# Short summaries for the two big cards (accurate, from the data).
BIG_SUMM = {
    BIG[0]: "UN talks in Antalya end with no agreement after the EU rejects "
            "a draft that omits fossil fuels.",
    BIG[1]: "The Houthis claim they hit the refinery and a radar site; "
            "Riyadh says a missile was intercepted.",
}
BADGE = {
    HERO: "REPORTED",
    BIG[0]: "REPORTED",
    BIG[1]: "CLAIM",    MEDIUM[0]: "REPORTED",
    MEDIUM[1]: "CONFIRMED",
    MEDIUM[2]: "CONFIRMED",
    MEDIUM[3]: "REPORTED",
    MEDIUM[4]: "REPORTED",
    MEDIUM[5]: "CONFIRMED",
    MEDIUM[6]: "CONFIRMED",
    MEDIUM[7]: "REPORTED",
    MEDIUM[8]: "CLAIM",
    MEDIUM[9]: "CONFIRMED",
}
LOC = {
    HERO: "DYMER, UKRAINE",
    BIG[0]: "ANTALYA, TURKIYE",
    BIG[1]: "RABIGH, SAUDI ARABIA",
    MEDIUM[0]: "CANBERRA, AUSTRALIA",
    MEDIUM[1]: "CIKANDE, INDONESIA",
    MEDIUM[2]: "MELBOURNE, AUSTRALIA",
    MEDIUM[3]: "BENGHAZI, LIBYA",
    MEDIUM[4]: "KHARTOUM, SUDAN",
    MEDIUM[5]: "BARRANQUILLA, COLOMBIA",
    MEDIUM[6]: "WASHINGTON, USA",
    MEDIUM[7]: "RAMALLAH, WEST BANK",
    MEDIUM[8]: "TEHRAN, IRAN",
    MEDIUM[9]: "LIVERPOOL, ENGLAND",
}
# map pins for the 13 illustrated stories (lon, lat); nudged slightly where
# two real locations would overlap on the small map (Canberra/Melbourne,
# Antalya/Ramallah).
PIN = {
    HERO: (30.5, 50.8),
    BIG[0]: (28.5, 38.5),
    BIG[1]: (39.0, 22.8),
    MEDIUM[0]: (152.0, -32.0),
    MEDIUM[1]: (106.2, -6.0),
    MEDIUM[2]: (143.0, -40.0),
    MEDIUM[3]: (20.1, 32.1),
    MEDIUM[4]: (32.5, 15.5),
    MEDIUM[5]: (-74.8, 11.0),
    MEDIUM[6]: (-77.0, 38.9),
    MEDIUM[7]: (37.5, 30.0),
    MEDIUM[8]: (51.4, 35.7),
    MEDIUM[9]: (-3.0, 53.4),
}
# condensed one-line titles for the ALSO ON list (accurate, from the data)
ALSO_SHORT = {
    ALSO[0]: "21 killed in Tonj East camp",
    ALSO[1]: "Argentina OKs $50bn LNG plan",
    ALSO[2]: "Trump: China nukes worry",
    ALSO[3]: "NFL Sunday: four winners",
    ALSO[4]: "Albanese meets Xi",
    ALSO[5]: "Zelensky seeks Patriots",
    ALSO[6]: "Perth rally vs drilling",
    ALSO[7]: "Taiwan warns Canada",
    ALSO[8]: "18 children rescued",
    ALSO[9]: "China AI chip campaign",
    ALSO[10]: "Saudi intercepts missile",
    ALSO[11]: "Botswana: visas scrapped",
    ALSO[12]: "Barcelona 3-2 Villarreal",
    ALSO[13]: "Falklands oil row",
    ALSO[14]: "Exxon OKs $4bn Angola plan",
    ALSO[15]: "Codelco copper row",
    ALSO[16]: "Ebola follow-up ends",
    ALSO[17]: "ANC scrambles in cities",
    ALSO[18]: "581 women slain in SA",
    ALSO[19]: "17 dead in shootings",
    ALSO[20]: "Atalanta draw 4-4 with Inter",
    ALSO[21]: "Sydney heatwave warning",
    ALSO[22]: "Iran rations electricity",
}

REGION_ORDER = ["Europe", "Middle East", "Asia", "Africa",
                "Oceania", "Latin America", "North America"]
REGION_LABEL = {
    "Europe": "EUROPE", "Middle East": "MIDDLE EAST", "Asia": "ASIA",
    "Africa": "AFRICA", "Oceania": "OCEANIA",
    "Latin America": "LATIN AMERICA", "North America": "NORTH AMERICA",
}


# ---- text helpers -------------------------------------------------------
def wrap(d, text, f, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(d, x, y, lines, f, fill, leading):
    for ln in lines:
        d.text((x, y), ln, font=f, fill=fill)
        y += leading
    return y


def badge(d, x, y, text):
    """Certainty badge; returns width used."""
    bg = TEAL
    if text == "CLAIM":
        bg = RED
    elif text == "CONFIRMED":
        bg = INK
    f = f_sans_b(9)
    tw = d.textlength(text, font=f)
    pad = 5
    d.rounded_rectangle([x, y, x + tw + 2 * pad, y + 15], radius=3, fill=bg)
    d.text((x + pad, y + 2), text, font=f, fill=WHITE)
    return tw + 2 * pad


def fit_font(draw, text, fname, start, target_w):
    """Largest size <= start whose width fits target_w."""
    size = start
    while size > 10:
        f = font(fname, size)
        if draw.textlength(text, font=f) <= target_w:
            return f, size
        size -= 1
    return font(fname, size), size


# ---- drawn illustrations (original, in code) ----------------------------
STARS = [(12, 8), (38, 20), (70, 6), (105, 16), (140, 8), (170, 22),
         (205, 10), (240, 18), (275, 7), (310, 20), (345, 9), (380, 16),
         (415, 8), (450, 20), (480, 10), (515, 18), (30, 34), (95, 30),
         (160, 36), (225, 32), (290, 36), (355, 30), (420, 34), (485, 32),
         (60, 46), (130, 44), (200, 48), (270, 44), (340, 48), (410, 44),
         (475, 46)]


def draw_hero_scene(d, x0, y0, w, h):
    """Kyiv night: dark sky, searchlights, drone silhouettes, a collapsed
    block with rubble, smoke and an orange glow. No faces, no photos."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=SKY)
    # stars
    sx = w / 540.0
    sy = h / 60.0
    for (px, py) in STARS:
        d.ellipse([x0 + px * sx - 1, y0 + py * sy - 1,
                   x0 + px * sx + 1, y0 + py * sy + 1], fill=(220, 228, 240))
    # moon
    d.ellipse([x0 + w - 52, y0 + 10, x0 + w - 22, y0 + 40], fill=(226, 230, 238))
    d.ellipse([x0 + w - 46, y0 + 16, x0 + w - 38, y0 + 24], fill=(200, 208, 220))
    # searchlight beams
    d.polygon([(x0 + 30, y0 + h), (x0 + 70, y0 + h), (x0 + 250, y0 + 6)],
              fill=(58, 74, 102))
    d.polygon([(x0 + w - 40, y0 + h), (x0 + w - 80, y0 + h), (x0 + w - 260, y0 + 8)],
              fill=(58, 74, 102))
    # drone silhouettes with red lights
    for (dx, dy) in [(150, 26), (330, 18), (430, 30)]:
        d.ellipse([x0 + dx - 14, y0 + dy - 3, x0 + dx + 14, y0 + dy + 3],
                  fill=(8, 14, 26))
        d.rectangle([x0 + dx - 3, y0 + dy - 7, x0 + dx + 3, y0 + dy + 7],
                    fill=(8, 14, 26))
        d.ellipse([x0 + dx - 2, y0 + dy - 2, x0 + dx + 2, y0 + dy + 2],
                  fill=RED)
    # building silhouettes along the bottom
    base = y0 + h
    bx = x0
    heights = [58, 74, 48, 66, 40, 70, 52, 60, 44, 68, 50]
    bw = w / len(heights)
    for i, bh in enumerate(heights):
        d.rectangle([bx + i * bw, base - bh, bx + (i + 1) * bw - 2, base],
                    fill=(10, 18, 34))
        # lit windows
        for wy in range(int(base - bh + 8), int(base - 6), 12):
            for wx in range(int(bx + i * bw + 6), int(bx + (i + 1) * bw - 8), 11):
                if (i * 7 + wy) % 3 == 0:
                    d.rectangle([wx, wy, wx + 3, wy + 4], fill=GOLD)
    # collapsed block (centre-left): tilted slab + rubble + smoke
    cx = x0 + int(w * 0.30)
    d.polygon([(cx - 70, base), (cx - 58, base - 78), (cx + 20, base - 62),
               (cx + 58, base)], fill=(24, 34, 54))
    d.polygon([(cx - 58, base - 78), (cx - 30, base - 92), (cx + 8, base - 70)],
              fill=(32, 44, 66))
    for (rx, ry, rr) in [(cx - 46, base - 8, 9), (cx - 20, base - 6, 12),
                         (cx + 8, base - 10, 8), (cx + 34, base - 6, 10),
                         (cx - 62, base - 4, 7)]:
        d.ellipse([rx - rr, ry - rr, rx + rr, ry + rr], fill=(40, 52, 74))
    # orange glow + flames at the rubble
    d.ellipse([cx - 34, base - 34, cx + 30, base - 2], fill=(217, 120, 28))
    d.polygon([(cx - 18, base - 2), (cx - 8, base - 30), (cx + 2, base - 2)],
              fill=(240, 180, 60))
    d.polygon([(cx + 4, base - 2), (cx + 12, base - 22), (cx + 20, base - 2)],
              fill=(240, 180, 60))
    # smoke rising (kept inside the illustration box)
    for (sx2, sy2, sr) in [(cx - 30, base - 80, 9), (cx - 8, base - 88, 10),
                           (cx + 16, base - 78, 8), (cx + 2, base - 88, 10)]:
        d.ellipse([sx2 - sr, sy2 - sr, sx2 + sr, sy2 + sr], fill=(90, 100, 118))


def draw_cop31_scene(d, x0, y0, w, h):
    """COP31 hall: teal backdrop, row of flags, podium, delegates."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(18, 74, 84))
    d.rectangle([x0, y0, x0 + w, y0 + 26], fill=TEAL_DK)
    f = f_sans_b(15)
    d.text((x0 + 8, y0 + 5), "COP31", font=f, fill=WHITE)
    # flags
    flag_cols = [(217, 72, 28), (201, 162, 39), (255, 255, 255),
                 (120, 180, 180), (240, 180, 60)]
    fx = x0 + 10
    for i, col in enumerate(flag_cols):
        d.rectangle([fx, y0 + 34, fx + 2, y0 + 66], fill=(220, 226, 234))
        d.rectangle([fx + 2, y0 + 34, fx + 16, y0 + 46], fill=col)
        fx += 18
    # long table + delegates
    d.rectangle([x0 + 6, y0 + 72, x0 + w - 6, y0 + 82], fill=(120, 90, 60))
    for i in range(5):
        hx = x0 + 14 + i * 18
        d.ellipse([hx - 4, y0 + 60, hx + 4, y0 + 68], fill=(230, 220, 200))
        d.rectangle([hx - 5, y0 + 68, hx + 5, y0 + 73], fill=(40, 50, 70))
    # podium
    d.rectangle([x0 + w - 24, y0 + 56, x0 + w - 8, y0 + 82], fill=INK)
    d.rectangle([x0 + w - 22, y0 + 48, x0 + w - 10, y0 + 56], fill=GOLD)


def draw_bahrain_scene(d, x0, y0, w, h):
    """Rabigh refinery at night: towers, radar dish, flames, smoke."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=SKY)
    for (px, py) in [(8, 8), (30, 16), (55, 7), (80, 14)]:
        d.ellipse([x0 + px - 1, y0 + py - 1, x0 + px + 1, y0 + py + 1],
                  fill=(220, 228, 240))
    # refinery towers
    d.rectangle([x0 + 10, y0 + 40, x0 + 22, y0 + h - 8], fill=(30, 44, 66))
    d.rectangle([x0 + 26, y0 + 28, x0 + 40, y0 + h - 8], fill=(24, 36, 56))
    d.rectangle([x0 + 44, y0 + 48, x0 + 58, y0 + h - 8], fill=(30, 44, 66))
    d.rectangle([x0 + 62, y0 + 36, x0 + 72, y0 + h - 8], fill=(24, 36, 56))
    # pipes
    d.line([x0 + 10, y0 + 58, x0 + 78, y0 + 58], fill=GOLD, width=2)
    d.line([x0 + 22, y0 + 44, x0 + 62, y0 + 44], fill=GOLD, width=2)
    # radar dish
    d.arc([x0 + 66, y0 + 6, x0 + 92, y0 + 32], 200, 340, fill=WHITE, width=3)
    d.line([x0 + 79, y0 + 30, x0 + 79, y0 + 44], fill=WHITE, width=2)
    # flames
    d.polygon([(x0 + 30, y0 + h - 8), (x0 + 36, y0 + h - 30), (x0 + 42, y0 + h - 8)],
              fill=(240, 180, 60))
    d.polygon([(x0 + 50, y0 + h - 8), (x0 + 55, y0 + h - 24), (x0 + 60, y0 + h - 8)],
              fill=(217, 120, 28))
    # smoke
    d.ellipse([x0 + 28, y0 + 12, x0 + 44, y0 + 26], fill=(90, 100, 118))
    d.ellipse([x0 + 48, y0 + 6, x0 + 62, y0 + 18], fill=(90, 100, 118))


def draw_motif(d, kind, x0, y0, w, h, bg):
    """Small abstract motif for a medium card (band h~24px)."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=bg)
    cx, cy = x0 + w // 2, y0 + h // 2
    if kind == "sub":
        d.rectangle([x0, y0 + h - 6, x0 + w, y0 + h], fill=(40, 90, 110))
        d.ellipse([cx - 34, cy - 6, cx + 34, cy + 6], fill=INK)
        d.rectangle([cx - 8, cy - 11, cx + 6, cy - 4], fill=INK)
        d.line([cx + 2, cy - 15, cx + 2, cy - 11], fill=INK, width=2)
        d.ellipse([cx + 34, cy - 2, cx + 38, cy + 2], fill=GOLD)
    elif kind == "fire":
        d.rectangle([cx - 30, cy - 2, cx - 8, cy + 9], fill=(60, 60, 70))
        d.rectangle([cx - 26, cy - 12, cx - 20, cy - 2], fill=(60, 60, 70))
        d.rectangle([cx + 4, cy - 6, cx + 30, cy + 9], fill=(60, 60, 70))
        d.polygon([(cx - 22, cy - 2), (cx - 16, cy - 14), (cx - 10, cy - 2)],
                  fill=(240, 180, 60))
        d.polygon([(cx + 10, cy - 6), (cx + 16, cy - 16), (cx + 22, cy - 6)],
                  fill=(217, 120, 28))
        d.ellipse([cx - 28, cy - 20, cx - 14, cy - 10], fill=(150, 155, 165))
    elif kind == "mic":
        d.ellipse([cx - 8, cy - 10, cx + 8, cy + 4], fill=(230, 230, 235))
        d.line([cx - 6, cy - 6, cx + 6, cy - 6], fill=INK, width=1)
        d.line([cx - 6, cy - 2, cx + 6, cy - 2], fill=INK, width=1)
        d.rectangle([cx - 2, cy + 4, cx + 2, cy + 11], fill=(230, 230, 235))
        d.arc([cx - 14, cy - 2, cx + 14, cy + 12], 20, 160, fill=GOLD, width=2)
    elif kind == "ship":
        d.polygon([(cx - 34, cy + 2), (cx + 34, cy + 2), (cx + 26, cy + 9),
                   (cx - 26, cy + 9)], fill=(40, 50, 70))
        d.rectangle([cx - 16, cy - 8, cx + 6, cy + 2], fill=(70, 80, 100))
        d.rectangle([cx - 6, cy - 13, cx - 2, cy - 8], fill=(70, 80, 100))
        for (ex, ey) in [(cx - 30, cy - 10), (cx - 22, cy - 14), (cx - 34, cy - 4)]:
            d.line([ex - 5, ey, ex + 5, ey], fill=GOLD, width=2)
            d.line([ex, ey - 5, ex, ey + 5], fill=GOLD, width=2)
    elif kind == "skyline":
        for i, bh in enumerate([14, 20, 10, 18, 12]):
            bx = cx - 36 + i * 15
            d.rectangle([bx, cy + 10 - bh, bx + 12, cy + 10], fill=(30, 40, 60))
        d.ellipse([cx + 8, cy - 16, cx + 26, cy - 2], fill=(150, 155, 165))
        d.ellipse([cx + 18, cy - 20, cx + 32, cy - 8], fill=(170, 175, 185))
    elif kind == "ball":
        d.ellipse([cx - 26, cy - 10, cx - 6, cy + 10], fill=WHITE)
        d.polygon([(cx - 19, cy - 4), (cx - 13, cy - 4), (cx - 16, cy + 2)],
                  fill=INK)
        d.line([cx - 16, cy - 10, cx - 16, cy - 4], fill=INK, width=1)
        d.line([cx - 22, cy - 2, cx - 16, cy - 2], fill=INK, width=1)
        d.line([cx - 10, cy - 2, cx - 16, cy - 2], fill=INK, width=1)
        d.polygon([(cx + 8, cy - 10), (cx + 26, cy - 10), (cx + 23, cy + 2),
                   (cx + 11, cy + 2)], fill=GOLD)
        d.rectangle([cx + 14, cy + 2, cx + 20, cy + 9], fill=GOLD)
        d.rectangle([cx + 10, cy + 9, cx + 24, cy + 11], fill=GOLD)
    elif kind == "capitol":
        d.arc([cx - 12, cy - 12, cx + 12, cy + 6], 180, 360, fill=WHITE, width=3)
        d.rectangle([cx - 12, cy + 4, cx + 12, cy + 6], fill=WHITE)
        for i in range(4):
            d.rectangle([cx - 14 + i * 8, cy + 6, cx - 11 + i * 8, cy + 11],
                        fill=WHITE)
        d.line([cx, cy - 12, cx, cy - 16], fill=RED, width=2)
        d.rectangle([cx, cy - 16, cx + 7, cy - 13], fill=RED)
    elif kind == "house":
        for (hx, hw) in [(cx - 30, 18), (cx - 4, 22), (cx + 22, 16)]:
            d.rectangle([hx, cy - 2, hx + hw, cy + 10], fill=(50, 55, 70))
            d.polygon([(hx - 2, cy - 2), (hx + hw // 2, cy - 12),
                       (hx + hw + 2, cy - 2)], fill=(90, 60, 50))
        d.polygon([(cx - 12, cy + 10), (cx - 6, cy - 6), (cx, cy + 10)],
                  fill=(240, 180, 60))
        d.polygon([(cx + 6, cy + 10), (cx + 11, cy - 2), (cx + 16, cy + 10)],
                  fill=(217, 120, 28))
    elif kind == "missile":
        d.arc([cx - 30, cy - 12, cx + 30, cy + 12], 180, 360, fill=(30, 40, 60),
              width=4)
        d.rectangle([cx - 30, cy, cx + 30, cy + 2], fill=(30, 40, 60))
        d.rounded_rectangle([cx - 16, cy - 4, cx + 16, cy + 2], radius=3,
                            fill=(200, 205, 215))
        d.polygon([(cx + 16, cy - 4), (cx + 22, cy - 1), (cx + 16, cy + 2)],
                  fill=(200, 205, 215))
        d.polygon([(cx - 10, cy + 2), (cx - 6, cy + 8), (cx - 2, cy + 2)],
                  fill=(200, 205, 215))
    elif kind == "stadium":
        d.arc([cx - 30, cy - 4, cx + 30, cy + 16], 180, 360, fill=WHITE, width=3)
        d.line([cx - 30, cy + 6, cx + 30, cy + 6], fill=WHITE, width=2)
        for (fx, fy) in [(cx - 34, cy - 12), (cx + 34, cy - 12)]:
            d.line([fx, fy + 8, fx, fy - 2], fill=GOLD, width=2)
            d.ellipse([fx - 3, fy - 5, fx + 3, fy + 1], fill=GOLD)
        d.ellipse([cx - 5, cy - 2, cx + 5, cy + 8], fill=WHITE)

MOTIF = {
    MEDIUM[0]: ("sub", (24, 68, 88)),
    MEDIUM[1]: ("fire", (70, 52, 58)),
    MEDIUM[2]: ("mic", (40, 44, 66)),
    MEDIUM[3]: ("ship", (24, 58, 80)),
    MEDIUM[4]: ("skyline", (60, 60, 70)),
    MEDIUM[5]: ("ball", (18, 90, 60)),
    MEDIUM[6]: ("capitol", (30, 60, 90)),
    MEDIUM[7]: ("house", (66, 56, 56)),
    MEDIUM[8]: ("missile", (30, 40, 60)),
    MEDIUM[9]: ("stadium", (90, 30, 40)),
}

# ---- world map ----------------------------------------------------------
CONTINENTS = [
    # North America
    [(-168, 66), (-150, 70), (-130, 71), (-115, 68), (-100, 68), (-90, 66),
     (-85, 69), (-80, 73), (-75, 70), (-70, 62), (-65, 60), (-58, 55),
     (-55, 50), (-60, 46), (-65, 44), (-70, 42), (-74, 39), (-76, 35),
     (-80, 32), (-81, 26), (-84, 30), (-88, 29), (-90, 21), (-94, 18),
     (-97, 16), (-100, 16), (-104, 18), (-107, 22), (-110, 24), (-114, 28),
     (-117, 32), (-122, 37), (-124, 42), (-125, 48), (-130, 55), (-140, 60),
     (-150, 58), (-158, 58), (-165, 60), (-168, 66)],
    # South America
    [(-79, 9), (-76, 10), (-72, 12), (-66, 10), (-61, 9), (-56, 6), (-52, 4),
     (-50, 0), (-46, -2), (-40, -5), (-35, -8), (-37, -12), (-40, -18),
     (-45, -23), (-48, -27), (-52, -32), (-57, -38), (-62, -41), (-65, -45),
     (-68, -50), (-70, -54), (-73, -52), (-73, -45), (-73, -37), (-71, -30),
     (-70, -20), (-75, -15), (-78, -8), (-80, -4), (-80, 2), (-79, 9)],
    # Europe
    [(-10, 36), (-9, 38), (-9, 43), (-2, 44), (-1, 46), (0, 48), (2, 50),
     (4, 52), (7, 54), (8, 57), (10, 58), (12, 56), (18, 56), (21, 55),
     (23, 58), (25, 60), (28, 62), (30, 64), (25, 66), (20, 69), (15, 70),
     (12, 68), (8, 63), (5, 60), (3, 58), (0, 55), (-3, 53), (-5, 50),
     (-8, 48), (-10, 43), (-10, 36)],
    # Africa
    [(-17, 15), (-16, 20), (-12, 25), (-8, 30), (-4, 34), (0, 36), (5, 37),
     (10, 37), (15, 32), (20, 32), (25, 31), (30, 31), (33, 28), (36, 24),
     (38, 20), (40, 15), (43, 12), (47, 11), (51, 10), (50, 5), (46, 0),
     (42, -5), (40, -10), (38, -15), (36, -20), (33, -25), (30, -30),
     (27, -33), (22, -35), (18, -34), (15, -30), (12, -25), (12, -18),
     (10, -10), (9, -2), (9, 4), (5, 5), (0, 6), (-5, 5), (-10, 6),
     (-13, 8), (-16, 12), (-17, 15)],
    # Asia
    [(30, 62), (35, 65), (40, 68), (50, 69), (60, 70), (70, 72), (80, 73),
     (90, 75), (100, 77), (110, 76), (120, 73), (130, 72), (140, 72),
     (150, 70), (160, 69), (170, 67), (178, 66), (175, 62), (170, 60),
     (162, 58), (158, 52), (150, 50), (142, 48), (138, 45), (135, 43),
     (130, 40), (128, 38), (125, 35), (122, 32), (120, 28), (118, 24),
     (114, 22), (110, 20), (108, 15), (105, 10), (102, 8), (100, 10),
     (98, 14), (95, 16), (92, 20), (89, 22), (86, 20), (83, 18), (80, 14),
     (78, 10), (76, 10), (74, 14), (72, 20), (70, 22), (67, 25), (64, 25),
     (61, 25), (58, 26), (56, 27), (53, 27), (51, 29), (49, 30), (47, 30),
     (44, 31), (42, 33), (40, 35), (37, 36), (35, 36), (33, 36), (31, 36),
     (30, 38), (30, 42), (30, 48), (30, 54), (30, 62)],
    # Australia
    [(113, -22), (114, -28), (115, -33), (118, -35), (122, -34), (126, -32),
     (129, -32), (132, -32), (135, -35), (138, -35), (140, -38), (143, -39),
     (146, -39), (149, -37), (150, -34), (153, -31), (153, -27), (151, -24),
     (149, -20), (146, -19), (143, -16), (142, -11), (141, -13), (138, -14),
     (136, -15), (135, -12), (132, -11), (130, -13), (127, -14), (124, -16),
     (121, -18), (118, -20), (115, -21), (113, -22)],
    # New Zealand
    [(167, -45), (170, -42), (173, -40), (175, -38), (177, -38), (178, -37),
     (176, -40), (174, -42), (171, -43), (168, -46), (167, -45)],
    # Japan
    [(130, 31), (132, 33), (134, 34), (136, 35), (138, 35), (140, 37),
     (141, 40), (142, 43), (144, 44), (145, 44), (143, 42), (141, 39),
     (140, 36), (138, 34), (136, 33), (133, 32), (130, 31)],
    # United Kingdom
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 54), (1, 51),
     (-2, 50), (-5, 50)],
    # Madagascar
    [(44, -16), (47, -15), (50, -16), (50, -20), (48, -24), (45, -25),
     (43, -22), (43, -18), (44, -16)],
]


def draw_map(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(214, 221, 230))
    lat_top, lat_bot = 83.0, -57.0

    def proj(lon, lat):
        px = x0 + (lon + 180.0) / 360.0 * w
        py = y0 + (lat_top - lat) / (lat_top - lat_bot) * h
        return (px, py)

    for poly in CONTINENTS:
        pts = [proj(lon, lat) for (lon, lat) in poly]
        d.polygon(pts, fill=(120, 150, 158), outline=TEAL_DK)
    # graticule
    for lon in range(-150, 181, 30):
        px = x0 + (lon + 180.0) / 360.0 * w
        d.line([px, y0, px, y0 + h], fill=(190, 199, 210), width=1)
    for lat in [60, 30, 0, -30]:
        py = y0 + (lat_top - lat) / (lat_top - lat_bot) * h
        d.line([x0, py, x0 + w, py], fill=(190, 199, 210), width=1)
    # pins 1-13
    f = f_sans_b(9)
    for i, title in enumerate([HERO] + BIG + MEDIUM):
        lon, lat = PIN[title]
        px, py = proj(lon, lat)
        r = 7
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED,
                  outline=WHITE, width=1)
        tw = d.textlength(str(i + 1), font=f)
        d.text((px - tw / 2, py - 6), str(i + 1), font=f, fill=WHITE)


# ---- page -----------------------------------------------------------------
def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    x = MARGIN
    y = 12

    # ---- top bar ----
    d.rectangle([x, y, x + CW, y + 20], fill=INK)
    d.text((x + 8, y + 4), "THE WORLD IN ONE DAY", font=f_sans_b(11),
           fill=WHITE)
    right = "36 STORIES  ·  7 REGIONS  ·  EVERY ONE DATED SUNDAY 22 NOVEMBER 2026"
    tw = d.textlength(right, font=f_sans_b(11))
    d.text((x + CW - 8 - tw, y + 4), right, font=f_sans_b(11), fill=WHITE)
    y += 22

    # ---- masthead ----
    f, msize = fit_font(d, "Sunday 22 November 2026", "DejaVuSerif-Bold.ttf",
                        54, CW)
    d.text((x, y + 2), "Sunday 22 November 2026", font=f, fill=INK)
    bbox = d.textbbox((x, y + 2), "Sunday 22 November 2026", font=f)
    rule_y = bbox[3] + 5
    d.line([x, rule_y, x + CW, rule_y], fill=INK, width=2)
    y = rule_y + 4

    # ---- sub-headline (red, serif bold) ----
    sub = ("COP31 COLLAPSES WITHOUT A DEAL  ·  IRAN CLAIMS STRIKES ON U.S. "
           "RADARS IN BAHRAIN  ·  186 RUSSIAN DRONES HIT UKRAINE")
    f, _ = fit_font(d, sub, "DejaVuSerif-Bold.ttf", 17, CW)
    d.text((x, y + 4), sub, font=f, fill=RED)
    y += 28

    # ---- stats strip ----
    stats = [
        ("186", "DRONES FIRED AT UKRAINE"),
        ("161", "DRONES DOWNED OR JAMMED"),
        ("258", "HOUSE SEATS, DEMOCRATS"),
        ("$50BN", "ARGENTINA LNG PROJECT"),
        ("21", "KILLED IN S. SUDAN ATTACK"),
        ("36", "MISSING IN INDONESIA FIRE"),
    ]
    d.rectangle([x, y, x + CW, y + 46], fill=CARD, outline=RULE)
    colw = CW / 6.0
    for i, (num, lab) in enumerate(stats):
        cx = x + colw * i
        fn = f_sans_b(24)
        nw = d.textlength(num, font=fn)
        d.text((cx + (colw - nw) / 2, y + 3), num, font=fn, fill=TEAL_DK)
        fl = f_sans_b(8)
        for li, ln in enumerate(wrap(d, lab, fl, colw - 12)):
            lw = d.textlength(ln, font=fl)
            d.text((cx + (colw - lw) / 2, y + 30 + li * 9), ln, font=fl,
                   fill=MUTED)
        if i:
            d.line([cx, y + 6, cx, y + 40], fill=RULE, width=1)
    y += 48

    # ---- region tabs ----
    counts = {}
    for t in SELECTED:
        counts[BY_TITLE[t]["region"]] = counts.get(BY_TITLE[t]["region"], 0) + 1
    d.rectangle([x, y, x + CW, y + 24], fill=TEAL_DK)
    tx = x + 8
    d.text((tx, y + 6), "REGIONS:", font=f_sans_b(11), fill=(180, 210, 210))
    tx += d.textlength("REGIONS:", font=f_sans_b(11)) + 10
    for reg in REGION_ORDER:
        lab = "%s %d" % (REGION_LABEL[reg], counts.get(reg, 0))
        d.text((tx, y + 6), lab, font=f_sans_b(11), fill=WHITE)
        tx += d.textlength(lab, font=f_sans_b(11)) + 14
    y += 26

    # ---- timeline ----
    timeline = [
        ("00:33", "AUKUS report criticised"),
        ("03:00", "Dymer block collapses"),
        ("06:00", "Factory fire, Cikande"),
        ("08:00", "Molly Meldrum dies, 83"),
        ("12:00", "Blast hits ship, Benghazi"),
        ("16:00", "COP31 collapses, Antalya"),
        ("21:00", "Boca win Copa Sudamericana"),
    ]
    d.rectangle([x, y, x + CW, y + 44], fill=CARD, outline=RULE)
    d.text((x + 8, y + 15), "THE DAY IN UTC", font=f_sans_b(11), fill=TEAL_DK)
    tl_x0 = x + 132
    tl_w = CW - 140
    d.line([tl_x0, y + 22, x + CW - 8, y + 22], fill=RULE, width=2)
    tw_col = tl_w / len(timeline)
    for i, (tm, lab) in enumerate(timeline):
        cx = tl_x0 + tw_col * i + tw_col / 2
        ft = f_sans_b(10)
        tw2 = d.textlength(tm, font=ft)
        d.text((cx - tw2 / 2, y + 6), tm, font=ft, fill=INK)
        d.ellipse([cx - 4, y + 18, cx + 4, y + 26], fill=TEAL, outline=WHITE,
                  width=1)
        fl = f_sans(8)
        lw = d.textlength(lab, font=fl)
        d.text((cx - lw / 2, y + 30), lab, font=fl, fill=MUTED)
    y += 45

    # ---- hero row: hero (55%) + 2 big cards stacked ----
    hero_w = int(CW * 0.55)
    side_w = CW - hero_w - 8
    hero_x, hero_y = x, y
    side_x = x + hero_w + 8
    hero_h = 204
    # hero card
    d.rectangle([hero_x, hero_y, hero_x + hero_w, hero_y + hero_h], fill=CARD,
                outline=RULE)
    draw_hero_scene(d, hero_x + 1, hero_y + 1, hero_w - 2, 100)
    d.rectangle([hero_x + 1, hero_y + 101, hero_x + hero_w - 1, hero_y + 103],
                fill=TEAL)
    hx, hy = hero_x + 10, hero_y + 108
    bw = badge(d, hx, hy, BADGE[HERO])
    d.text((hx + bw + 8, hy + 2), "1  ·  DYMER, UKRAINE  ·  AP",
           font=f_sans_b(10), fill=MUTED)
    hy += 19
    ht = f_serif_b(19)
    for ln in wrap(d, "Russian drone strike collapses apartment block near Kyiv",
                   ht, hero_w - 20):
        d.text((hx, hy), ln, font=ht, fill=INK)
        hy += 22
    hs = f_sans(12)
    summ = ("A five-storey block comes down in Dymer, killing 2 and wounding 4, "
            "with about 11 feared trapped in the rubble - part of a 186-drone "
            "barrage, 161 of them downed.")
    for ln in wrap(d, summ, hs, hero_w - 20):
        d.text((hx, hy), ln, font=hs, fill=INK)
        hy += 15
    # big cards (right column, stacked)
    card_h = (hero_h - 6) // 2
    for ci, title in enumerate(BIG):
        cy = hero_y + ci * (card_h + 6)
        d.rectangle([side_x, cy, side_x + side_w, cy + card_h], fill=CARD,
                    outline=RULE)
        ill_w = 96
        if ci == 0:
            draw_cop31_scene(d, side_x + 1, cy + 1, ill_w - 1, card_h - 2)
        else:
            draw_bahrain_scene(d, side_x + 1, cy + 1, ill_w - 1, card_h - 2)
        tx2 = side_x + ill_w + 8
        tw2 = side_x + side_w - 8
        by = cy + 7
        bw = badge(d, tx2, by, BADGE[title])
        d.text((tx2 + bw + 6, by + 2), "%d  ·  %s" % (ci + 2, LOC[title]),
               font=f_sans_b(9), fill=MUTED)
        by += 18
        bt = f_serif_b(15)
        for ln in wrap(d, SHORT.get(title, title), bt, tw2 - tx2):
            d.text((tx2, by), ln, font=bt, fill=INK)
            by += 17
        bs = f_sans(10)
        s = BIG_SUMM[title]
        for ln in wrap(d, s, bs, tw2 - tx2):
            d.text((tx2, by), ln, font=bs, fill=INK)
            by += 12
        d.text((tx2, cy + card_h - 14), BY_TITLE[title]["source"].upper(),
               font=f_sans_b(9), fill=TEAL_DK)
    y += hero_h + 2

    # ---- 10 medium cards: 2 rows x 5 ----
    gap = 6
    card_w = (CW - gap * 4) // 5
    card_h = 94
    for row in range(2):
        for col in range(5):
            idx = row * 5 + col
            title = MEDIUM[idx]
            cx0 = x + col * (card_w + gap)
            cy0 = y + row * (card_h + gap)
            d.rectangle([cx0, cy0, cx0 + card_w, cy0 + card_h], fill=CARD,
                        outline=RULE)
            kind, bg = MOTIF[title]
            draw_motif(d, kind, cx0 + 1, cy0 + 1, card_w - 2, 24, bg)
            num = str(idx + 4)
            d.ellipse([cx0 + 5, cy0 + 5, cx0 + 19, cy0 + 19], fill=INK)
            fnum = f_sans_b(9)
            nw = d.textlength(num, font=fnum)
            d.text((cx0 + 12 - nw / 2, cy0 + 7), num, font=fnum, fill=WHITE)
            bf = f_sans_b(9)
            btw = d.textlength(BADGE[title], font=bf) + 10
            badge(d, cx0 + card_w - 6 - btw, cy0 + 5, BADGE[title])
            tx3 = cx0 + 6
            ty = cy0 + 29
            tt = f_sans_b(12)
            for ln in wrap(d, SHORT[title], tt, card_w - 12)[:2]:
                d.text((tx3, ty), ln, font=tt, fill=INK)
                ty += 14
            ts = f_sans(10)
            for ln in wrap(d, SUMM[title], ts, card_w - 12)[:2]:
                d.text((tx3, ty), ln, font=ts, fill=MUTED)
                ty += 12
            d.text((tx3, cy0 + card_h - 12),
                   BY_TITLE[title]["source"].upper() + "  ·  " + LOC[title],
                   font=f_sans_b(8), fill=TEAL_DK)
    y += 2 * card_h + gap + 2

    # ---- map (left) + ALSO ON (right) ----
    sec_y = y
    sec_h = 250
    map_w = 380
    also_x = x + map_w + 12
    also_w = CW - map_w - 12
    # map panel
    d.rectangle([x, sec_y, x + map_w, sec_y + sec_h], fill=CARD, outline=RULE)
    d.text((x + 8, sec_y + 6), "WHERE IT HAPPENED", font=f_sans_b(11),
           fill=TEAL_DK)
    d.text((x + 8, sec_y + 20), "Pins match story numbers 1-13",
           font=f_sans(9), fill=MUTED)
    draw_map(d, x + 6, sec_y + 36, map_w - 12, sec_h - 42)
    # ALSO ON panel
    d.rectangle([also_x, sec_y, also_x + also_w, sec_y + sec_h], fill=CARD,
                outline=RULE)
    d.text((also_x + 8, sec_y + 6), "ALSO ON SUNDAY 22 NOVEMBER - 23 MORE",
           font=f_sans_b(11), fill=TEAL_DK)
    d.line([also_x + 8, sec_y + 22, also_x + also_w - 8, sec_y + 22],
           fill=RULE, width=1)
    col_w = (also_w - 16) // 2
    row_h = 18
    f_item = f_sans(13)
    f_num = f_sans_b(13)
    f_src = f_sans(10)
    for i, title in enumerate(ALSO):
        col = i // 12
        row = i % 12
        ix = also_x + 8 + col * col_w
        iy = sec_y + 28 + row * row_h
        num = str(i + 14)
        d.text((ix, iy), num, font=f_num, fill=TEAL_DK)
        nx = ix + d.textlength("36  ", font=f_num)
        d.text((nx, iy), ALSO_SHORT[title], font=f_item, fill=INK)
        sx = nx + d.textlength(ALSO_SHORT[title] + " ", font=f_item)
        d.text((sx, iy + 2), "(" + BY_TITLE[title]["source"] + ")",
               font=f_src, fill=MUTED)
    y = sec_y + sec_h + 2

    # ---- DATE CHECK ----
    dc_h = 72
    d.rectangle([x, y, x + CW, y + dc_h], fill=CARD, outline=RED, width=2)
    d.text((x + 8, y + 5), "DATE CHECK", font=f_sans_b(13), fill=RED)
    d.text((x + 108, y + 6), "Wires read to 23:00 UTC. All 36 stories are "
           "dated Sunday 22 November 2026.", font=f_sans_b(11), fill=INK)
    f_dc = f_sans(10)
    excl = ("NOT SUNDAY - LEFT OUT:  400-drone barrage (19-20 Nov)  ·  "
            "El Chapo capture (20 Nov)  ·  BepiColombo (21 Nov)  ·  "
            "Kryvyi Rih strike (21 Nov)  ·  Peru quake (20 Nov)  ·  "
            "Nvidia probe (20 Nov)  ·  EU-Indonesia deal (21 Nov)")
    ey = y + 26
    for ln in wrap(d, excl, f_dc, CW - 16):
        d.text((x + 8, ey), ln, font=f_dc, fill=INK)
        ey += 12
    ny = ("NOT YET DECIDED AT PRESS TIME:  fate of 11 feared trapped in "
          "Dymer  ·  36 missing after the Cikande fire  ·  4 abducted "
          "children still missing in Kaduna.")
    ny_y = ey + 2
    for li, ln in enumerate(wrap(d, ny, f_dc, CW - 16)):
        d.text((x + 8, ny_y + li * 12), ln, font=f_dc, fill=INK)
    y += dc_h + 2

    # ---- footer ----
    d.line([x, y + 2, x + CW, y + 2], fill=INK, width=1)
    f_ft = f_sans(9)
    srcs = ("SOURCES: Reuters  ·  AP  ·  The Guardian  ·  Radio Dabanga  ·  "
            "Eye Radio  ·  LiveScore  ·  New York Times  ·  Sydney Morning "
            "Herald  ·  WA Today  ·  Juba Global  ·  Starlit Daily  ·  "
            "OneTurn  ·  NN24  ·  PitchLab  ·  news.com.au  ·  EIN Presswire  ·  "
            "StatMuse  ·  Vesper")
    for li, ln in enumerate(wrap(d, srcs, f_ft, CW)):
        d.text((x, y + 6 + li * 11), ln, font=f_ft, fill=MUTED)
    d.text((x, y + 29),
           "Pictures and map: original, drawn in code. Scenes are drawn "
           "illustrations, not photographs.  CONFIRMED = verified by two "
           "sources  ·  REPORTED = carried by the day's wires  ·  CLAIM = "
           "one side's account, labelled as such.",
           font=f_ft, fill=MUTED)

    out = os.path.join(BASE, "entry.png")
    img.save(out, format="PNG", optimize=True)
    data = open(out, "rb").read()
    print("entry.png bytes:", len(data))
    print("entry.png sha256:", hashlib.sha256(data).hexdigest())
    print("stories used:", len(SELECTED))
    print("final y (footer bottom):", y + 40, "of", H)


if __name__ == "__main__":
    render()
