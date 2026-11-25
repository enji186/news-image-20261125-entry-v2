#!/usr/bin/env python3
"""Draw the make.fun news-image-20261125 entry (v2).

One image summing up the world news of Wednesday 25 November 2026,
in the newspaper style of the 20 November winning entry: masthead,
UTC timeline, numbers strip, three hero stories, a grid of small
tiles, a world map with numbered dots, an ALSO ON list, a DATE CHECK
box and a verification legend.

Everything is drawn with Pillow (rectangles, lines, polygons,
ellipses, text). No network, no randomness, no timestamps: running
the program twice writes byte-identical output.

Usage:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

INK = (17, 17, 17)
PAPER = (247, 243, 232)
RED = (200, 16, 46)
DARK_RED = (160, 10, 35)
BLUE = (31, 78, 121)
GREEN = (30, 122, 52)
ORANGE = (198, 96, 10)
GREY = (110, 110, 110)
LIGHT_LINE = (150, 140, 120)
SEA = (220, 235, 245)
LAND = (232, 220, 192)
NAVY = (16, 28, 52)

SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, f, max_w, max_lines=None):
    """Wrap text to fit max_w; optionally cap the number of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    if max_lines is not None and len(lines) > max_lines:
        lines = lines[:max_lines]
        # Ellipsis on the last line if it was cut.
        while lines and d.textlength(lines[-1] + "...", font=f) > max_w:
            lines[-1] = lines[-1][:-1].rstrip()
        lines[-1] = lines[-1] + "..."
    return lines


def draw_wrapped(d, x, y, text, f, max_w, fill, lh, max_lines=None):
    lines = wrap(d, text, f, max_w, max_lines)
    for i, line in enumerate(lines):
        d.text((x, y + i * lh), line, font=f, fill=fill)
    return y + len(lines) * lh


# ---------------------------------------------------------------- stories

# Verification tags: CONFIRMED = 2+ independent outlets;
# OFFICIAL = on the record; REPORTED = one outlet / claim only.
HEROES = [
    dict(n=1, region="CHINA · SPACE", tag="CONFIRMED", tag_src="REUTERS, XINHUA",
         headline="Shenzhou-24 flies first foreign astronaut to Tiangong",
         summary=("Long March 2F lifts off 08:18 CST; docks 11:56. Pakistani "
                  "Muhammad Zeeshan Ali is the first foreigner aboard China's station."),
         art="rocket"),
    dict(n=2, region="MIDDLE EAST · HORMUZ", tag="REPORTED", tag_src="REUTERS",
         headline="Two tankers hit by mines, on fire in Strait of Hormuz",
         summary=("Fires aboard two Liberia-flagged tankers after early-morning "
                  "blasts; Iran's Guards blame mines. Claims not independently verified."),
         art="sea"),
    dict(n=3, region="MARKETS · ASIA", tag="CONFIRMED", tag_src="REUTERS, AP",
         headline="Asia's AI sell-off: Kospi -6.2%, Nikkei -2.8%",
         summary=("Chip and AI shares plunge on valuation fears; Taiex -4.8%, "
                  "Shanghai -1%. Fresh US tariff threats add to the rout."),
         art="chart"),
]

TILES = [
    dict(n=4, region="YEMEN", tag="CONFIRMED", tag_src="REUTERS",
         headline="Coalition strikes Hodeidah port; Houthis threaten Jeddah",
         summary="Strikes hit Hodeidah, Saada, Amran after a warning; Houthis vow to hit ports.",
         art="hodeidah"),
    dict(n=5, region="SAUDI ARABIA", tag="REPORTED", tag_src="REUTERS, WSJ",
         headline="Houthis claim Riyadh tower strike; 11 hurt",
         summary="Group says it hit the financial district and Ras Tanura; the strike was Tue.",
         art="riyadh"),
    dict(n=6, region="SOUTH KOREA", tag="CONFIRMED", tag_src="KOREA JOONGANG DAILY",
         headline="Seoul subway strike called off at dawn",
         summary="Deal shelves 2,212 job cuts, adds 500 hires, lifts pay 3.5%; Lines 1-8 run.",
         art="seoul"),
    dict(n=7, region="COLOMBIA", tag="CONFIRMED", tag_src="REUTERS, AFP",
         headline="Cartagena supermarket siege ends; all hostages freed",
         summary="Forces storm the Exito store at ~01:00; one gunman killed, four detained.",
         art="cartagena"),
    dict(n=8, region="SPORT · AFRICA", tag="CONFIRMED", tag_src="AP, SUPERSPORT",
         headline="CAS restores Senegal as AFCON champions",
         summary="Court overturns the forfeit ruling; Senegal keep the title.",
         art="afcon"),
    dict(n=9, region="PACIFIC", tag="OFFICIAL", tag_src="PM.GOV.AU",
         headline="Australia-Solomons pact blocks foreign bases",
         summary="Canberra treaty bars foreign military bases; Honiara scraps its China pact.",
         art="treaty"),
    dict(n=10, region="INDONESIA", tag="CONFIRMED", tag_src="REUTERS, AP",
         headline="Three bodies found in flooded Bogor gold mine",
         summary="Three dead found in an illegal mine swamped by floodwater; 26 still trapped.",
         art="mine"),
    dict(n=11, region="SUDAN", tag="CONFIRMED", tag_src="RELIEFWEB, DABANGA",
         headline="UN condemns Khartoum strikes; Ethiopia offers talks",
         summary="Aid groups condemn the strikes; Addis Ababa offers to host dialogue.",
         art="sudan"),
    dict(n=12, region="GAZA", tag="CONFIRMED", tag_src="REUTERS",
         headline="Hamas security chief killed in Beach camp strike",
         summary="The group's No. 2 security chief dies with his wife and two children.",
         art="gaza"),
    dict(n=13, region="UKRAINE", tag="CONFIRMED", tag_src="REUTERS, UKRENERGO",
         headline="Russian strikes cut power in five regions",
         summary="Overnight attacks hit a DTEK plant and grid sites; the nuclear plant on diesel.",
         art="power"),
    dict(n=14, region="RUSSIA", tag="REPORTED", tag_src="REUTERS, KYIV INDEPENDENT",
         headline="Ukraine drones set two Rosneft refineries ablaze",
         summary="Fires reported at Syzran and Kuibyshev plants, 800 km from the border.",
         art="refinery"),
    dict(n=15, region="WALL ST", tag="CONFIRMED", tag_src="REUTERS, NORDFX",
         headline="Dow tops 50,000 for the first time",
         summary="Dow +0.85% to 50,019; S&P slips 0.5%, Nasdaq falls 1.5%; Nvidia -5.9%.",
         art="dow"),
    dict(n=16, region="TECH", tag="CONFIRMED", tag_src="IANS",
         headline="Cisco chief: AI lets hackers outpace defences",
         summary="Robbins: AI finds flaws faster than firms can fix them; act in 30 days.",
         art="cisco"),
    dict(n=17, region="AI STOCKS", tag="CONFIRMED", tag_src="UPSTOX, ATFX",
         headline="Anthropic slips below its $83 IPO price",
         summary="Shares -6.5% to $81.90 a day after listing, as the AI rally fades.",
         art="anthropic"),
    dict(n=18, region="INDIA", tag="CONFIRMED", tag_src="REUTERS",
         headline="Sensex bucks the rout, up as much as 2.4%",
         summary="Indian shares rise while the rest of Asia falls; Sensex gains 1.5-2.4%.",
         art="sensex"),
]

TIMELINE = [
    ("00:08", "Coalition warns Hodeidah to evacuate"),
    ("00:18", "Shenzhou-24 launches"),
    ("02:09", "Coalition confirms Hodeidah strikes"),
    ("03:56", "Shenzhou-24 docks"),
    ("06:30", "Cartagena raid frees hostages"),
    ("13:30", "US PCE inflation + Q3 GDP due"),
]

NUMBERS = [
    ("50,019", "Dow's first close above 50,000"),
    ("-6.16%", "Kospi's fall to 4,697.51"),
    ("2,212", "Seoul Metro job cuts shelved"),
    ("30", "hostages held, all freed"),
    ("5", "Ukrainian regions without power"),
]

ALSO = [
    "Champions League (Tue night): Real Madrid 5-1 PSV; Man City 2-2 Napoli; Arsenal 1-1 Dortmund.",
    "NBA (Tue): Tatum's 41 lifts Celtics past Wizards 131-116; Pistons beat Magic 104-86.",
    "Hong Kong: a year on from the Tai Po fire; the anniversary is Thu.",
    "Russia says it hit a cargo ship in the Black Sea port of Chornomorsk.",
    "Naftogaz: a Russian strike sets its Poltava gas plant ablaze.",
    "Zaporizhzhia nuclear plant back on diesel power — the 17th time.",
    "US markets shut Thu for Thanksgiving.",
]

DATE_CHECK = ("Left out on purpose, first reported before Wednesday: COP31 collapse (Sun); "
              "Trump Iran interview (Tue); US tariff-probe findings, reported not published (Tue); "
              "Lilly buys LoQus23 for up to $725m (Mon); BepiColombo flyby (Mon); Hunger Games "
              "prequel (Sat); Norway's $7bn Ukraine aid (Tue); Spain snap election, 29 Nov (called 5 Oct). "
              "Not yet: Tai Po fire anniversary (Thu).")

SOURCES = ("Sources: Reuters, AP, AFP, Xinhua, Aviation Week, Korea JoongAng Daily, AJP, YTN, "
           "pm.gov.au, SuperSport, Ukrenergo, IANS, NordFX, UEFA, NBA — full list in README.")

# Map dots: (story number, map-local x, map-local y, region colour)
DOT_COLORS = {"EU": (31, 78, 121), "ME": (200, 16, 46), "AS": (30, 122, 52),
              "AM": (120, 60, 20), "AF": (198, 96, 10), "PA": (0, 120, 120)}
MAP_DOTS = [
    (1, 545, 32, "AS"), (2, 508, 46, "ME"), (3, 556, 42, "AS"), (4, 480, 72, "ME"),
    (5, 494, 58, "ME"), (6, 572, 24, "AS"), (7, 198, 82, "AM"), (8, 425, 78, "AF"),
    (9, 548, 112, "PA"), (10, 545, 82, "AS"), (11, 455, 78, "AF"), (12, 472, 48, "ME"),
    (13, 445, 28, "EU"), (14, 478, 22, "EU"), (15, 150, 42, "AM"), (16, 98, 52, "AM"),
    (17, 88, 40, "AM"), (18, 520, 62, "AS"),
]
# 1 Jiuquan, 2 Hormuz, 3 Shanghai (Asian markets), 4 Hodeidah, 5 Riyadh,
# 6 Seoul, 7 Cartagena, 8 Dakar, 9 Canberra, 10 Bogor, 11 Khartoum, 12 Gaza,
# 13 Kyiv, 14 Samara, 15 New York, 16 San Jose, 17 San Francisco, 18 Mumbai.

TAG_COLOR = {"CONFIRMED": GREEN, "OFFICIAL": BLUE, "REPORTED": ORANGE}


def tag_box(d, x_right, y, tag, src, f_tag):
    """Right-aligned verification tag, e.g. CONFIRMED · REUTERS (or just CONFIRMED)."""
    text = tag + (" · " + src if src else "")
    tw = d.textlength(text, font=f_tag)
    d.rectangle([x_right - tw - 8, y, x_right, y + 13], outline=TAG_COLOR[tag], width=1)
    d.text((x_right - tw - 4, y + 2), text, font=f_tag, fill=TAG_COLOR[tag])


def badge(d, x, y, n, r=10):
    d.ellipse([x - r, y - r, x + r, y + r], fill=RED)
    f = font(SANS_B, 11 if n < 10 else 10)
    tw = d.textlength(str(n), font=f)
    d.text((x - tw / 2, y - 7), str(n), font=f, fill=(255, 255, 255))


# ---------------------------------------------------------------- hero art

def art_rocket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    for sx, sy in [(20, 18), (60, 40), (110, 12), (160, 30), (210, 15), (260, 42),
                   (300, 20), (40, 70), (140, 62), (240, 66), (90, 95), (200, 95)]:
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(255, 255, 255))
    # Earth curve at the bottom (chord capped at the art box edge)
    d.chord([x - 60, y + h - 52, x + w + 60, y + h], 180, 360, fill=(38, 90, 160))
    d.arc([x - 60, y + h - 52, x + w + 60, y + h], 180, 360, fill=(90, 160, 220), width=2)
    # Station: grey bar + panels
    d.rectangle([x + 210, y + 26, x + 300, y + 36], fill=(180, 180, 180))
    d.rectangle([x + 218, y + 18, x + 246, y + 44], fill=(120, 140, 180))
    d.rectangle([x + 264, y + 18, x + 292, y + 44], fill=(120, 140, 180))
    # Rocket
    cx = x + 90
    d.polygon([(cx - 12, y + 62), (cx + 12, y + 62), (cx, y + 30)], fill=RED)
    d.rectangle([cx - 12, y + 62, cx + 12, y + 108], fill=(240, 240, 240))
    d.rectangle([cx - 12, y + 62, cx - 6, y + 108], fill=(200, 200, 200))
    d.polygon([(cx - 12, y + 96), (cx - 26, y + 112), (cx - 12, y + 108)], fill=RED)
    d.polygon([(cx + 12, y + 96), (cx + 26, y + 112), (cx + 12, y + 108)], fill=RED)
    d.polygon([(cx - 7, y + 108), (cx + 7, y + 108), (cx, y + 132)], fill=(255, 170, 0))
    d.polygon([(cx - 4, y + 108), (cx + 4, y + 108), (cx, y + 122)], fill=(255, 230, 120))


def art_sea(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 232, 242))
    d.rectangle([x, y + 78, x + w, y + h], fill=(38, 90, 140))
    for i in range(5):
        d.line([x, y + 88 + i * 10, x + w, y + 88 + i * 10], fill=(90, 150, 200), width=2)
    # Ship 1 (left)
    d.rectangle([x + 18, y + 62, x + 130, y + 84], fill=(60, 60, 60))
    d.rectangle([x + 60, y + 44, x + 96, y + 62], fill=(200, 200, 200))
    d.rectangle([x + 70, y + 34, x + 86, y + 44], fill=(150, 150, 150))
    # Ship 2 (right, burning)
    d.rectangle([x + 190, y + 66, x + 300, y + 86], fill=(90, 30, 30))
    d.rectangle([x + 225, y + 50, x + 255, y + 66], fill=(200, 200, 200))
    # Flames on ship 2
    d.polygon([(x + 215, y + 52), (x + 228, y + 18), (x + 240, y + 52)], fill=(255, 170, 0))
    d.polygon([(x + 232, y + 52), (x + 244, y + 26), (x + 256, y + 52)], fill=(255, 90, 0))
    d.polygon([(x + 248, y + 52), (x + 258, y + 34), (x + 268, y + 52)], fill=(255, 200, 60))
    # Smoke
    for sx, sy, r in [(240, 14, 9), (252, 6, 7), (228, 6, 6)]:
        d.ellipse([x + sx - r, y + sy - r, x + sx + r, y + sy + r], fill=(120, 120, 120))
    # Mines in the water
    for mx, my in [(150, 108), (170, 122), (140, 126)]:
        d.ellipse([x + mx - 4, y + my - 4, x + mx + 4, y + my + 4], fill=(20, 20, 20))
        d.line([x + mx - 7, y + my, x + mx + 7, y + my], fill=(20, 20, 20), width=1)
        d.line([x + mx, y + my - 7, x + mx, y + my + 7], fill=(20, 20, 20), width=1)


def art_chart(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    for i in range(1, 5):
        yy = y + i * h // 5
        d.line([x + 8, yy, x + w - 8, yy], fill=(50, 70, 110), width=1)
    pts = [(x + 14, y + 22), (x + 70, y + 34), (x + 120, y + 30), (x + 175, y + 58),
           (x + 225, y + 78), (x + 275, y + 96), (x + 316, y + 122)]
    d.line(pts, fill=(255, 70, 70), width=4, joint="curve")
    d.polygon([(pts[-1][0], pts[-1][1]), (pts[-1][0] - 12, pts[-1][1] - 2),
               (pts[-1][0] - 2, pts[-1][1] - 12)], fill=(255, 70, 70))
    f = font(SANS_B, 13)
    d.text((x + 14, y + 8), "KOSPI  -6.2%", font=f, fill=(255, 255, 255))
    d.text((x + 150, y + 44), "NIKKEI  -2.8%", font=f, fill=(255, 200, 200))
    d.text((x + 210, y + 104), "TAIEX  -4.8%", font=f, fill=(255, 200, 200))


# ---------------------------------------------------------------- tile art

def tile_art(d, kind, x, y, w, h):
    bg = {"hodeidah": (214, 232, 242), "riyadh": (232, 226, 214), "seoul": (220, 235, 225),
          "cartagena": (240, 228, 210), "afcon": (255, 243, 205), "treaty": (226, 232, 240),
          "mine": (232, 226, 214), "sudan": (240, 226, 226), "gaza": (228, 228, 228),
          "power": (30, 40, 70), "refinery": (40, 40, 50), "dow": (220, 240, 225),
          "cisco": (226, 232, 240), "anthropic": (240, 230, 245), "sensex": (220, 240, 225)}[kind]
    d.rectangle([x, y, x + w, y + h], fill=bg)
    cx, cy = x + w // 2, y + h // 2
    if kind == "hodeidah":
        d.rectangle([x + 30, y + 18, x + 110, y + 28], fill=(60, 60, 60))
        d.polygon([(x + 130, y + 20), (x + 140, y + 2), (x + 150, y + 20)], fill=(255, 170, 0))
        d.polygon([(x + 146, y + 20), (x + 154, y + 8), (x + 162, y + 20)], fill=(255, 90, 0))
        d.ellipse([x + 132, y - 2, x + 146, y + 10], fill=(120, 120, 120))
    elif kind == "riyadh":
        d.rectangle([cx - 6, y + 4, cx + 6, y + 30], fill=(90, 90, 90))
        d.rectangle([cx - 14, y + 30, cx + 14, y + 34], fill=(60, 60, 60))
        d.polygon([(cx - 10, y + 10), (cx, y - 2), (cx + 10, y + 10)], fill=(255, 150, 0))
        d.ellipse([cx - 4, y + 2, cx + 6, y + 10], fill=(150, 150, 150))
    elif kind == "seoul":
        d.rectangle([x + 40, y + 8, x + 150, y + 26], fill=(0, 120, 120))
        for wx in range(50, 146, 16):
            d.rectangle([x + wx, y + 12, x + wx + 10, y + 20], fill=(220, 245, 245))
        d.line([x + 20, y + 30, x + 170, y + 30], fill=(60, 60, 60), width=2)
    elif kind == "cartagena":
        d.rectangle([x + 45, y + 6, x + 145, y + 32], fill=(200, 160, 40))
        d.rectangle([x + 85, y + 16, x + 105, y + 32], fill=(90, 60, 20))
        d.rectangle([x + 45, y + 6, x + 145, y + 11], fill=(160, 30, 30))
    elif kind == "afcon":
        d.polygon([(cx - 12, y + 4), (cx + 12, y + 4), (cx + 8, y + 18), (cx - 8, y + 18)],
                  fill=(220, 180, 40))
        d.rectangle([cx - 3, y + 18, cx + 3, y + 26], fill=(180, 140, 30))
        d.rectangle([cx - 10, y + 26, cx + 10, y + 30], fill=(180, 140, 30))
        d.ellipse([cx - 18, y + 4, cx - 8, y + 12], outline=(220, 180, 40), width=2)
        d.ellipse([cx + 8, y + 4, cx + 18, y + 12], outline=(220, 180, 40), width=2)
    elif kind == "treaty":
        d.rectangle([x + 70, y + 4, x + 120, y + 30], fill=(255, 255, 255))
        d.rectangle([x + 70, y + 4, x + 120, y + 30], outline=(100, 100, 100))
        for i, ly in enumerate([10, 16, 22]):
            d.line([x + 76, y + ly, x + 114, y + ly], fill=(60, 60, 60), width=1)
        d.line([x + 130, y + 26, x + 150, y + 8], fill=(200, 16, 46), width=3)
    elif kind == "mine":
        d.polygon([(x + 30, y + 32), (x + 80, y + 4), (x + 130, y + 32)], fill=(140, 120, 90))
        d.polygon([(x + 68, y + 12), (x + 80, y + 4), (x + 92, y + 12)], fill=(255, 255, 255))
        d.ellipse([x + 140, y + 14, x + 160, y + 30], fill=(255, 210, 0))
        d.rectangle([x + 140, y + 24, x + 160, y + 28], fill=(200, 160, 0))
    elif kind == "sudan":
        d.polygon([(x + 60, y + 12), (x + 120, y + 4), (x + 120, y + 26), (x + 60, y + 20)],
                  fill=(200, 60, 60))
        d.rectangle([x + 48, y + 12, x + 60, y + 20], fill=(120, 30, 30))
        d.line([x + 122, y + 8, x + 140, y + 4], fill=(200, 60, 60), width=2)
        d.line([x + 122, y + 15, x + 142, y + 15], fill=(200, 60, 60), width=2)
        d.line([x + 122, y + 22, x + 140, y + 26], fill=(200, 60, 60), width=2)
    elif kind == "gaza":
        for bx, bh in [(40, 22), (75, 28), (112, 18), (145, 24)]:
            d.rectangle([x + bx, y + 32 - bh, x + bx + 24, y + 32], fill=(150, 150, 150))
        d.polygon([(x + 78, y + 2), (x + 88, y + 14), (x + 96, y + 4)], fill=(255, 170, 0))
    elif kind == "power":
        d.polygon([(cx + 6, y + 2), (cx - 12, y + 18), (cx - 1, y + 18),
                   (cx - 6, y + 32), (cx + 12, y + 14), (cx + 1, y + 14)],
                  fill=(255, 210, 0))
    elif kind == "refinery":
        for bx in [55, 85, 115]:
            d.rectangle([x + bx, y + 10, x + bx + 12, y + 30], fill=(180, 180, 180))
            d.polygon([(x + bx, y + 10), (x + bx + 6, y + 2), (x + bx + 12, y + 10)],
                      fill=(120, 120, 120))
        d.polygon([(x + 140, y + 14), (x + 148, y + 2), (x + 156, y + 14)], fill=(255, 150, 0))
    elif kind in ("dow", "sensex"):
        d.line([(x + 20, y + 28), (x + 70, y + 20), (x + 110, y + 22), (x + 160, y + 6)],
               fill=(30, 150, 60), width=4, joint="curve")
        d.polygon([(x + 160, y + 6), (x + 148, y + 4), (x + 158, y + 16)], fill=(30, 150, 60))
    elif kind == "cisco":
        d.polygon([(cx, y + 4), (cx + 14, y + 8), (cx + 14, y + 18), (cx, y + 30),
                   (cx - 14, y + 18), (cx - 14, y + 8)], fill=(31, 78, 121))
        d.line([(cx - 6, y + 16), (cx - 1, y + 21), (cx + 7, y + 11)],
               fill=(255, 255, 255), width=2, joint="curve")
    elif kind == "anthropic":
        d.rectangle([cx - 12, y + 6, cx + 12, y + 28], fill=(160, 60, 60))
        d.rectangle([cx - 6, y + 12, cx + 6, y + 22], fill=(255, 255, 255))
        for px in (-12, 12):
            d.line([cx + px, y + 12, cx + px + (6 if px < 0 else -6), y + 12],
                   fill=(160, 60, 60), width=2)


# ---------------------------------------------------------------- map

CONTINENTS = [
    # North America
    [(18, 18), (95, 8), (150, 20), (165, 45), (140, 72), (95, 78), (55, 62), (22, 45)],
    # South America
    [(185, 78), (225, 72), (245, 95), (225, 122), (195, 108)],
    # Europe
    [(400, 18), (455, 10), (470, 38), (440, 52), (405, 42)],
    # Africa
    [(415, 58), (465, 52), (480, 88), (450, 118), (420, 95)],
    # Asia
    [(475, 12), (560, 6), (588, 35), (575, 70), (540, 88), (505, 72), (478, 45)],
    # Australia
    [(520, 100), (560, 95), (568, 112), (535, 120)],
]


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SEA)
    for poly in CONTINENTS:
        d.polygon([(x + px, y + py) for px, py in poly], fill=LAND)
    f = font(SANS_B, 9)
    for n, mx, my, reg in MAP_DOTS:
        col = DOT_COLORS[reg]
        d.ellipse([x + mx - 8, y + my - 8, x + mx + 8, y + my + 8], fill=col,
                  outline=(255, 255, 255), width=1)
        tw = d.textlength(str(n), font=f)
        d.text((x + mx - tw / 2, y + my - 6), str(n), font=f, fill=(255, 255, 255))


# ---------------------------------------------------------------- build

def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    f_strap = font(SANS_B, 13)
    d.text((8, 8), "ONE DAY OF WORLD NEWS, ONE PICTURE", font=f_strap, fill=RED)
    f_sub = font(SANS_B, 11)
    sub = "25 STORIES · 6 REGIONS · 10 FIELDS · EVERY ONE FROM THIS WEDNESDAY"
    d.text((1016 - d.textlength(sub, font=f_sub), 10), sub, font=f_sub, fill=INK)
    d.text((8, 26), "Wednesday 25 November 2026", font=font(SERIF_B, 46), fill=INK)
    d.line([8, 84, 1016, 84], fill=INK, width=2)

    # ---- timeline strip
    d.rectangle([8, 90, 96, 128], fill=RED)
    f_lab = font(SANS_B, 11)
    d.text((14, 96), "THE DAY", font=f_lab, fill=(255, 255, 255))
    d.text((14, 110), "IN UTC", font=f_lab, fill=(255, 255, 255))
    col_w = (1016 - 100) / 6
    f_time = font(SANS_B, 13)
    f_tcap = font(SANS, 10)
    for i, (t, cap) in enumerate(TIMELINE):
        cx = 100 + i * col_w
        d.text((cx + 6, 91), t, font=f_time, fill=RED)
        draw_wrapped(d, cx + 6, 107, cap, f_tcap, col_w - 10, INK, 12, max_lines=2)
    d.line([8, 132, 1016, 132], fill=LIGHT_LINE, width=1)

    # ---- numbers strip
    d.rectangle([8, 136, 96, 170], fill=INK)
    d.text((14, 142), "THE DAY", font=f_lab, fill=(255, 255, 255))
    d.text((14, 154), "IN NUMBERS", font=font(SANS_B, 10), fill=(255, 255, 255))
    ncol_w = (1016 - 100) / 5
    f_big = font(SANS_B, 20)
    f_ncap = font(SANS, 9)
    for i, (big, cap) in enumerate(NUMBERS):
        cx = 100 + i * ncol_w
        col = RED if big.startswith("-") else INK
        d.text((cx + 6, 136), big, font=f_big, fill=col)
        draw_wrapped(d, cx + 6, 159, cap, f_ncap, ncol_w - 10, GREY, 11, max_lines=2)
    d.line([8, 174, 1016, 174], fill=INK, width=2)

    # ---- heroes
    hw, gap = 330, 9
    f_hreg = font(SANS_B, 11)
    f_htag = font(SANS_B, 9)
    f_hhead = font(SANS_B, 15)
    f_hsum = font(SANS, 11)
    for i, s in enumerate(HEROES):
        x = 8 + i * (hw + gap)
        y = 180
        d.rectangle([x, y, x + hw, y + 272], outline=(120, 110, 90), width=1)
        {"rocket": art_rocket, "sea": art_sea, "chart": art_chart}[s["art"]](d, x + 1, y + 1, hw - 2, 140)
        badge(d, x + 14, y + 156, s["n"])
        d.text((x + 28, y + 149), s["region"], font=f_hreg, fill=INK)
        tag_box(d, x + hw - 6, y + 149, s["tag"], s["tag_src"], f_htag)
        draw_wrapped(d, x + 8, y + 170, s["headline"], f_hhead, hw - 16, INK, 19, max_lines=2)
        draw_wrapped(d, x + 8, y + 210, s["summary"], f_hsum, hw - 16, (40, 40, 40), 14, max_lines=3)

    # ---- tiles: 5 columns x 3 rows
    tw_, th_, tgap = 196, 100, 7
    f_treg = font(SANS_B, 9)
    f_ttag = font(SANS_B, 8)
    f_thead = font(SANS_B, 11)
    f_tsum = font(SANS, 9)
    for i, s in enumerate(TILES):
        col, row = i % 5, i // 5
        x = 8 + col * (tw_ + tgap)
        y = 458 + row * (th_ + 5)
        d.rectangle([x, y, x + tw_, y + th_], outline=(120, 110, 90), width=1)
        tile_art(d, s["art"], x + 1, y + 1, tw_ - 2, 34)
        badge(d, x + 11, y + 45, s["n"], r=8)
        d.text((x + 23, y + 39), s["region"], font=f_treg, fill=INK)
        tag_box(d, x + tw_ - 4, y + 39, s["tag"], "", f_ttag)
        draw_wrapped(d, x + 5, y + 52, s["headline"], f_thead, tw_ - 10, INK, 13, max_lines=2)
        draw_wrapped(d, x + 5, y + 78, s["summary"], f_tsum, tw_ - 10, (40, 40, 40), 11, max_lines=2)

    # ---- bottom: map + ALSO ON
    f_sec = font(SANS_B, 12)
    d.text((8, 770), "WHERE IT HAPPENED", font=f_sec, fill=RED)
    d.text((612, 770), "ALSO ON WEDNESDAY 25 NOVEMBER", font=f_sec, fill=RED)
    d.line([8, 786, 1016, 786], fill=INK, width=1)
    draw_map(d, 8, 790, 596, 126)
    f_also = font(SANS, 11)
    f_anum = font(SANS_B, 11)
    ay = 792
    for i, item in enumerate(ALSO):
        n = 19 + i
        d.text((612, ay), str(n), font=f_anum, fill=RED)
        ay = draw_wrapped(d, 636, ay, item, f_also, 1016 - 636, INK, 13, max_lines=2) + 3

    # legend under the map
    f_leg = font(SANS, 9)
    lx = 8
    for label, reg in [("Europe 2", "EU"), ("Middle East 4", "ME"), ("Asia 5", "AS"),
                       ("Americas 4", "AM"), ("Africa 2", "AF"), ("Pacific 1", "PA")]:
        d.ellipse([lx, 921, lx + 7, 928], fill=DOT_COLORS[reg])
        lx += 10
        d.text((lx, 920), label, font=f_leg, fill=INK)
        lx += d.textlength(label, font=f_leg) + 12

    # ---- footer
    d.rectangle([8, 934, 1016, 974], outline=RED, width=1)
    d.rectangle([8, 934, 108, 974], fill=RED)
    d.text((14, 946), "DATE CHECK", font=font(SANS_B, 11), fill=(255, 255, 255))
    draw_wrapped(d, 116, 937, DATE_CHECK, font(SANS, 10), 1016 - 124, INK, 12, max_lines=3)
    # legend line
    f_foot = font(SANS, 10)
    lx = 8
    for label, col in [("CONFIRMED", GREEN), ("OFFICIAL", BLUE), ("REPORTED", ORANGE)]:
        d.rectangle([lx, 982, lx + 9, 991], fill=col)
        lx += 12
        d.text((lx, 981), label, font=font(SANS_B, 10), fill=col)
        lx += d.textlength(label, font=font(SANS_B, 10)) + 6
    d.text((lx, 981), "= 2+ outlets      = on the record      = one outlet / claim",
           font=f_foot, fill=INK)
    d.text((8, 998), SOURCES, font=font(SANS, 9), fill=GREY)
    d.text((8, 1010), "Every story here happened or was first reported on Wed 25 Nov 2026.",
           font=font(SANS, 9), fill=GREY)

    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "entry.png")
    img.save(path, "PNG")
    return path


if __name__ == "__main__":
    print(build())
