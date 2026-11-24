#!/usr/bin/env python3
"""draw.py — Treasure map of the Isle of the Gilded Gull (fictional island).

Draws a 1024x1024 vintage ink-on-parchment treasure map with a fictional
island, 9 legible labeled places, compass rose, dashed route to a red X,
sea monster, ship, mountains and palm forest. Deterministic: fixed fonts,
fixed coordinates, no clock, no randomness — two runs are byte-identical.

Output: entry.png in MAKEFUN_OUTPUT_DIR when set (the grader's repo is
read-only), else next to this file.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR") or os.path.dirname(os.path.abspath(__file__)), "entry.png")

# --- palette (vintage parchment, ink, red accent) ---
PARCHMENT = (242, 230, 196)
PARCHMENT_DARK = (228, 212, 168)
SEA = (203, 222, 211)
SEA_DEEP = (178, 205, 196)
LAND = (236, 217, 160)
LAND_EDGE = (214, 190, 128)
FOREST = (122, 154, 90)
FOREST_DARK = (94, 124, 66)
INK = (58, 42, 26)
INK_SOFT = (96, 74, 48)
RED = (168, 60, 42)
RED_DARK = (140, 44, 30)
GOLD = (184, 138, 44)
MOUNTAIN = (150, 138, 118)
SNOW = (250, 248, 240)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_TITLE = font("DejaVuSerif-Bold.ttf", 40)
F_TITLE_SMALL = font("DejaVuSerif-Bold.ttf", 30)
F_LABEL = font("DejaVuSerif-Bold.ttf", 24)
F_LABEL_SM = font("DejaVuSerif-Bold.ttf", 20)
F_NOTE = font("DejaVuSerif.ttf", 18)
F_SMALL = font("DejaVuSerif.ttf", 15)

img = Image.new("RGB", (W, H), PARCHMENT)
d = ImageDraw.Draw(img)

# --- aging stains (fixed soft ellipses, deterministic) ---
for (x0, y0, x1, y1, col) in [
    (60, 820, 300, 980, PARCHMENT_DARK),
    (760, 60, 980, 240, PARCHMENT_DARK),
    (820, 760, 990, 950, PARCHMENT_DARK),
    (40, 60, 220, 220, PARCHMENT_DARK),
]:
    d.ellipse([x0, y0, x1, y1], fill=col)

# --- sea (pale wash inside the double border) ---
d.rectangle([34, 34, 990, 990], fill=SEA)
# a few deeper sea patches
d.ellipse([70, 120, 260, 260], fill=SEA_DEEP)
d.ellipse([780, 700, 960, 880], fill=SEA_DEEP)
d.ellipse([700, 90, 880, 200], fill=SEA_DEEP)

# --- wave squiggles (fixed positions) ---
for (x, y, s) in [
    (120, 340, 26), (180, 420, 22), (110, 640, 24), (160, 760, 20),
    (850, 300, 24), (900, 480, 22), (830, 620, 26), (120, 180, 20),
    (880, 180, 20), (700, 900, 24), (300, 920, 22), (900, 880, 20),
]:
    d.arc([x, y, x + s, y + s // 2], 180, 360, fill=INK_SOFT, width=2)
    d.arc([x + s // 2, y + s // 4, x + s, y + s // 2 + s // 4], 180, 360, fill=INK_SOFT, width=2)

# --- the island (fictional, irregular coastline) ---
ISLAND = [
    (430, 260), (520, 280), (600, 250), (680, 300), (740, 360),
    (770, 450), (720, 520), (760, 600), (700, 680), (640, 760),
    (560, 800), (470, 780), (380, 800), (300, 740), (240, 660),
    (200, 560), (230, 460), (280, 380), (340, 300), (380, 280),
]
d.polygon(ISLAND, fill=LAND, outline=INK, width=4)
# beach ring (inner coastline)
d.polygon(ISLAND, outline=LAND_EDGE, width=10)
d.polygon(ISLAND, outline=INK, width=2)

# --- palm forest (east) ---
def palm(x, y, s=1.0):
    # trunk
    d.line([(x, y), (x + 4 * s, y - 22 * s)], fill=INK_SOFT, width=3)
    # fronds
    for dx, dy in [(-16, -26), (-8, -32), (4, -34), (14, -30), (20, -22)]:
        d.arc([x + dx * s - 6, y - 34 * s, x + dx * s + 10, y - 18 * s],
              200, 340, fill=FOREST_DARK, width=3)
    d.ellipse([x - 3, y - 6, x + 7, y + 2], fill=FOREST_DARK)

for (x, y, s) in [
    (640, 560, 1.0), (680, 600, 0.9), (620, 620, 1.1), (700, 540, 0.8),
    (660, 660, 1.0), (610, 690, 0.9), (720, 630, 1.0), (640, 720, 0.8),
]:
    palm(x, y, s)

# --- mountains (north) ---
def mountain(x, y, w, h):
    d.polygon([(x - w, y), (x, y - h), (x + w, y)], fill=MOUNTAIN, outline=INK, width=2)
    d.polygon([(x - w // 3, y - h * 2 // 3), (x, y - h), (x + w // 3, y - h * 2 // 3)],
              fill=SNOW, outline=INK, width=1)

mountain(440, 380, 55, 70)
mountain(530, 360, 65, 85)
mountain(620, 385, 50, 60)

# --- harbor (south): small jetty + anchor ---
d.line([(500, 795), (500, 830)], fill=INK, width=4)
d.line([(470, 830), (530, 830)], fill=INK, width=4)
d.arc([485, 815, 515, 845], 0, 180, fill=INK, width=3)

# --- ship (southwest sea) ---
def ship(cx, cy, s=1.0):
    # hull
    d.polygon([(cx - 42 * s, cy), (cx + 42 * s, cy), (cx + 30 * s, cy + 16 * s),
               (cx - 30 * s, cy + 16 * s)], fill=(122, 84, 50), outline=INK, width=2)
    # masts + sails
    d.line([(cx, cy), (cx, cy - 52 * s)], fill=INK, width=3)
    d.line([(cx - 22 * s, cy - 8 * s), (cx - 22 * s, cy - 40 * s)], fill=INK, width=2)
    d.polygon([(cx + 2, cy - 50 * s), (cx + 2, cy - 12 * s), (cx + 34 * s, cy - 12 * s)],
              fill=PARCHMENT, outline=INK, width=2)
    d.polygon([(cx - 4, cy - 38 * s), (cx - 4, cy - 10 * s), (cx - 24 * s, cy - 10 * s)],
              fill=PARCHMENT, outline=INK, width=2)
    # flag
    d.polygon([(cx, cy - 52 * s), (cx + 18 * s, cy - 47 * s), (cx, cy - 42 * s)],
              fill=RED, outline=INK, width=1)

ship(150, 700, 1.0)

# --- small fish near the ship ---
def fish(x, y, s=1.0):
    d.ellipse([x, y, x + 22 * s, y + 10 * s], outline=INK_SOFT, width=2)
    d.polygon([(x + 22 * s, y + 5 * s), (x + 32 * s, y - 3 * s), (x + 32 * s, y + 13 * s)],
              outline=INK_SOFT, width=2)
    d.ellipse([x + 4, y + 3, x + 7, y + 6], fill=INK_SOFT)

fish(210, 640, 0.9)
fish(90, 780, 1.1)
fish(250, 780, 0.8)

# --- sea monster (southeast sea) ---
def sea_monster(cx, cy, s=1.0):
    # humps
    for i, (hx, hy) in enumerate([(cx - 50, cy), (cx, cy - 12), (cx + 50, cy)]):
        d.arc([hx - 26 * s, hy - 22 * s, hx + 26 * s, hy + 22 * s], 180, 360,
              fill=INK, width=4)
    # head + neck
    d.line([(cx + 50, cy), (cx + 78, cy - 38 * s)], fill=INK, width=5)
    d.ellipse([cx + 68, cy - 52 * s, cx + 92, cy - 30 * s], fill=SEA_DEEP, outline=INK, width=3)
    d.ellipse([cx + 82, cy - 48 * s, cx + 88, cy - 42 * s], fill=INK)
    # spines
    for i in range(3):
        d.line([(cx + 60 + i * 8, cy - 34 * s - i * 4), (cx + 60 + i * 8, cy - 44 * s - i * 4)],
               fill=INK, width=2)

sea_monster(860, 780, 1.0)

# --- dashed treasure route: harbor -> X ---
ROUTE = [(500, 790), (470, 720), (430, 660), (470, 590), (540, 540), (590, 480), (620, 440)]
def dashed(points, dash=10, gap=7):
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        import math
        dist = math.hypot(x1 - x0, y1 - y0)
        n = int(dist / (dash + gap))
        for i in range(n + 1):
            t0 = i * (dash + gap) / dist
            t1 = min((i * (dash + gap) + dash) / dist, 1.0)
            if t0 >= 1.0:
                break
            d.line([(x0 + (x1 - x0) * t0, y0 + (y1 - y0) * t0),
                    (x0 + (x1 - x0) * t1, y0 + (y1 - y0) * t1)],
                   fill=RED_DARK, width=3)

dashed(ROUTE)

# --- the X (treasure) ---
X, Y = 620, 430
d.line([(X - 26, Y - 26), (X + 26, Y + 26)], fill=RED, width=7)
d.line([(X - 26, Y + 26), (X + 26, Y - 26)], fill=RED, width=7)
d.line([(X - 26, Y - 26), (X + 26, Y + 26)], fill=RED_DARK, width=3)
d.line([(X - 26, Y + 26), (X + 26, Y - 26)], fill=RED_DARK, width=3)
# small chest beside the X
d.rectangle([X + 34, Y + 6, X + 62, Y + 28], fill=GOLD, outline=INK, width=2)
d.line([(X + 34, Y + 14), (X + 62, Y + 14)], fill=INK, width=2)
d.ellipse([X + 44, Y + 14, X + 52, Y + 22], fill=INK)

# --- compass rose (top right) ---
CX, CY, R = 868, 132, 52
d.ellipse([CX - R, CY - R, CX + R, CY + R], outline=INK, width=2)
d.ellipse([CX - R + 8, CY - R + 8, CX + R - 8, CY + R - 8], outline=INK_SOFT, width=1)
for ang, ln, col, w in [(0, R - 6, RED, 5), (90, R - 6, INK, 5), (180, R - 6, INK, 5),
                        (270, R - 6, INK, 5), (45, R - 22, INK_SOFT, 3),
                        (135, R - 22, INK_SOFT, 3), (225, R - 22, INK_SOFT, 3),
                        (315, R - 22, INK_SOFT, 3)]:
    import math
    a = math.radians(ang - 90)
    d.line([(CX, CY), (CX + ln * math.cos(a), CY + ln * math.sin(a))], fill=col, width=w)
d.ellipse([CX - 7, CY - 7, CX + 7, CY + 7], fill=GOLD, outline=INK, width=2)
d.text((CX - 8, CY - R - 26), "N", font=F_LABEL_SM, fill=INK)
d.text((CX + R + 8, CY - 10), "E", font=F_LABEL_SM, fill=INK)
d.text((CX - 8, CY + R + 6), "S", font=F_LABEL_SM, fill=INK)
d.text((CX - R - 24, CY - 10), "W", font=F_LABEL_SM, fill=INK)

# --- title cartouche (top left) ---
d.rounded_rectangle([48, 48, 660, 148], radius=18, fill=PARCHMENT, outline=INK, width=3)
d.rounded_rectangle([56, 56, 652, 140], radius=14, outline=INK_SOFT, width=1)
d.text((76, 58), "THE ISLE OF", font=F_LABEL, fill=INK_SOFT)
d.text((76, 90), "THE GILDED GULL", font=F_TITLE_SMALL, fill=INK)

# --- labels (parchment stroke halo for legibility) ---
def label(xy, text, fnt=F_LABEL, fill=INK):
    d.text(xy, text, font=fnt, fill=fill, stroke_width=3, stroke_fill=PARCHMENT)

label((330, 396), "MT. CROW'S NEST", F_LABEL_SM)
label((575, 730), "WHISPERING", F_LABEL_SM)
label((615, 756), "PALMS", F_LABEL_SM)
label((248, 500), "DEAD MAN'S", F_LABEL_SM)
label((248, 526), "COVE", F_LABEL_SM)
label((400, 852), "GULL'S REST", F_LABEL)
label((648, 396), "THE BURIED", F_LABEL_SM)
label((648, 422), "CHEST", F_LABEL_SM)
label((60, 730), "WRECK OF THE", F_LABEL_SM)
label((60, 756), "SALTY MAID", F_LABEL_SM)
label((770, 700), "KRAKEN'S", F_LABEL_SM)
label((770, 726), "DEEP", F_LABEL_SM)
d.text((740, 830), "HERE BE MONSTERS", font=F_NOTE, fill=INK_SOFT,
       stroke_width=2, stroke_fill=PARCHMENT)

# --- scale bar (bottom left) ---
d.text((60, 900), "0", font=F_SMALL, fill=INK)
for i, col in enumerate([INK, PARCHMENT, INK, PARCHMENT]):
    d.rectangle([110 + i * 40, 906, 150 + i * 40, 918], fill=col, outline=INK, width=1)
d.text((280, 900), "5", font=F_SMALL, fill=INK)
d.text((110, 926), "LEAGUES", font=F_SMALL, fill=INK)
d.text((110, 946), "1 league = 3 miles, more or less", font=F_SMALL, fill=INK_SOFT)

# --- decorative double border ---
d.rectangle([18, 18, 1006, 1006], outline=INK, width=3)
d.rectangle([30, 30, 994, 994], outline=INK_SOFT, width=1)

img.save(OUT, "PNG", optimize=True)
print(f"saved {OUT} ({os.path.getsize(OUT)} bytes)")
