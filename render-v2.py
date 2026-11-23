#!/usr/bin/env python3
"""Render v2 'THE WORLD IN ONE DAY - Sunday 22 November 2026' (Concept B:
The Map Is the Front Page).

Reads data/stories-v2.json (36 verified 22-Nov-2026 stories: 3 heroes,
10 medium, 23 listed), draws a 1024x1024 PNG with PIL. Deterministic:
bundled fonts from assets/, fixed layout, no randomness, no clock.
Run: python3 render-v2.py  -> entry.png

Palette: warm cream winner palette (NOT the cold blue-grey of v1).
Layout: masthead + red sub-headline + 6-number stats strip + 3 EQUAL
hero cards (warm Kyiv night / COP31 / Verstappen) + BIG functional map
with 13 numbered pins + 8-event UTC timeline + 10 medium cards +
ALSO ON 23 rows in 3 columns + red-framed DATE CHECK + sources footer.
"""
import json
import os
import hashlib
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE, "assets")
DATA = os.path.join(BASE, "data", "stories-v2.json")

W, H = 1024, 1024
MARGIN = 16
CW = W - 2 * MARGIN  # 992 content width

# ---- palette: warm cream winner palette (spec 8.1) --------------------
PAPER = (245, 239, 227)      # #F5EFE3 warm cream paper
PANEL = (255, 253, 246)      # #FFFDF6 card panel
INK = (20, 20, 20)           # #141414 main ink
NAVY = (16, 30, 51)          # #101E33 headline navy
RED = (217, 72, 28)          # #D9481C vermilion
GOLD = (201, 162, 39)        # #C9A227 gold accent
GREY = (107, 107, 107)       # #6B6B6B secondary text
SEA = (220, 228, 232)        # #DCE4E8 very pale map sea
LAND = (231, 217, 181)       # warm sand land on the map
LAND_LINE = (176, 150, 100)  # land outline
SKY = (27, 42, 74)           # #1B2A4A warm Kyiv night sky
FIRE = (232, 114, 42)        # #E8722A orange fire
AMBER = (242, 183, 5)        # #F2B705 amber windows
FLAME = (240, 180, 60)       # flame yellow-orange
DC_BG = (253, 243, 238)      # #FDF3EE date-check background
RULE = (200, 185, 150)       # hairline rule on cream
WHITE = (255, 255, 255)
GREEN = (46, 125, 50)        # sports green, sparingly


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
    V2 = json.load(fh)
STORIES = V2["stories"]
BY_ID = {s["id"]: s for s in STORIES}
HEROES = [s for s in STORIES if s["role"] == "hero"]
MEDIUM = [s for s in STORIES if s["role"] == "medium"]
ALSO = [s for s in STORIES if s["role"] == "also"]
assert len(HEROES) == 3 and len(MEDIUM) == 10 and len(ALSO) == 23
ILLUSTRATED = HEROES + MEDIUM  # 13 stories, pinned on the map

# Condensed hero summaries (accurate, from the data; fit 2 lines at 12pt).
HERO_SUMM = {
    "v2-02": "Talks in Antalya collapse over fossil fuels; no deal as summit "
              "closes, 16:00 UTC.",
}
# Condensed medium summaries (accurate, from the data; fit 2 lines at 11pt).
MED_SUMM = {
    "v2-04": "856 candidates, 723 seats, turnout 98.79%.",
    "v2-05": "Rahul 136, Pant 128; lead 352 over New Zealand.",
    "v2-06": "Attacked Saturday; fire burns on, 16 crew evacuated.",
    "v2-07": "3 killed in aid-van strike; Hamas seeks talks Sunday.",
    "v2-08": "Largest House majority since 1992.",
    "v2-09": "Strikes hit Khartoum and Omdurman, 17:20 UTC.",
    "v2-10": "Beat Atl\u00e9tico Mineiro 2\u20130 in Barranquilla.",
    "v2-11": "6\u20132, 7\u20136(7); first ATP Finals title, $5.17M.",
    "v2-12": "Rolling cuts up to 2 hours a day; fuel shortages.",
    "v2-13": "Stable and conscious; son says difficult night.",
}
# Condensed ALSO ON titles (accurate, from the data) + short source.
ALSO_SHORT = {
    "v2-14": ("Cikande fire kills 3, 36 missing", "AP"),
    "v2-15": ("Houthis claim Rabigh strike", "Reuters"),
    "v2-16": ("Blast hits Russian ship in Benghazi", "Reuters"),
    "v2-17": ("Australia hits back at AUKUS report", "Reuters"),
    "v2-18": ("Molly Meldrum dies at 83", "Guardian"),
    "v2-19": ("Pope hosts lunch for 1,300 in need", "Vatican News"),
    "v2-20": ("Wembanyama drops 50 in Spurs win", "AP"),
    "v2-21": ("FBI probes hack of crime database", "AP"),
    "v2-22": ("Nepal PM arrives in New Delhi", "MFA Nepal"),
    "v2-23": ("Settlers torch West Bank homes", "AP"),
    "v2-24": ("Iran unveils missile base", "Reuters"),
    "v2-25": ("21 killed in Tonj East camp attack", "Eye Radio"),
    "v2-26": ("Liverpool 4-0 Man United", "LiveScore"),
    "v2-27": ("NFL Sunday: four winners", "Reuters"),
    "v2-28": ("Albanese meets Xi, urges end to war", "SMH"),
    "v2-29": ("China AI chip campaign alleged", "NYT"),
    "v2-30": ("Barcelona edge Villarreal 3-2", "LiveScore"),
    "v2-31": ("China cuts stock margin to 80%", "Reuters"),
    "v2-32": ("PBS drugs capped at $25 to 2030", "ABC"),
    "v2-33": ("Lula protects Raoni territory", "EIN Presswire"),
    "v2-34": ("Michigan stuns UCLA in 3OT, 18-16", "StatMuse"),
    "v2-35": ("Perth rally against gas drilling", "WA Today"),
    "v2-36": ("Paredes collapses on live TV", "EIN Presswire"),
}
# Map pins for the 13 illustrated stories (lon, lat) — real locations.
PIN = {
    "v2-01": (30.5, 50.8),    # Dymer, Ukraine
    "v2-02": (30.5, 36.9),    # Antalya, Turkiye
    "v2-03": (-115.1, 36.2),  # Las Vegas, USA
    "v2-04": (114.2, 22.3),   # Hong Kong
    "v2-05": (91.7, 26.1),    # Guwahati, India
    "v2-06": (23.0, 59.0),    # Baltic / Finnish waters
    "v2-07": (34.5, 31.5),    # Gaza
    "v2-08": (-77.0, 38.9),   # Washington, USA
    "v2-09": (32.5, 15.5),    # Khartoum, Sudan
    "v2-10": (-74.8, 11.0),   # Barranquilla, Colombia
    "v2-11": (7.7, 45.1),     # Turin, Italy
    "v2-12": (51.4, 35.7),    # Tehran, Iran
    "v2-13": (-47.9, -15.8),  # Brasilia, Brazil
}
REGION_LABEL = {
    "Europe": "EUROPE", "Middle East": "MIDDLE EAST", "Asia": "ASIA",
    "Africa": "AFRICA", "Oceania": "OCEANIA",
    "Latin America": "LATIN AMERICA", "North America": "NORTH AMERICA",
}
HERO_LOC = {"v2-01": "DYMER, UKRAINE", "v2-02": "ANTALYA, T\u00dcRKIYE",
            "v2-03": "LAS VEGAS, USA"}


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


def fit_font(draw, text, fname, start, target_w):
    """Largest size <= start whose width fits target_w."""
    size = start
    while size > 10:
        f = font(fname, size)
        if draw.textlength(text, font=f) <= target_w:
            return f, size
        size -= 1
    return font(fname, size), size


# ---- hero illustrations (original, drawn in code) -----------------------
STARS = [(12, 8), (38, 20), (70, 6), (105, 16), (140, 8), (170, 22),
         (205, 10), (240, 18), (275, 7), (310, 20), (345, 9), (380, 16),
         (415, 8), (450, 20), (480, 10), (515, 18), (30, 34), (95, 30),
         (160, 36), (225, 32), (290, 36), (355, 30), (420, 34), (485, 32),
         (60, 46), (130, 44), (200, 48), (270, 44), (340, 48), (410, 44),
         (475, 46)]


def draw_kyiv(d, x0, y0, w, h):
    """Kyiv night, WARM: navy sky, amber windows, orange fire glow.
    No faces, no photos."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=SKY)
    sx = w / 540.0
    sy = h / 56.0
    for (px, py) in STARS:
        d.ellipse([x0 + px * sx - 1, y0 + py * sy - 1,
                   x0 + px * sx + 1, y0 + py * sy + 1], fill=(235, 225, 190))
    # moon
    d.ellipse([x0 + w - 50, y0 + 8, x0 + w - 20, y0 + 38], fill=(240, 232, 200))
    d.ellipse([x0 + w - 44, y0 + 14, x0 + w - 36, y0 + 22], fill=(215, 205, 170))
    # searchlight beams (lighter navy, warm-tinged)
    d.polygon([(x0 + 28, y0 + h), (x0 + 68, y0 + h), (x0 + 250, y0 + 6)],
              fill=(52, 70, 108))
    d.polygon([(x0 + w - 38, y0 + h), (x0 + w - 78, y0 + h), (x0 + w - 250, y0 + 8)],
              fill=(52, 70, 108))
    # drone silhouettes with red lights
    for (dx, dy) in [(150, 24), (330, 16), (430, 28)]:
        d.ellipse([x0 + dx - 13, y0 + dy - 3, x0 + dx + 13, y0 + dy + 3],
                  fill=(10, 16, 30))
        d.rectangle([x0 + dx - 3, y0 + dy - 7, x0 + dx + 3, y0 + dy + 7],
                    fill=(10, 16, 30))
        d.ellipse([x0 + dx - 2, y0 + dy - 2, x0 + dx + 2, y0 + dy + 2],
                  fill=RED)
    # building silhouettes along the bottom, MANY amber windows
    base = y0 + h
    heights = [52, 66, 44, 60, 38, 64, 48, 56, 42, 62, 46]
    bw = w / len(heights)
    for i, bh in enumerate(heights):
        d.rectangle([x0 + i * bw, base - bh, x0 + (i + 1) * bw - 2, base],
                    fill=(13, 22, 42))
        for wy in range(int(base - bh + 8), int(base - 6), 11):
            for wx in range(int(x0 + i * bw + 5), int(x0 + (i + 1) * bw - 7), 10):
                if (i * 5 + wy) % 2 == 0:
                    d.rectangle([wx, wy, wx + 3, wy + 4], fill=AMBER)
    # collapsed block (centre-left): tilted slab + rubble + smoke
    cx = x0 + int(w * 0.30)
    d.polygon([(cx - 66, base), (cx - 54, base - 70), (cx + 18, base - 56),
               (cx + 54, base)], fill=(22, 32, 54))
    d.polygon([(cx - 54, base - 70), (cx - 28, base - 84), (cx + 6, base - 64)],
              fill=(30, 42, 66))
    for (rx, ry, rr) in [(cx - 44, base - 8, 8), (cx - 18, base - 6, 11),
                         (cx + 8, base - 9, 7), (cx + 32, base - 6, 9),
                         (cx - 58, base - 4, 6)]:
        d.ellipse([rx - rr, ry - rr, rx + rr, ry + rr], fill=(38, 50, 74))
    # big warm orange glow + flames at the rubble
    d.ellipse([cx - 36, base - 32, cx + 32, base - 2], fill=FIRE)
    d.polygon([(cx - 18, base - 2), (cx - 8, base - 28), (cx + 2, base - 2)],
              fill=FLAME)
    d.polygon([(cx + 4, base - 2), (cx + 12, base - 20), (cx + 20, base - 2)],
              fill=FLAME)
    # smoke rising (kept inside the illustration box)
    for (sx2, sy2, sr) in [(cx - 28, base - 72, 8), (cx - 6, base - 80, 9),
                           (cx + 14, base - 70, 7), (cx + 2, base - 80, 9)]:
        d.ellipse([sx2 - sr, sy2 - sr, sx2 + sr, sy2 + sr], fill=(96, 104, 126))


def draw_cop31(d, x0, y0, w, h):
    """COP31 hall, empty: cream wall, COP31 banner, flags, long table
    with empty chairs, wall clock at 16:00, podium. No faces."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(238, 226, 196))
    # banner
    d.rectangle([x0, y0, x0 + w, y0 + 24], fill=NAVY)
    f = f_sans_b(14)
    d.text((x0 + 8, y0 + 4), "COP31", font=f, fill=WHITE)
    d.text((x0 + 66, y0 + 7), "ANTALYA", font=f_sans_b(10), fill=(200, 210, 230))
    # wall clock (16:00)
    ccx, ccy = x0 + w - 30, y0 + 44
    d.ellipse([ccx - 13, ccy - 13, ccx + 13, ccy + 13], fill=WHITE,
              outline=NAVY, width=2)
    d.line([ccx, ccy, ccx + 8, ccy - 4], fill=NAVY, width=2)
    d.line([ccx, ccy, ccx, ccy - 9], fill=NAVY, width=2)
    # flags along the wall
    flag_cols = [RED, GOLD, (46, 125, 50), (41, 98, 168), (120, 60, 140),
                 (230, 230, 230)]
    fx = x0 + 10
    for col in flag_cols:
        d.rectangle([fx, y0 + 30, fx + 2, y0 + 58], fill=(120, 110, 90))
        d.rectangle([fx + 2, y0 + 30, fx + 15, y0 + 41], fill=col)
        fx += 19
    # long table + empty chairs
    ty = y0 + h - 34
    d.rectangle([x0 + 8, ty, x0 + w - 8, ty + 12], fill=(107, 79, 42))
    d.rectangle([x0 + 8, ty + 12, x0 + w - 8, ty + 16], fill=(88, 64, 34))
    for i in range(6):
        chx = x0 + 22 + i * 50
        d.rectangle([chx - 9, ty - 22, chx + 9, ty - 2], fill=NAVY)
        d.rectangle([chx - 11, ty - 26, chx + 11, ty - 20], fill=(24, 44, 72))
        d.rectangle([chx - 6, ty + 2, chx + 6, ty + 6], fill=WHITE)
    # podium with microphone
    d.rectangle([x0 + w - 52, ty - 30, x0 + w - 14, ty], fill=(60, 48, 32))
    d.line([x0 + w - 33, ty - 30, x0 + w - 33, ty - 42], fill=INK, width=2)
    d.ellipse([x0 + w - 37, ty - 48, x0 + w - 29, ty - 40], fill=INK)


def draw_f1(d, x0, y0, w, h):
    """Las Vegas GP at night: dark sky, neon light trails, skyline with
    lit windows, road, F1 car silhouette, checkered flag."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(16, 30, 51))
    for (px, py) in [(10, 8), (40, 16), (75, 6), (110, 14), (150, 8),
                     (190, 16), (230, 6), (270, 14), (305, 8)]:
        d.ellipse([x0 + px - 1, y0 + py - 1, x0 + px + 1, y0 + py + 1],
                  fill=(220, 228, 240))
    # skyline with lit windows
    base = y0 + h
    heights = [34, 48, 28, 42, 30, 52, 36, 44]
    bw = w / len(heights)
    for i, bh in enumerate(heights):
        d.rectangle([x0 + i * bw, base - 62 - bh + 20, x0 + (i + 1) * bw - 2,
                     base - 42], fill=(10, 18, 34))
        for wy in range(int(base - 62 - bh + 26), int(base - 46), 9):
            for wx in range(int(x0 + i * bw + 4), int(x0 + (i + 1) * bw - 6), 9):
                if (i * 3 + wy) % 2 == 0:
                    d.rectangle([wx, wy, wx + 2, wy + 3], fill=AMBER)
    # neon light trails
    d.line([x0, base - 40, x0 + w, base - 46], fill=(224, 64, 155), width=3)
    d.line([x0, base - 34, x0 + w, base - 30], fill=(41, 182, 246), width=2)
    d.line([x0, base - 28, x0 + w, base - 26], fill=GOLD, width=2)
    # road
    d.rectangle([x0, base - 24, x0 + w, base], fill=(24, 26, 30))
    for dx in range(0, int(w), 26):
        d.rectangle([x0 + dx, base - 13, x0 + dx + 13, base - 10],
                    fill=(220, 220, 220))
    # F1 car (side profile, red)
    cx, cy = x0 + int(w * 0.42), base - 24
    d.polygon([(cx - 78, cy), (cx - 70, cy - 8), (cx - 20, cy - 10),
               (cx + 8, cy - 16), (cx + 34, cy - 16), (cx + 52, cy - 10),
               (cx + 74, cy - 8), (cx + 78, cy), (cx + 60, cy + 2),
               (cx - 60, cy + 2)], fill=RED)
    d.polygon([(cx + 8, cy - 16), (cx + 14, cy - 24), (cx + 30, cy - 24),
               (cx + 34, cy - 16)], fill=(30, 30, 34))
    d.rectangle([cx + 56, cy - 22, cx + 78, cy - 18], fill=(30, 30, 34))
    d.rectangle([cx + 74, cy - 18, cx + 76, cy - 6], fill=(30, 30, 34))
    for wx in (cx - 52, cx + 52):
        d.ellipse([wx - 11, cy - 9, wx + 11, cy + 11], fill=(8, 8, 10))
        d.ellipse([wx - 5, cy - 4, wx + 5, cy + 5], fill=(120, 125, 135))
    # speed lines
    for (lx, ly, ll) in [(cx - 110, cy - 14, 26), (cx - 96, cy - 4, 18),
                         (cx + 100, cy - 12, 22)]:
        d.line([lx, ly, lx + ll, ly], fill=(200, 210, 230), width=2)
    # checkered flag on a pole at the right
    fx = x0 + w - 26
    d.rectangle([fx, y0 + 30, fx + 2, y0 + 66], fill=(220, 220, 220))
    for r in range(3):
        for c in range(4):
            col = INK if (r + c) % 2 == 0 else WHITE
            d.rectangle([fx + 2 + c * 5, y0 + 30 + r * 5,
                         fx + 7 + c * 5, y0 + 35 + r * 5], fill=col)


# ---- world map ----------------------------------------------------------
# Simplified continent outlines (own simplification from geography).
CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69), (-85, 66),
     (-80, 73), (-70, 62), (-60, 55), (-55, 47), (-65, 44), (-70, 40),
     (-76, 35), (-80, 26), (-84, 30), (-90, 21), (-95, 16), (-105, 20),
     (-110, 24), (-115, 29), (-120, 34), (-124, 42), (-125, 49), (-135, 58),
     (-150, 58), (-160, 55), (-168, 66)],
    # South America
    [(-79, 9), (-72, 12), (-62, 10), (-55, 5), (-50, 0), (-44, -3),
     (-35, -8), (-38, -15), (-41, -22), (-48, -28), (-55, -35), (-62, -41),
     (-68, -50), (-70, -54), (-74, -48), (-73, -37), (-71, -30), (-70, -19),
     (-76, -14), (-80, -5), (-79, 9)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (3, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 59), (28, 62), (30, 64), (25, 66), (20, 70),
     (15, 69), (10, 64), (5, 60), (0, 55), (-4, 51), (-8, 48), (-10, 43),
     (-10, 36)],
    # Africa
    [(-17, 15), (-13, 24), (-8, 30), (-2, 35), (5, 37), (11, 34), (20, 32),
     (30, 31), (34, 28), (38, 20), (43, 12), (51, 11), (50, 4), (43, -3),
     (40, -10), (36, -18), (33, -25), (28, -33), (20, -35), (16, -30),
     (12, -22), (12, -15), (9, -5), (9, 4), (2, 6), (-6, 5), (-12, 7),
     (-17, 15)],
    # Asia
    [(30, 62), (40, 68), (55, 69), (70, 72), (85, 74), (100, 77),
     (115, 76), (130, 72), (145, 71), (160, 69), (175, 66), (170, 60),
     (160, 55), (150, 48), (142, 44), (135, 42), (128, 38), (124, 33),
     (120, 28), (114, 22), (108, 15), (104, 9), (100, 12), (96, 16),
     (92, 21), (88, 22), (84, 19), (80, 14), (77, 10), (74, 16), (70, 22),
     (66, 25), (61, 25), (57, 27), (53, 28), (50, 30), (47, 31), (43, 34),
     (40, 36), (36, 36), (33, 37), (30, 42), (30, 50), (30, 62)],
    # Australia
    [(113, -22), (114, -30), (118, -35), (124, -33), (129, -32), (133, -33),
     (137, -35), (140, -38), (145, -39), (150, -37), (153, -31), (153, -26),
     (150, -22), (146, -19), (142, -11), (140, -14), (136, -15), (132, -12),
     (129, -14), (125, -16), (121, -19), (116, -21), (113, -22)],
    # New Zealand
    [(167, -45), (170, -41), (174, -39), (177, -38), (175, -41), (171, -43),
     (168, -46), (167, -45)],
    # Japan
    [(130, 31), (133, 33), (136, 35), (139, 36), (141, 39), (142, 43),
     (144, 44), (142, 41), (140, 37), (137, 34), (133, 32), (130, 31)],
    # United Kingdom
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (0, 55), (1, 51), (-2, 50),
     (-5, 50)],
    # Madagascar
    [(44, -16), (48, -15), (50, -17), (49, -21), (47, -24), (44, -25),
     (43, -21), (44, -16)],
]


def draw_map(d, x0, y0, w, h):
    """World map: pale sea, warm sand land, graticule, 13 numbered pins
    with leader lines (greedy offset placement, deterministic)."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=SEA)
    lat_top, lat_bot = 83.0, -57.0

    def proj(lon, lat):
        px = x0 + (lon + 180.0) / 360.0 * w
        py = y0 + (lat_top - lat) / (lat_top - lat_bot) * h
        return (px, py)

    for poly in CONTINENTS:
        pts = [proj(lon, lat) for (lon, lat) in poly]
        d.polygon(pts, fill=LAND, outline=LAND_LINE)
    for lon in range(-150, 181, 30):
        px = x0 + (lon + 180.0) / 360.0 * w
        d.line([px, y0, px, y0 + h], fill=(200, 210, 216), width=1)
    for lat in [60, 30, 0, -30]:
        py = y0 + (lat_top - lat) / (lat_top - lat_bot) * h
        d.line([x0, py, x0 + w, py], fill=(200, 210, 216), width=1)
    # pins: small red dot at the exact place, numbered badge offset with
    # a leader line so crowded Europe/Middle East pins never stack.
    f = f_sans_b(9)
    OFFSETS = [(0, -17), (15, -13), (-15, -13), (17, 0), (-17, 0),
               (15, 13), (-15, 13), (0, 17), (25, -7), (-25, -7),
               (25, 9), (-25, 9), (0, -25), (32, 0), (-32, 0)]
    placed = []
    for i, st in enumerate(ILLUSTRATED):
        lon, lat = PIN[st["id"]]
        px, py = proj(lon, lat)
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED,
                  outline=WHITE, width=1)
        chosen = None
        for dx, dy in OFFSETS:
            bx, by = px + dx, py + dy
            if bx < x0 + 9 or bx > x0 + w - 9 or by < y0 + 9 or by > y0 + h - 9:
                continue
            if all((bx - cx) ** 2 + (by - cy) ** 2 >= 16 ** 2
                   for cx, cy in placed):
                chosen = (bx, by)
                break
        if chosen is None:
            chosen = (px, py - 17)
        bx, by = chosen
        placed.append((bx, by))
        d.line([px, py, bx, by], fill=(120, 110, 90), width=1)
        d.ellipse([bx - 7, by - 7, bx + 7, by + 7], fill=RED,
                  outline=WHITE, width=1)
        tw = d.textlength(str(i + 1), font=f)
        d.text((bx - tw / 2, by - 6), str(i + 1), font=f, fill=WHITE)


# ---- page -----------------------------------------------------------------
def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    x = MARGIN
    y = 0

    # ---- top bar (0-56): masthead left, date right ----
    f_date, _ = fit_font(d, "SUNDAY 22 NOVEMBER 2026", "DejaVuSans-Bold.ttf",
                         28, 430)
    dw = d.textlength("SUNDAY 22 NOVEMBER 2026", font=f_date)
    f_mast, _ = fit_font(d, "THE WORLD IN ONE DAY", "DejaVuSerif-Bold.ttf",
                         44, CW - dw - 24)
    d.text((x, y + 2), "THE WORLD IN ONE DAY", font=f_mast, fill=NAVY)
    d.text((x + CW - dw, y + 2), "SUNDAY 22 NOVEMBER 2026", font=f_date,
           fill=NAVY)
    f_wires = f_sans(10)
    wires = "WIRES READ TO 23:59 UTC  \u00b7  36 STORIES  \u00b7  7 REGIONS"
    ww = d.textlength(wires, font=f_wires)
    d.text((x + CW - ww, y + 34), wires, font=f_wires, fill=GREY)
    d.line([x, y + 54, x + CW, y + 54], fill=GOLD, width=2)
    y += 56

    # ---- sub-headline (56-88): red serif, one line ----
    sub = ("COP31 collapses without a deal  \u00b7  Kyiv hit by 186 drones  "
           "\u00b7  Verstappen wins in Las Vegas")
    f_sub, _ = fit_font(d, sub, "DejaVuSerif-Bold.ttf", 15, CW)
    d.text((x, y + 7), sub, font=f_sub, fill=RED)
    d.line([x, y + 30, x + CW, y + 30], fill=RULE, width=1)
    y += 32

    # ---- stats strip (88-132): 6 consensus numbers ----
    stats = [(s["value"], s["label"]) for s in V2["stats_strip"]]
    d.rectangle([x, y, x + CW, y + 44], fill=PANEL, outline=GOLD)
    colw = CW / 6.0
    for i, (num, lab) in enumerate(stats):
        cx = x + colw * i
        fn = f_sans_b(22)
        nw = d.textlength(num, font=fn)
        d.text((cx + (colw - nw) / 2, y + 2), num, font=fn, fill=NAVY)
        fl = f_sans_b(9)
        for li, ln in enumerate(wrap(d, lab, fl, colw - 12)):
            lw = d.textlength(ln, font=fl)
            d.text((cx + (colw - lw) / 2, y + 28 + li * 10), ln, font=fl,
                   fill=GREY)
        if i:
            d.line([cx, y + 5, cx, y + 39], fill=RULE, width=1)
    y += 44

    # ---- hero row (132-374): 3 EQUAL cards ----
    hero_w = 326
    hero_h = 242
    hero_gap = 7
    hero_y = y
    ill_h = 120
    for hi, st in enumerate(HEROES):
        hx = x + hi * (hero_w + hero_gap)
        d.rectangle([hx, hero_y, hx + hero_w, hero_y + hero_h], fill=PANEL,
                    outline=RULE)
        if st["id"] == "v2-01":
            draw_kyiv(d, hx + 1, hero_y + 1, hero_w - 2, ill_h)
        elif st["id"] == "v2-02":
            draw_cop31(d, hx + 1, hero_y + 1, hero_w - 2, ill_h)
        else:
            draw_f1(d, hx + 1, hero_y + 1, hero_w - 2, ill_h)
        d.rectangle([hx + 1, hero_y + ill_h + 1, hx + hero_w - 1,
                     hero_y + ill_h + 3], fill=GOLD)
        tx = hx + 10
        ty = hero_y + ill_h + 8
        d.text((tx, ty), "%d  \u00b7  %s" % (hi + 1, HERO_LOC[st["id"]]),
               font=f_sans_b(9), fill=RED)
        ty += 13
        ht = f_serif_b(20)
        for ln in wrap(d, st["title"], ht, hero_w - 20)[:2]:
            d.text((tx, ty), ln, font=ht, fill=NAVY)
            ty += 23
        hs = f_sans(12)
        summ = HERO_SUMM.get(st["id"], st["summary"])
        for ln in wrap(d, summ, hs, hero_w - 20)[:2]:
            d.text((tx, ty), ln, font=hs, fill=INK)
            ty += 15
        d.text((tx, hero_y + hero_h - 14), st["source"].upper(),
               font=f_sans_b(9), fill=GREY)
    y += hero_h

    # ---- map + timeline band (382-622) ----
    band_y = y
    band_h = 240
    map_w = 552
    tl_x = x + map_w + 8
    tl_w = CW - map_w - 8
    # map panel
    d.rectangle([x, band_y, x + map_w, band_y + band_h], fill=PANEL,
                outline=RULE)
    d.text((x + 8, band_y + 5), "WHERE THE DAY HAPPENED \u2014 13 STORIES MAPPED",
           font=f_sans_b(10), fill=NAVY)
    d.text((x + 8, band_y + 18), "Pins match story numbers 1\u201313",
           font=f_sans(9), fill=GREY)
    draw_map(d, x + 6, band_y + 34, map_w - 12, band_h - 40)
    # timeline panel
    d.rectangle([tl_x, band_y, tl_x + tl_w, band_y + band_h], fill=PANEL,
                outline=RULE)
    d.text((tl_x + 8, band_y + 5), "THE DAY IN UTC", font=f_sans_b(12),
           fill=NAVY)
    d.line([tl_x + 8, band_y + 22, tl_x + tl_w - 8, band_y + 22], fill=RULE,
           width=1)
    tl = V2["timeline_utc"]
    ty = band_y + 28
    ft = f_sans_b(11)
    ftx = f_sans(11)
    for ev in tl:
        tm = ev["time"]
        lines = wrap(d, ev["text"], ftx, tl_w - 16 - 46)
        d.text((tl_x + 8, ty), tm, font=ft, fill=RED)
        d.ellipse([tl_x + 46 - 3, ty + 4, tl_x + 46 + 3, ty + 10], fill=GOLD)
        ly = ty
        for ln in lines[:2]:
            d.text((tl_x + 54, ly), ln, font=ftx, fill=INK)
            ly += 13
        ty = ly + 4
        if ty > band_y + band_h - 16:
            break
    y += band_h

    # ---- 10 medium cards (614-782): 2 rows x 5 ----
    gap = 5
    card_w = 194
    card_h = 82
    for row in range(2):
        for col in range(5):
            idx = row * 5 + col
            st = MEDIUM[idx]
            cx0 = x + col * (card_w + gap)
            cy0 = y + row * (card_h + 4)
            d.rectangle([cx0, cy0, cx0 + card_w, cy0 + card_h], fill=PANEL,
                        outline=RULE)
            d.rectangle([cx0, cy0, cx0 + card_w, cy0 + 2], fill=GOLD)
            tx = cx0 + 6
            ty = cy0 + 5
            d.text((tx, ty), "%d  \u00b7  %s" % (idx + 4,
                   REGION_LABEL[st["region"]]), font=f_sans_b(9), fill=RED)
            ty += 12
            tt = f_sans_b(13)
            for ln in wrap(d, st["title"], tt, card_w - 12)[:2]:
                d.text((tx, ty), ln, font=tt, fill=NAVY)
                ty += 14
            ts = f_sans(11)
            summ = MED_SUMM[st["id"]]
            for ln in wrap(d, summ, ts, card_w - 12)[:2]:
                d.text((tx, ty), ln, font=ts, fill=GREY)
                ty += 12
            d.text((tx, ty + 2), st["source"].upper(),
                   font=f_sans_b(9), fill=GREY)
    y += 2 * card_h + 4

    # ---- ALSO ON (782-926): 23 rows, 3 columns ----
    also_y = y
    d.text((x, also_y), "ALSO ON \u2014 SUNDAY 22 NOVEMBER",
           font=f_sans_b(11), fill=NAVY)
    d.line([x + 240, also_y + 7, x + CW, also_y + 7], fill=RED, width=2)
    col_w = CW // 3
    f_item = f_sans(12)
    f_num = f_sans_b(12)
    f_src = f_sans(10)
    for i, st in enumerate(ALSO):
        col = i // 8
        r = i % 8
        ix = x + col * col_w
        iy = also_y + 20 + r * 16
        short, src = ALSO_SHORT[st["id"]]
        num = str(i + 14)
        d.text((ix, iy), num, font=f_num, fill=RED)
        nx = ix + d.textlength("36  ", font=f_num)
        d.text((nx, iy), short, font=f_item, fill=INK)
        sx = nx + d.textlength(short + " ", font=f_item)
        d.text((sx, iy + 2), "(" + src + ")", font=f_src, fill=GREY)
    y = also_y + 20 + 8 * 16

    # ---- DATE CHECK (926-1000): red frame, exact text ----
    dc_y = y
    dc_h = 1000 - dc_y
    d.rectangle([x, dc_y, x + CW, dc_y + dc_h], fill=DC_BG, outline=RED,
                width=2)
    dc_text = V2["date_check"]
    # The data text already opens with "DATE CHECK — "; the red label
    # above carries it, so strip the prefix to avoid printing it twice.
    if dc_text.startswith("DATE CHECK"):
        dc_text = dc_text.split("\u2014", 1)[1].strip()
    # largest size (10.5 -> 9) whose wrap fits the box
    chosen = None
    for size in (10.5, 10, 9.5, 9):
        f_dc = f_sans(size)
        lines = wrap(d, dc_text, f_dc, CW - 24)
        if len(lines) <= 5:
            chosen = (f_dc, lines, size)
            break
    if chosen is None:
        f_dc = f_sans(9)
        lines = wrap(d, dc_text, f_dc, CW - 24)
        chosen = (f_dc, lines, 9)
    f_dc, lines, dc_size = chosen
    d.text((x + 10, dc_y + 6), "DATE CHECK", font=f_sans_b(11), fill=RED)
    ly = dc_y + 6
    for ln in lines:
        d.text((x + 10, ly + 14), ln, font=f_dc, fill=INK)
        ly += 12
    y = dc_y + dc_h

    # ---- footer (1000-1024): sources + bounty line, 2 lines ----
    d.line([x, y + 2, x + CW, y + 2], fill=NAVY, width=1)
    f_ft = f_sans(9)
    foot = ("Sources: AP \u00b7 Reuters \u00b7 AFP \u00b7 BBC \u00b7 The Guardian "
            "\u00b7 SCMP \u00b7 Cricinfo \u00b7 Formula1.com \u00b7 ATP Tour "
            "\u00b7 Vatican News \u00b7 Radio Dabanga \u00b7 Eye Radio "
            "\u00b7 EIN Presswire \u00b7 Sydney Morning Herald \u00b7 ABC "
            "\u00b7 LiveScore. Built by an AI agent for make.fun's "
            "\u201cSum up 22 November's world news in one image\u201d bounty.")
    fy = y + 4
    for ln in wrap(d, foot, f_ft, CW):
        d.text((x, fy), ln, font=f_ft, fill=GREY)
        fy += 10

    out = os.path.join(BASE, "entry.png")
    img.save(out, format="PNG", optimize=True)
    data = open(out, "rb").read()
    print("entry.png bytes:", len(data))
    print("entry.png sha256:", hashlib.sha256(data).hexdigest())
    print("stories used:", len(STORIES))
    print("date-check font size:", dc_size, "lines:", len(lines))
    print("final y (footer bottom):", fy, "of", H)


if __name__ == "__main__":
    render()
