#!/usr/bin/env python3
"""THE WORLD — Friday 20 November 2026. A newspaper front page drawn
from scratch with Pillow: 35 dated stories, 7 regions, 3 lead panels,
10 feature stories, a world map with numbered pins, a UTC timeline,
a day-in-numbers strip and a date-check box. No network, no clock,
no randomness: two runs write byte-identical PNGs."""

import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
M = 20                      # side margin
CW = W - 2 * M              # 984 content width

PAPER = (247, 241, 222)
INK = (22, 20, 18)
RED = (178, 34, 28)
RED_DK = (140, 24, 20)
NAVY = (16, 32, 66)
NAVY2 = (24, 48, 96)
TEAL = (14, 110, 110)
GOLD = (176, 132, 30)
GREY = (96, 90, 80)
RULE = (150, 138, 112)
TAN = (214, 196, 150)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit `width` px."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_lines(d, x, y, lines, fnt, fill=INK, leading=None, align="left"):
    lead = leading if leading is not None else int(fnt.size * 1.28)
    for i, ln in enumerate(lines):
        if align == "center":
            d.text((x + CW // 2, y + i * lead), ln, font=fnt, fill=fill,
                   anchor="ma")
        else:
            d.text((x, y + i * lead), ln, font=fnt, fill=fill)
    return y + len(lines) * lead


def chip(d, x, y, label, bg, fg=(255, 255, 255)):
    f = font(SANS_B, 11)
    w = int(d.textlength(label, font=f)) + 18
    d.rounded_rectangle([x, y, x + w, y + 19], radius=4, fill=bg)
    d.text((x + 9, y + 4), label, font=f, fill=fg)
    return w


def tag(d, x, y, label, bg=RED, fg=(255, 255, 255), size=11):
    f = font(SANS_B, size)
    w = int(d.textlength(label, font=f)) + 12
    d.rectangle([x, y, x + w, y + size + 7], fill=bg)
    d.text((x + 6, y + 3), label, font=f, fill=fg)
    return w


# ------------------------------------------------------------------ panels
def panel_kyiv(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(10, 18, 44))
    for sx, sy, r in [(18, 14, 1), (70, 26, 1), (130, 10, 2), (200, 30, 1),
                      (260, 12, 1), (300, 34, 2), (40, 44, 1), (170, 40, 1)]:
        d.ellipse([x + sx - r, y + sy - r, x + sx + r, y + sy + r],
                  fill=(255, 240, 190))
    # skyline silhouettes
    for bx, bw, bh in [(0, 34, 34), (38, 26, 48), (68, 40, 30), (112, 22, 52),
                       (138, 44, 36), (186, 30, 46), (220, 36, 30),
                       (260, 28, 44), (292, 28, 32)]:
        d.rectangle([x + bx, y + h - 46 - bh, x + bx + bw, y + h - 46],
                    fill=(20, 34, 70))
        for wy in range(y + h - 42 - bh, y + h - 50, 8):
            for wx in range(x + bx + 4, x + bx + bw - 4, 9):
                if (wx * 7 + wy * 3) % 11 < 4:
                    d.rectangle([wx, wy, wx + 2, wy + 3], fill=(255, 214, 110))
    # river + bridge deck
    d.rectangle([x, y + h - 46, x + w, y + h], fill=(14, 42, 84))
    d.line([x, y + h - 46, x + w, y + h - 46], fill=(120, 160, 220), width=2)
    for i in range(5):
        bx = x + 30 + i * 62
        d.line([bx, y + h - 46, bx + 14, y + h - 78], fill=(200, 210, 235),
               width=2)
        d.ellipse([bx + 9, y + h - 82, bx + 19, y + h - 72],
                  fill=(255, 214, 110))
    # fires on the deck
    for fx in (x + 78, x + 196, x + 272):
        d.polygon([(fx, y + h - 66), (fx - 9, y + h - 44), (fx + 9, y + h - 44)],
                  fill=(255, 150, 30))
        d.polygon([(fx, y + h - 58), (fx - 5, y + h - 44), (fx + 5, y + h - 44)],
                  fill=(255, 220, 90))
    # dashed missile trails
    for k in range(9):
        px = x + 250 - k * 16
        py = y + 14 + k * 5
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(255, 220, 130))
    d.ellipse([x + 96, y + 62, x + 104, y + 70], fill=(255, 220, 130))


def panel_cyclone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(28, 84, 138))
    # coast landmass, left
    d.polygon([(x, y), (x + 92, y), (x + 78, y + 46), (x + 96, y + 78),
               (x + 60, y + h), (x, y + h)], fill=(196, 178, 120))
    d.polygon([(x, y), (x + 40, y), (x + 30, y + 60), (x, y + 70)],
              fill=(120, 150, 90))
    # spiral bands
    cx, cy = x + w - 108, y + h // 2 + 4
    for r, col in [(66, (255, 255, 255)), (52, (230, 240, 248)),
                   (38, (255, 255, 255)), (24, (210, 226, 240))]:
        d.arc([cx - r, cy - r, cx + r, cy + r], start=200, end=560,
              fill=col, width=7)
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(255, 255, 255))
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(28, 84, 138))
    # rain streaks over the coast
    for i in range(7):
        rx = x + 12 + i * 11
        d.line([rx, y + 84 + (i % 3) * 6, rx - 5, y + 100 + (i % 3) * 6],
               fill=(220, 235, 245), width=2)
    # landfall marker
    lx, ly = x + 88, y + 62
    d.ellipse([lx - 5, ly - 5, lx + 5, ly + 5], fill=RED)
    d.ellipse([lx - 9, ly - 9, lx + 9, ly + 9], outline=(255, 255, 255),
              width=2)


def panel_markets(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(18, 10, 12))
    # faint red ticker figures
    tf = font(SANS_B, 9)
    for i, num in enumerate(["26941", "18607", "51275", "3949", "15960",
                             "135164", "21302", "48688"]):
        d.text((x + 14 + (i % 4) * 78, y + 6 + (i // 4) * 14), num,
               font=tf, fill=(150, 40, 36))
    # red volume bars, falling
    bars = [52, 44, 58, 40, 48, 34, 42, 26, 30, 18]
    bw = w // len(bars)
    for i, bh in enumerate(bars):
        d.rectangle([x + i * bw + 4, y + h - 14 - bh,
                     x + (i + 1) * bw - 4, y + h - 14], fill=(196, 32, 26))
    # white falling line
    pts = []
    for i in range(11):
        pts.append((x + 8 + i * (w - 16) // 10,
                    y + 34 + int((i / 10) ** 1.4 * (h - 64))
                    + (6 if i % 3 == 0 else -4)))
    d.line(pts, fill=(255, 255, 255), width=3, joint="curve")
    d.polygon([(pts[-1][0], pts[-1][1]), (pts[-1][0] - 12, pts[-1][1] - 2),
               (pts[-1][0] - 4, pts[-1][1] + 10)], fill=(220, 40, 30))

# ------------------------------------------------------- feature mini-panels
def mini_ukeu(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 48, 110))
    # Union Jack suggestion: red cross + white diagonals on blue
    d.line([x, y, x + w, y + h], fill=(255, 255, 255), width=5)
    d.line([x + w, y, x, y + h], fill=(255, 255, 255), width=5)
    d.line([x + w // 2, y, x + w // 2, y + h], fill=(200, 30, 30), width=8)
    d.line([x, y + h // 2, x + w, y + h // 2], fill=(200, 30, 30), width=8)
    # EU stars ring, right
    cx, cy = x + w - 34, y + h // 2
    for k in range(8):
        a = math.radians(k * 45)
        d.ellipse([cx + 13 * math.cos(a) - 2, cy + 13 * math.sin(a) - 2,
                   cx + 13 * math.cos(a) + 2, cy + 13 * math.sin(a) + 2],
                  fill=(255, 220, 60))


def mini_cop(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(18, 96, 88))
    d.ellipse([x + 12, y + 8, x + 74, y + 52], fill=(70, 160, 120))
    d.arc([x + 20, y + 16, x + 66, y + 44], 0, 360, fill=(255, 255, 255),
          width=2)
    d.line([x + 24, y + 30, x + 62, y + 30], fill=(255, 255, 255), width=2)
    # thermometer, right
    d.rectangle([x + 96, y + 10, x + 104, y + 40], fill=(255, 255, 255))
    d.ellipse([x + 92, y + 36, x + 108, y + 52], fill=(220, 40, 30))
    d.rectangle([x + 99, y + 16, x + 101, y + 40], fill=(220, 40, 30))


def mini_poland(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(150, 190, 120))
    d.rectangle([x, y + h - 16, x + w, y + h], fill=(90, 140, 70))
    d.polygon([(x + 30, y + 34), (x + 130, y + 22), (x + 150, y + 30),
               (x + 30, y + 42)], fill=(120, 125, 130))
    d.polygon([(x + 150, y + 30), (x + 168, y + 26), (x + 168, y + 34),
               (x + 150, y + 30)], fill=(220, 40, 30))
    d.ellipse([x + 150, y + 8, x + 178, y + 36], fill=(255, 200, 60))
    d.ellipse([x + 158, y + 16, x + 170, y + 28], fill=(255, 120, 30))


def mini_iraq(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(216, 186, 130))
    d.ellipse([x + w - 46, y + 8, x + w - 14, y + 40], fill=(255, 214, 110))
    for i, tx in enumerate((14, 62, 110)):
        d.rectangle([x + tx, y + 30, x + tx + 42, y + 46], fill=(70, 90, 50))
        d.ellipse([x + tx + 8, y + 46, x + tx + 16, y + 54], fill=(30, 30, 30))
        d.ellipse([x + tx + 28, y + 46, x + tx + 36, y + 54], fill=(30, 30, 30))
    d.rectangle([x, y + h - 8, x + w, y + h], fill=(180, 150, 100))


def mini_italy(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 240, 235))
    d.rectangle([x, y, x + w // 3, y + h], fill=(30, 140, 70))
    d.rectangle([x + 2 * w // 3, y, x + w, y + h], fill=(200, 40, 40))
    for i in range(9):
        px = x + 16 + (i % 3) * 58
        py = y + 12 + (i // 3) * 16
        d.ellipse([px, py, px + 7, py + 7], fill=(30, 30, 30))
        d.rectangle([px + 2, py + 7, px + 5, py + 14], fill=(30, 30, 30))


def mini_japan(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(245, 245, 240))
    d.ellipse([x + 14, y + 8, x + 58, y + 52], fill=(200, 40, 40))
    bars = [14, 20, 26, 34]
    for i, bh in enumerate(bars):
        bx = x + 84 + i * 24
        d.rectangle([bx, y + h - 10 - bh, bx + 16, y + h - 10],
                    fill=(40, 90, 160))
    d.line([x + 80, y + h - 44, x + w - 8, y + h - 52], fill=RED, width=3)


def mini_seoul(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(210, 205, 190))
    d.polygon([(x + 30, y + 12), (x + 100, y + 12), (x + 118, y + 24),
               (x + 12, y + 24)], fill=(120, 110, 95))
    for i in range(5):
        cx = x + 26 + i * 20
        d.rectangle([cx, y + 26, cx + 8, y + 48], fill=(240, 238, 230))
    d.rectangle([x + 12, y + 48, x + 118, y + 54], fill=(120, 110, 95))
    # gavel, right
    d.line([x + 138, y + 16, x + 168, y + 46], fill=(90, 60, 30), width=5)
    d.rectangle([x + 132, y + 10, x + 152, y + 20], fill=(60, 40, 20))


def mini_kenya(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(250, 170, 70))
    d.ellipse([x + w // 2 - 22, y + 6, x + w // 2 + 22, y + 50],
              fill=(255, 220, 120))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(120, 80, 40))
    # oil derrick silhouette
    d.polygon([(x + 30, y + h - 14), (x + 52, y + 8), (x + 66, y + 8),
               (x + 88, y + h - 14)], fill=(40, 30, 25))
    d.line([x + 52, y + 8, x + 88, y + h - 14], fill=(40, 30, 25), width=3)
    d.line([x + 66, y + 8, x + 30, y + h - 14], fill=(40, 30, 25), width=3)


def mini_bukele(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 90, 170))
    d.rectangle([x + 58, y + 20, x + 130, y + 52], fill=(240, 240, 235))
    d.rectangle([x + 58, y + 20, x + 130, y + 28], fill=(200, 40, 40))
    d.line([x + 78, y + 32, x + 86, y + 44], fill=(30, 140, 70), width=4)
    d.line([x + 86, y + 44, x + 110, y + 26], fill=(30, 140, 70), width=4)
    d.rectangle([x + 20, y + 14, x + 44, y + 38], fill=(255, 255, 255))
    d.text((x + 26, y + 18), "3rd", font=font(SANS_B, 11), fill=RED)


def mini_cricket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(70, 150, 70))
    d.ellipse([x + 12, y + 10, x + 176, y + 58], fill=(120, 190, 90))
    d.line([x + 30, y + 44, x + 130, y + 20], fill=(210, 170, 110), width=7)
    d.ellipse([x + 140, y + 12, x + 154, y + 26], fill=(200, 40, 40))
    d.line([x + 150, y + 26, x + 158, y + 44], fill=(255, 255, 255), width=2)


MINI = [mini_ukeu, mini_cop, mini_poland, mini_iraq, mini_italy,
        mini_japan, mini_seoul, mini_kenya, mini_bukele, mini_cricket]

# ------------------------------------------------------------------- content
LEADS = [
    dict(n=1, label="KYIV", loc="KYIV, UKRAINE · WAR", panel=panel_kyiv,
         head="Russian missiles hit three Kyiv bridges",
         body=("111 missiles and 400 drones hit overnight, killing at "
               "least nine and cutting power and water in Kyiv. (BBC)"),
         src="Officials' count", verify="CONFIRMED"),
    dict(n=2, label="CYCLONE AKVAN", loc="ODISHA, INDIA · CYCLONE",
         panel=panel_cyclone,
         head="Cyclone Akvan comes ashore in eastern India",
         body=("Crossed the coast near Gopalpur from about 8 am after "
               "300,000+ people moved to shelters. (IMD, Deccan Herald)"),
         src="Weather office", verify="CONFIRMED"),
    dict(n=3, label="AI SELL-OFF", loc="TAIPEI · SEOUL · TOKYO · MARKETS",
         panel=panel_markets,
         head="AI sell-off sinks Asia's stock markets",
         body=("Taiwan fell 6.2%, its worst week since 1991. Seoul lost "
               "5.2% and Tokyo 5.1% as chipmakers led the slide. "
               "(Al Jazeera)"),
         src="Closing prices", verify="OFFICIAL"),
]

FEATURES = [
    (4, "UK-EU DEAL", "BRUSSELS · DIPLOMACY",
     "UK and EU seal a \u201creset\u201d deal",
     "Food trade, youth visas, carbon link.", "Agreed · Reuters", "OFFICIAL"),
    (5, "COP31: NO DEAL", "ANTALYA · CLIMATE",
     "COP31 reaches its last day with no deal",
     "The draft text leaves out fossil fuels.", "Ongoing · UN News", "REPORTED"),
    (6, "POLAND: MISSILE", "EASTERN POLAND · SECURITY",
     "Russian cruise missile lands in Poland",
     "It fell in a field; two airports paused.", "Minister says · Reuters", "REPORTED"),
    (7, "IRAQ: ARMY IN", "CENTRAL IRAQ · SECURITY",
     "Iraqi army enters a militia stronghold",
     "Troops deploy to Jurf al-Sakhar.", "Witnessed · Reuters", "CONFIRMED"),
    (8, "ITALY: STRIKE", "ITALY · LABOUR",
     "General strike over Italy's budget",
     "Workers and students march.", "Reported · Reuters", "REPORTED"),
    (9, "JAPAN: +2.3%", "TOKYO · ECONOMY",
     "Japan's inflation picks up to 2.3%",
     "A December rate rise stays in view.", "Official data · Reuters", "OFFICIAL"),
    (10, "SEOUL: IMPEACH", "SEOUL · POLITICS",
     "Korea's ruling party to impeach top judge",
     "It follows an overturned conviction.", "Party decision · Korea Herald", "REPORTED"),
    (11, "KENYA: OIL", "TURKANA, KENYA · ENERGY",
     "Kenya starts drilling its first oil",
     "First crude is due on 1 December.", "Ceremony held · allAfrica", "OFFICIAL"),
    (12, "BUKELE: 3RD BID", "SAN SALVADOR · POLITICS",
     "Bukele files to run for a third term",
     "The vote is on 28 February 2027.", "Filed · AP", "OFFICIAL"),
    (13, "PHILLIPS: 118", "WELLINGTON · CRICKET",
     "Phillips hits 118 against India",
     "Hundreds in India in all three formats.", "Scorecard · ICC", "OFFICIAL"),
]

ALSO_LEFT = [
    (14, "Lviv", "A strike on a railway station kills two (BBC)"),
    (15, "Moscow", "Russia declares Estonia's border closure (Reuters)"),
    (16, "Berlin", "Pupils strike against military service (Al Jazeera)"),
    (17, "London", "General says UK runs cyber attacks abroad (Sky News)"),
    (18, "Beijing", "China holds its loan rates for an 18th month (Xinhua)"),
    (19, "Tokyo", "SoftBank shares fall more than 14% in a day (Al Jazeera)"),
    (20, "Seoul", "Kospi index ends the week 7.9% lower (Anadolu)"),
    (21, "Ganjam", "209 mm of rain falls as Akvan crosses Odisha (PTI)"),
    (22, "Lebanon", "Israeli air strikes hit south and east (Anadolu)"),
    (23, "Yemen", "Gunmen fire on a cargo ship off the coast (UKMTO)"),
    (24, "Abuja", "Court bars new evidence against Tinubu (Channels TV)"),
]
ALSO_RIGHT = [
    (25, "Kampala", "Police told to enforce Ebola ban on rallies (allAfrica)"),
    (26, "Malawi", "Fuel crisis brings night-long petrol queues (Al Jazeera)"),
    (27, "Africa", "AFDB says 22 countries are in debt distress (allAfrica)"),
    (28, "Las Vegas", "Russell fastest in wet Grand Prix practice (Autosport)"),    (29, "New York", "Nasdaq futures fall 1.6% before the bell (Wall St)"),
    (30, "Washington", "Democrats query law firm's free work (Al Jazeera)"),
    (31, "Wellington", "Nicholls makes 175 in a stand of 216 (ICC)"),
    (32, "Sydney", "Australian shares fall 1.8% in the sell-off (Reuters)"),
    (33, "Antalya", "Panama asks COP31 to cap world oil output (Anadolu)"),
    (34, "Antalya", "EU official calls the climate draft unacceptable (RTE)"),
    (35, "Turin", "ATP backs a plan to lift player pay past $350m (Anadolu)"),
]

# lon, lat, small stagger (dx, dy) for the crowded European pins
PINS = [(30.5, 50.4, 3, -11), (84.9, 19.3, 0, 0), (121.6, 25.0, 0, 0),
        (4.4, 50.9, -11, -6), (30.7, 36.9, 11, 7), (23.5, 52.0, 13, -7),
        (44.4, 33.3, 0, 0), (12.5, 41.9, -13, 7), (139.7, 35.7, 0, 0),
        (127.0, 37.5, 0, 0), (36.0, 3.0, 0, 0), (-89.2, 13.7, 0, 0),
        (174.8, -41.3, 0, 0)]

CONTINENTS = [
    [(-168, 66), (-140, 70), (-110, 68), (-90, 72), (-70, 62), (-55, 47),
     (-70, 42), (-80, 26), (-95, 19), (-105, 22), (-118, 32), (-125, 48),
     (-150, 60), (-168, 66)],
    [(-80, 10), (-60, 8), (-35, -5), (-40, -20), (-55, -35), (-70, -40),
     (-73, -25), (-80, -5), (-80, 10)],
    [(-18, 35), (-10, 37), (0, 36), (10, 37), (20, 32), (32, 31),
     (35, 28), (43, 12), (51, 11), (48, -5), (40, -18), (32, -28),
     (20, -35), (15, -25), (12, -8), (8, 4), (-8, 5), (-17, 15),
     (-18, 35)],
    [(-10, 70), (5, 58), (10, 57), (20, 54), (30, 60), (40, 68),
     (60, 69), (80, 73), (110, 74), (140, 72), (170, 66), (180, 65),
     (160, 60), (140, 45), (127, 40), (120, 30), (108, 20), (100, 8),
     (90, 15), (80, 8), (75, 20), (65, 25), (55, 26), (45, 30),
     (35, 36), (25, 40), (15, 44), (0, 44), (-10, 48), (-10, 70)],
    [(113, -22), (125, -15), (135, -12), (145, -11), (153, -27),
     (150, -38), (140, -38), (130, -32), (115, -35), (113, -22)],
]


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # paper edge
    d.rectangle([0, 0, W - 1, H - 1], outline=RULE, width=2)

    # ---- kicker ------------------------------------------------------
    d.text((M, 12), "THE WORLD IN ONE DAY", font=font(SANS_B, 13), fill=RED)
    rk = "35 STORIES · 7 REGIONS · EVERY ONE DATED FRIDAY 20 NOVEMBER 2026"
    d.text((W - M, 12), rk, font=font(SANS_B, 11), fill=INK, anchor="ra")
    d.line([M, 30, W - M, 30], fill=INK, width=2)

    # ---- giant headline + sub-head -----------------------------------
    d.text((W // 2, 36), "Friday 20 November 2026",
           font=font(SERIF_B, 62), fill=INK, anchor="ma")
    sub = ("Russian missiles hit Kyiv's bridges · Cyclone Akvan strikes "
           "India · An AI sell-off sinks Asia's markets · UK and EU seal a deal")
    d.text((W // 2, 102), sub, font=font(SERIF_I, 15), fill=(60, 55, 48),
           anchor="ma")
    d.line([M, 124, W - M, 124], fill=RULE, width=1)

    # ---- stats strip ---------------------------------------------------
    stats = [("3", "bridges over the Dnipro damaged in Kyiv"),
             ("300,000+", "people moved to shelters before Akvan"),
             ("-6.2%", "Taiwan's share index, Friday's close"),
             ("100,000", "youth visas a year in the UK-EU deal"),
             ("2.3%", "Japan consumer inflation in October"),
             ("118", "runs by Glenn Phillips against India")]
    colw = CW // 6
    for i, (num, cap) in enumerate(stats):
        x = M + i * colw
        if i:
            d.line([x - 6, 132, x - 6, 164], fill=RED, width=2)
        d.text((x, 128), num, font=font(SERIF_B, 22), fill=INK)
        text_lines(d, x, 152, wrap(d, cap, font(SANS, 9), colw - 14),
                   font(SANS, 9), fill=GREY, leading=10)
    d.line([M, 176, W - M, 176], fill=RULE, width=1)

    # ---- region chips --------------------------------------------------
    chips = [("Europe 8", (30, 70, 150)), ("Asia 8", (178, 34, 28)),
             ("Middle East 3", (150, 110, 20)), ("Africa 5", (30, 120, 70)),
             ("Americas 4", (110, 50, 140)), ("Oceania 3", (14, 110, 110)),
             ("Global 4", (90, 90, 90))]
    cx = M
    for label, bg in chips:
        cx += chip(d, cx, 182, label, bg) + 8
    d.text((W - M, 184), "35 stories · 7 regions",
           font=font(SANS, 10), fill=GREY, anchor="ra")

    # ---- UTC timeline ---------------------------------------------------
    d.rectangle([M, 208, W - M, 230], fill=NAVY)
    d.text((M + 10, 213), "THE DAY IN UTC · TIMES APPROX.",
           font=font(SANS_B, 11), fill=(255, 220, 90))
    tl = ("00:30  Kyiv barrage   ·   02:30  Akvan landfall   ·   07:00  "
          "Asia close   ·   14:00  COP31 stalls   ·   19:00  UK-EU deal")
    d.text((M + 252, 213), tl, font=font(SANS, 11), fill=(255, 255, 255))

    # ---- lead stories ---------------------------------------------------
    lw = (CW - 24) // 3
    for i, lead in enumerate(LEADS):
        x = M + i * (lw + 12)
        y = 240
        lead["panel"](d, x, y, lw, 110)
        tag(d, x + 8, y + 8, lead["label"])
        d.rectangle([x, y + 110 - 18, x + 96, y + 110], fill=(0, 0, 0))
        d.text((x + 5, y + 110 - 15), lead["src"], font=font(SANS_B, 9),
               fill=(255, 255, 255))
        ty = 358
        d.text((x, ty), "%d  %s" % (lead["n"], lead["loc"]),
               font=font(SANS_B, 10), fill=RED)
        d.text((x + lw, ty), "✓ " + lead["verify"],
               font=font(SANS_B, 10), fill=RED_DK, anchor="ra")
        ty = text_lines(d, x, ty + 16,
                        wrap(d, lead["head"], font(SERIF_B, 16), lw),
                        font(SERIF_B, 16), leading=19)
        ty = text_lines(d, x, ty + 4,
                        wrap(d, lead["body"], font(SANS, 11), lw),
                        font(SANS, 11), leading=13)

    # ---- feature stories, two rows of five ------------------------------
    fw = (CW - 40) // 5
    for row in range(2):
        for c in range(5):
            k = row * 5 + c
            n, label, loc, head, body, src, ver = FEATURES[k]
            x = M + c * (fw + 10)
            py = 464 + row * 124
            MINI[k](d, x, py, fw, 56)
            tag(d, x + 5, py + 5, label, size=9)
            d.rectangle([x, py + 56 - 14, x + fw, py + 56], fill=(0, 0, 0))
            d.text((x + 5, py + 56 - 12), src, font=font(SANS, 8),
                   fill=(255, 255, 255))
            ty = py + 62
            d.text((x, ty), "%d  %s" % (n, loc), font=font(SANS_B, 8),
                   fill=RED)
            ty = text_lines(d, x, ty + 12,
                            wrap(d, head, font(SERIF_B, 12), fw),
                            font(SERIF_B, 12), leading=14)
            ty = text_lines(d, x, ty + 2,
                            wrap(d, body, font(SANS, 9), fw),
                            font(SANS, 9), leading=11)
            d.text((x, ty + 1), "✓ " + ver, font=font(SANS_B, 8),
                   fill=RED_DK)

    # ---- map + also-on-friday -------------------------------------------
    my = 726
    d.text((M, my), "WHERE IT HAPPENED", font=font(SANS_B, 12), fill=INK)
    d.text((M, my + 15), "Pins 1-13: the lead and feature stories above",
           font=font(SANS, 9), fill=GREY)
    mx, mw, mh = M, 310, 118
    mapy = my + 30
    d.rectangle([mx, mapy, mx + mw, mapy + mh], fill=NAVY)
    for poly in CONTINENTS:
        pts = []
        for lon, lat in poly:
            px = mx + 6 + (lon + 180) / 360.0 * (mw - 12)
            py = mapy + 4 + (75 - lat) / 130.0 * (mh - 8)
            pts.append((px, py))
        d.polygon(pts, fill=TAN)
    for i, (lon, lat, dx, dy) in enumerate(PINS, start=1):
        px = mx + 6 + (lon + 180) / 360.0 * (mw - 12) + dx
        py = mapy + 4 + (75 - lat) / 130.0 * (mh - 8) + dy
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED,
                  outline=(255, 255, 255), width=1)
        d.text((px, py - 4), str(i), font=font(SANS_B, 7),
               fill=(255, 255, 255), anchor="mm")
    d.text((M, mapy + mh + 4),
           "Each number is that story's number on this page.",
           font=font(SANS, 9), fill=GREY)

    ax = M + 330
    d.text((ax, my), "ALSO ON FRIDAY 20 NOVEMBER — 22 MORE STORIES",
           font=font(SANS_B, 12), fill=INK)
    d.line([ax, my + 16, W - M, my + 16], fill=RED, width=2)
    af = font(SANS, 9)
    for col, items in enumerate((ALSO_LEFT, ALSO_RIGHT)):
        x = ax + col * 332
        yy = my + 22
        for n, place, txt in items:
            line = "%d  %s — %s" % (n, place, txt)
            for ln in wrap(d, line, af, 326):
                d.text((x, yy), ln, font=af, fill=INK)
                yy += 11
            yy += 1

    # ---- day in numbers ---------------------------------------------------
    ny = 906
    d.rectangle([M, ny, W - M, ny + 30], fill=(232, 222, 198))
    d.text((M + 10, ny + 8), "THE DAY IN NUMBERS",
           font=font(SANS_B, 11), fill=RED_DK)
    nums = ("111 missiles  ·  400 drones  ·  9 killed in Kyiv  ·  "
            "209 mm of rain in Ganjam  ·  -14% SoftBank in a day  ·  "
            "$350m ATP player-pay plan")
    d.text((M + 168, ny + 8), nums, font=font(SANS, 11), fill=INK)

    # ---- date check -------------------------------------------------------
    dy = 944
    d.rectangle([M, dy, W - M, dy + 52], outline=RED, width=2)
    d.text((M + 10, dy + 6), "DATE CHECK",
           font=font(SANS_B, 11), fill=RED)
    dc = ("Left out as Thursday 19 November's news: the World Court's "
          "ruling on Myanmar, the three-leader declaration in Shenzhen, "
          "Tonga's drought emergency and the migrant boat lost off Senegal. "
          "Not yet happened, so not shown: BepiColombo's entry into orbit "
          "around Mercury, and any final COP31 text.")
    text_lines(d, M + 10, dy + 20, wrap(d, dc, font(SANS, 10), CW - 20),
               font(SANS, 10), leading=13)

    # ---- credit -----------------------------------------------------------
    d.text((M, 1004),
           "Every story here happened, or was first reported, on Friday "
           "20 November 2026. Officials' counts are attributed.",
           font=font(SANS, 10), fill=INK)
    d.text((W - M, 1004), "Sources named beside each story · original drawings",
           font=font(SANS, 10), fill=GREY, anchor="ra")
    return img


if __name__ == "__main__":
    out = os.path.join(HERE, "entry.png")
    build().save(out, "PNG", optimize=True)
    print("wrote %s (%d bytes)" % (out, os.path.getsize(out)))
