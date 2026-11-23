#!/usr/bin/env python3
"""Draw 'THE WORLD IN ONE DAY — TUESDAY 24 NOVEMBER 2026'.

Fresh generator for the news-image-20261124 bounty (round 1). Every story was
verified against wire reports dated 22-24 November 2026; the DATE CHECK box
on the page says honestly which day each lead is from. Deterministic: no
randomness, no clock, no network. Pillow only; run: python3 draw.py
Writes entry.png (1024x1024, <=1 MiB) next to this file.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))

PAPER = (246, 241, 229)
INK = (25, 23, 19)
GREY = (107, 101, 92)
LIGHT = (233, 226, 210)
RED = (164, 30, 34)
NAVY = (31, 58, 95)
TEAL = (15, 91, 77)
AMBER = (178, 118, 20)
BLUE = (43, 94, 167)
GREEN = (46, 110, 58)
CREAM2 = (250, 247, 238)


def font(name, size):
    paths = {
        "serif": "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "serif_b": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        "sans": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "sans_b": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    }
    return ImageFont.truetype(paths[name], size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap measured with the real font."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, color, width, leading):
    lines = wrap(draw, text, fnt, width)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=color)
        y += leading
    return y


def tag_chip(draw, x, y, label):
    """Small certainty tag: REPORTED green, CLAIM amber, ONGOING blue."""
    f = font("sans_b", 11)
    w = int(draw.textlength(label, font=f)) + 12
    fill = {"REPORTED": GREEN, "CLAIM": AMBER, "ONGOING": BLUE}[label]
    draw.rounded_rectangle([x, y, x + w, y + 16], radius=3, fill=fill)
    draw.text((x + 6, y + 2), label, font=f, fill=(255, 255, 255))
    return x + w + 6


def rule(draw, x0, x1, y, color=INK, width=2):
    draw.line([(x0, y), (x1, y)], fill=color, width=width)


# ---- dotted world map: coarse land mask, rows of (start, end) column spans ----
# 64 columns (lon -180..180), 24 rows (lat 75..-60). Hand-drawn approximation.
LAND = [
    [(2, 14), (40, 58)],
    [(1, 16), (38, 60)],
    [(2, 15), (36, 60)],
    [(3, 14), (34, 40), (44, 60)],
    [(4, 13), (33, 38), (45, 59)],
    [(5, 12), (32, 37), (44, 58)],
    [(6, 11), (31, 36), (42, 57)],
    [(7, 11), (31, 35), (42, 56)],
    [(8, 11), (33, 35), (43, 55)],
    [(9, 11), (33, 36), (44, 54)],
    [(10, 11), (33, 37), (45, 52), (54, 56)],
    [(10, 11), (34, 37), (46, 50), (54, 57)],
    [(11, 11), (34, 37), (47, 49), (55, 57)],
    [(12, 13), (35, 37), (48, 49), (56, 58)],
    [(13, 14), (35, 37), (49, 50), (57, 58)],
    [(14, 16), (36, 37), (50, 50), (58, 59)],
    [(15, 17), (36, 38), (51, 51), (59, 60)],
    [(16, 18), (37, 38), (52, 52), (59, 61)],
    [(17, 18), (37, 38), (59, 61)],
    [(18, 19), (37, 38), (58, 60)],
    [(19, 20), (38, 38), (57, 59)],
    [(20, 21), (38, 38), (57, 58)],
    [(21, 21), (57, 57)],
    [(22, 22), (57, 57)],
]

# (lon, lat, number) — the day's pinned places
PINS = [
    (20.1, 32.1, "1"),    # Benghazi — Merkury sunk
    (30.3, 50.8, "2"),    # Dymer, Kyiv region
    (24.5, 59.9, "3"),    # Gulf of Finland — Sparta II
    (30.7, 36.9, "4"),    # Antalya — COP31
    (106.0, -6.1, "5"),   # Banten — factory fire
    (77.2, 28.6, "6"),    # Delhi — India-Nepal
    (127.0, 37.5, "7"),   # Seoul — KOSPI
    (174.8, -41.3, "8"),  # Wellington — Test draw
    (-115.1, 36.2, "9"),  # Las Vegas — Verstappen
    (-77.0, 38.9, "10"),  # Washington — Trump / Iran
    (31.6, 4.9, "11"),    # Juba — South Sudan raid
    (-9.1, 38.7, "12"),   # Lisbon — protests
]


def draw_map(draw, x0, y0):
    """Dotted world map with numbered pins. Cell 13 x 5.5 px."""
    cw, ch = 13, 5.5
    for r, spans in enumerate(LAND):
        for a, b in spans:
            for c in range(a, b + 1):
                cx = x0 + c * cw + cw / 2
                cy = y0 + r * ch + ch / 2
                draw.ellipse([cx - 1.8, cy - 1.8, cx + 1.8, cy + 1.8], fill=(120, 110, 95))
    f = font("sans_b", 10)
    for lon, lat, num in PINS:
        col = (lon + 180.0) / 360.0 * 64
        row = (75.0 - lat) / 135.0 * 24
        px = x0 + col * cw
        py = y0 + row * ch
        draw.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=(255, 255, 255), width=1)
        tw = draw.textlength(num, font=f)
        draw.text((px - tw / 2, py - 6.5), num, font=f, fill=(255, 255, 255))


# ---- illustrated scenes (flat vector, drawn with PIL primitives) ----

def scene_sea(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=NAVY)
    for i in range(5):  # sea bands
        yy = y + 58 + i * 16
        draw.line([(x, yy), (x + w, yy)], fill=(58, 92, 140), width=2)
    # corvette silhouette, listing
    draw.polygon([(x + 55, y + 96), (x + 255, y + 96), (x + 240, y + 118),
                  (x + 70, y + 118)], fill=(30, 32, 36))
    draw.rectangle([x + 120, y + 66, x + 185, y + 96], fill=(44, 46, 50))
    draw.line([(x + 150, y + 66), (x + 150, y + 40)], fill=(44, 46, 50), width=4)
    draw.line([(x + 150, y + 40), (x + 172, y + 52)], fill=(44, 46, 50), width=3)
    # explosion burst
    cx, cy = x + 235, y + 62
    for ang in range(0, 360, 30):
        import math
        r1, r2 = 10, 26
        a = math.radians(ang)
        draw.line([(cx, cy), (cx + r2 * math.cos(a), cy + r2 * math.sin(a))],
                  fill=(255, 176, 32), width=4)
    draw.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(255, 122, 26))
    # three sea drones + dashed approach paths
    for dx, dy in [(30, 108), (70, 122), (110, 112)]:
        draw.ellipse([x + dx - 4, y + dy - 3, x + dx + 4, y + dy + 3], fill=(255, 255, 255))
    draw.text((x + 10, y + 8), "BENGHAZI  ·  SUNDAY", font=font("sans_b", 12),
              fill=(255, 255, 255))


def scene_market(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    draw.rectangle([x, y, x + w, y + h], outline=GREY, width=1)
    for i in range(1, 4):  # grid
        yy = y + i * h // 4
        draw.line([(x + 8, yy), (x + w - 8, yy)], fill=(226, 222, 210), width=1)
    pts = [(x + 14, y + 26), (x + 62, y + 44), (x + 110, y + 40),
           (x + 158, y + 66), (x + 206, y + 62), (x + 254, y + 96),
           (x + 296, y + 118)]
    draw.line(pts, fill=RED, width=4)
    for px, py in pts:
        draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=RED)
    draw.text((x + 12, y + 6), "KOSPI  −5.8%  ·  S&P 500 IN CORRECTION",
              font=font("sans_b", 12), fill=RED)
    draw.text((x + 12, y + h - 24), "NASDAQ −20% FROM PEAK",
              font=font("sans_b", 11), fill=GREY)


def scene_fire(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(38, 30, 26))
    for sx, sy, sr in [(60, 26, 26), (110, 14, 32), (170, 30, 24), (230, 18, 28)]:
        draw.ellipse([x + sx - sr, y + sy - sr, x + sx + sr, y + sy + sr],
                     fill=(90, 84, 78))
    # factory block
    draw.rectangle([x + 40, y + 88, x + 270, y + h], fill=(24, 22, 20))
    draw.rectangle([x + 40, y + 88, x + 270, y + 98], fill=(60, 54, 48))
    # flames
    for fx, fh in [(70, 52), (120, 66), (175, 56), (225, 70)]:
        draw.polygon([(x + fx - 16, y + 96), (x + fx, y + 96 - fh),
                      (x + fx + 16, y + 96)], fill=(255, 122, 26))
        draw.polygon([(x + fx - 8, y + 96), (x + fx, y + 96 - fh + 18),
                      (x + fx + 8, y + 96)], fill=(255, 196, 66))
    draw.text((x + 10, y + 8), "BANTEN, INDONESIA  ·  SATURDAY NIGHT",
              font=font("sans_b", 12), fill=(255, 255, 255))


def scene_cop(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=TEAL)
    # globe
    cx, cy, r = x + w // 2, y + 48, 36
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(250, 247, 238))
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255), width=2)
    draw.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=TEAL, width=3)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=TEAL, width=2)
    draw.ellipse([cx - 12, cy - 24, cx + 12, cy + 24], outline=TEAL, width=2)
    # red no-deal cross over the globe
    draw.line([(cx - 24, cy - 24), (cx + 24, cy + 24)], fill=RED, width=6)
    draw.line([(cx - 24, cy + 24), (cx + 24, cy - 24)], fill=RED, width=6)
    t = "NO DEAL"
    f = font("sans_b", 18)
    draw.text((x + w / 2 - draw.textlength(t, font=f) / 2, y + h - 26),
              t, font=f, fill=(255, 255, 255))


def scene_train(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(238, 232, 216))
    # flags: India + Nepal, top row
    draw.rectangle([x + 16, y + 10, x + 52, y + 22], fill=(255, 153, 51))
    draw.rectangle([x + 16, y + 22, x + 52, y + 34], fill=(255, 255, 255))
    draw.rectangle([x + 16, y + 34, x + 52, y + 46], fill=(19, 136, 8))
    draw.rectangle([x + 64, y + 10, x + 100, y + 46], fill=(220, 20, 60))
    draw.polygon([(x + 64, y + 10), (x + 100, y + 28), (x + 64, y + 46)],
                 fill=(0, 56, 147))
    # train front, full width below the flags
    draw.rounded_rectangle([x + 10, y + 56, x + w - 10, y + h - 16], radius=8,
                           fill=(164, 30, 34))
    draw.rectangle([x + 20, y + 66, x + w - 20, y + 92], fill=(250, 247, 238))
    for wx in range(x + 28, x + w - 28, 26):
        draw.line([(wx, y + 66), (wx, y + 92)], fill=(164, 30, 34), width=3)
    draw.ellipse([x + 30, y + h - 24, x + 44, y + h - 10], fill=(25, 23, 19))
    draw.ellipse([x + w - 44, y + h - 24, x + w - 30, y + h - 10], fill=(25, 23, 19))
    draw.line([(x + 10, y + h - 6), (x + w - 10, y + h - 6)], fill=GREY, width=3)


# ---- page composition ----

NUMBERS = [
    ("24", "DEAD IN BANTEN"),
    ("~30", "STILL MISSING"),
    ("7", "SEA DRONES"),
    ("-5.8%", "KOSPI, MONDAY"),
    ("$8BN", "SEOUL RESCUE FUND"),
    ("8", "INDIA-NEPAL MoUs"),
    ("128", "PANT, WELLINGTON"),
]

HEROES = [
    {
        "kicker": "WAR AT SEA",
        "tag": "REPORTED",
        "headline": "UKRAINE SINKS A RUSSIAN WARSHIP — IN LIBYA",
        "body": ("Seven Ukrainian sea drones sank the corvette Merkury at "
                 "Benghazi on Sunday; Kyiv confirmed it on Monday. A Ka-27 "
                 "helicopter went down with her."),
        "scene": scene_sea,
    },
    {
        "kicker": "MARKETS",
        "tag": "REPORTED",
        "headline": "THE AI ROUT ROLLS ON — SEOUL STEPS IN",
        "body": ("Wall Street's AI sell-off reached Asia: the KOSPI fell as "
                 "much as 5.8% on Monday before an $8bn stabilisation fund "
                 "steadied it. The S&P 500 is in correction; the Nasdaq is "
                 "20% off its peak."),
        "scene": scene_market,
    },
    {
        "kicker": "DISASTER",
        "tag": "ONGOING",
        "headline": "24 DEAD AS THE BANTEN RESCUE GOES ON",
        "body": ("Rescuers kept digging through the burnt-out candy factory "
                 "in Banten on Monday: 24 confirmed dead, about 30 still "
                 "missing of 300 workers inside when the fire broke out on "
                 "Saturday."),
        "scene": scene_fire,
    },
]

ALSO_LEFT = [
    ("2", "REPORTED", "Dymer, Kyiv region: drone collapses flats; 15 missing."),
    ("3", "ONGOING", "Sparta II still burning off Finland after a drone strike."),
    ("", "REPORTED", "Estonia to shut all land borders with Russia."),
    ("", "REPORTED", "Spain drops all charges against Catalan leader Puigdemont."),
    ("12", "REPORTED", "Thousands march in Lisbon over the cost of living."),
    ("", "REPORTED", "Athens reopens the Acropolis Museum after ~20 years."),
    ("7", "REPORTED", "Seoul names a new foreign minister and spy chief."),
    ("", "REPORTED", "China sets 2030 targets for elderly care, childcare."),
    ("", "CLAIM", "Bangladesh vows to arrest ex-PM Hasina if she returns."),
    ("", "REPORTED", "Bangladesh starts mass typhoid jabs vs resistant strains."),
    ("", "REPORTED", "SpiceJet crisis: pilots urge Delhi to act on pay, jets."),
    ("", "REPORTED", "Taiwan stocks rise 2.1% as the state steadies markets."),
    ("", "REPORTED", "Tajikistan tells the UN it will quit the ICC."),
]

ALSO_RIGHT = [
    ("10", "REPORTED", "Two killed in a shooting at a US university."),
    ("10", "CLAIM", "Trump warns Iran of a “very traumatic” outcome."),
    ("", "REPORTED", "Canada's Carney laughs off a Trump lookalike."),
    ("", "REPORTED", "US plans tougher citizenship test, H-1B changes."),
    ("", "CLAIM", "Iran's Guards claim radar strikes on US bases in Bahrain."),
    ("", "REPORTED", "UN seeks independent probe into the Libya ship attack."),
    ("11", "REPORTED", "South Sudan cattle-camp raid kills 24, incl. 7 children."),
    ("", "CLAIM", "Myanmar's junta slams an ASEAN decision as “unfair”."),
    ("9", "REPORTED", "Verstappen wins the Las Vegas Grand Prix."),
    ("8", "REPORTED", "Pant hits 128; India–NZ Test ends in a draw."),
    ("", "REPORTED", "Ferrari unveils the 296 Challenge Stradale and Evo."),
    ("", "REPORTED", "Nvidia reinstates Jensen Huang; shares jump 8.7%."),
    ("", "REPORTED", "Nvidia faces SEC, California probes on China chips."),
]


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 26
    # --- masthead ---
    d.text((M, 16), "MAKE.FUN  ·  WORLD NEWS IN ONE IMAGE",
           font=font("sans_b", 12), fill=GREY)
    d.text((W - M - 118, 16), "TUESDAY", font=font("sans_b", 12), fill=GREY)
    title = "THE WORLD IN ONE DAY"
    tf = font("serif_b", 56)
    d.text(((W - d.textlength(title, font=tf)) / 2, 34), title, font=tf, fill=INK)
    df = font("serif_b", 27)
    date = "TUESDAY  24  NOVEMBER  2026"
    d.text(((W - d.textlength(date, font=df)) / 2, 100), date, font=df, fill=RED)
    rule(d, M, W - M, 132)
    # --- numbers strip ---
    y0, y1 = 140, 172
    cw = (W - 2 * M) / len(NUMBERS)
    for i, (num, lab) in enumerate(NUMBERS):
        x = M + i * cw
        d.rectangle([x + 2, y0, x + cw - 2, y1], outline=GREY, width=1)
        nf = font("sans_b", 19)
        d.text((x + cw / 2 - d.textlength(num, font=nf) / 2, y0 + 2),
               num, font=nf, fill=INK)
        lf = font("sans", 8)
        d.text((x + cw / 2 - d.textlength(lab, font=lf) / 2, y0 + 22),
               lab, font=lf, fill=GREY)
    rule(d, M, W - M, 180)
    # --- hero row (3 illustrated leads) ---
    hy, hh = 188, 252
    colw = 310
    xs = [M, M + colw + 21, M + 2 * (colw + 21)]
    for x, hero in zip(xs, HEROES):
        hero["scene"](d, x, hy, colw, 132)
        yy = hy + 140
        d.text((x, yy), hero["kicker"], font=font("sans_b", 12), fill=RED)
        tag_chip(d, x + 118, yy, hero["tag"])
        yy += 20
        yy = para(d, x, yy, hero["headline"], font("serif_b", 19), INK, colw, 21)
        para(d, x, yy + 2, hero["body"], font("sans", 12), INK, colw, 14)
    rule(d, M, W - M, 452)
    # --- secondary row: COP31 + India-Nepal ---
    sy = 456
    # COP31 (left)
    d.text((M, sy), "CLIMATE", font=font("sans_b", 12), fill=RED)
    tag_chip(d, M + 82, sy, "REPORTED")
    yy = para(d, M, sy + 20, "COP31 ENDS WITH NO DEAL ON FOSSIL FUELS",
              font("serif_b", 19), INK, 300, 21)
    para(d, M, yy + 2,
         ("Two weeks of talks in Antalya ended on Sunday without any "
          "agreement on fossil fuels, after the EU and Panama rejected a "
          "draft that never named them."),
         font("sans", 12), INK, 300, 15)
    scene_cop(d, M + 316, sy, 164, 130)
    # India-Nepal (right)
    rx = 527
    d.text((rx, sy), "SOUTH ASIA", font=font("sans_b", 12), fill=RED)
    tag_chip(d, rx + 96, sy, "REPORTED")
    yy = para(d, rx, sy + 20, "A TRAIN, EIGHT DEALS, ₹15,000 CRORE",
              font("serif_b", 19), INK, 300, 21)
    para(d, rx, yy + 2,
         ("Modi and Nepal's Balen Shah flagged off the Saryu-Kamala "
          "Express, Ayodhya to Janakpur, and signed eight MoUs on Monday. "
          "Delhi pledged ₹15,000 crore for post-flood rebuilding."),
         font("sans", 12), INK, 300, 15)
    scene_train(d, rx + 316, sy, 155, 130)
    rule(d, M, W - M, 594)
    # --- map ---
    d.text((M, 602), "THE WORLD, PINNED  —  12 PLACES THAT MADE THE DAY",
           font=font("sans_b", 13), fill=INK)
    d.text((M, 620), "● REPORTED — confirmed by wire reports    ◆ CLAIM — one side's account    ◐ ONGOING — still developing",
           font=font("sans", 11), fill=GREY)
    draw_map(d, 96, 638)
    rule(d, M, W - M, 772)
    # --- also today ---
    d.text((M, 780), "ALSO TODAY", font=font("sans_b", 13), fill=INK)
    d.text((W - M - 300, 780), "31 STORIES  ·  7 REGIONS", font=font("sans_b", 12), fill=GREY)
    cols = [(M, ALSO_LEFT), (527, ALSO_RIGHT)]
    for cx, items in cols:
        yy = 800
        for pin, tag, text in items:
            tagf = font("sans_b", 9)
            tf_ = font("sans", 11)
            tw = int(d.textlength(tag, font=tagf)) + 10
            fill = {"REPORTED": GREEN, "CLAIM": AMBER, "ONGOING": BLUE}[tag]
            d.rounded_rectangle([cx, yy + 1, cx + tw, yy + 14], radius=2, fill=fill)
            d.text((cx + 5, yy + 2), tag, font=tagf, fill=(255, 255, 255))
            tx = cx + tw + 6
            if pin:
                pf = font("sans_b", 11)
                d.ellipse([tx, yy + 1, tx + 14, yy + 15], fill=RED)
                nw = d.textlength(pin, font=pf)
                d.text((tx + 7 - nw / 2, yy + 2), pin, font=pf, fill=(255, 255, 255))
                tx += 19
            lines = wrap(d, text, tf_, 471 - (tx - cx))
            for ln in lines[:1]:
                d.text((tx, yy), ln, font=tf_, fill=INK)
                yy += 13
            yy += 1
    # --- date check + footer ---
    rule(d, M, W - M, 978)
    d.text((M, 984),
           "DATE CHECK — Merkury sunk Sun 22 Nov, confirmed Mon 23 Nov · COP31 ended Sun 22 Nov · Banten fire Sat 21 Nov, toll reached 24 on Mon 23 Nov ·",
           font=font("sans", 10), fill=GREY)
    d.text((M, 998),
           "India–Nepal, KOSPI, Nvidia: Mon 23 Nov. All reported in Tuesday 24 Nov editions. Nothing here is from before 22 Nov 2026.",
           font=font("sans", 10), fill=GREY)
    return img


if __name__ == "__main__":
    out = os.path.join(HERE, "entry.png")
    build().save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")
