#!/usr/bin/env python3
"""Draw the 20 November 2026 world-news poster (1024x1024 PNG).

Deterministic, no network. Run: python3 make_poster.py  -> writes entry.png
Sources for the six stories (all reported 20 Nov 2026): BBC, AP, Reuters,
The Hindu, Japan Times, Dawn, Le Monde, UN News, ICJ.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (13, 27, 46)        # deep navy
CARD = (24, 44, 71)      # panel navy
CARD2 = (30, 56, 88)
GOLD = (232, 184, 76)
WHITE = (245, 246, 248)
MUTED = (178, 196, 216)
ACCENTS = {
    "summit": (232, 184, 76),
    "icj": (96, 165, 250),
    "cop": (74, 222, 128),
    "anthropic": (240, 130, 90),
    "ukraine": (250, 204, 21),
    "cyclone": (56, 189, 248),
}

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(size, bold=True):
    return ImageFont.truetype(FB if bold else FR, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_globe(d, cx, cy, r, color):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=5)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=color, width=3)
    d.line([cx - r, cy, cx + r, cy], fill=color, width=3)
    d.arc([cx - r, cy - r * 0.45, cx + r, cy + r * 0.45], 0, 360, fill=color, width=3)


def draw_scales(d, cx, cy, s, color):
    d.line([cx, cy - s, cx, cy + s], fill=color, width=5)
    d.line([cx - s, cy - s * 0.45, cx + s, cy - s * 0.45], fill=color, width=5)
    for x in (cx - s, cx + s):
        d.line([x, cy - s * 0.45, x, cy + s * 0.25], fill=color, width=3)
        d.polygon([(x - s * 0.42, cy + s * 0.25), (x + s * 0.42, cy + s * 0.25),
                   (x, cy + s * 0.8)], outline=color, width=3)
    d.line([cx - s * 0.5, cy + s, cx + s * 0.5, cy + s], fill=color, width=5)


def draw_leaf(d, cx, cy, s, color):
    d.pieslice([cx - s, cy - s, cx + s, cy + s], 200, 20, fill=color)
    d.line([cx - s * 0.7, cy + s * 0.7, cx + s * 0.7, cy - s * 0.7], fill=BG, width=4)


def draw_chart(d, cx, cy, s, color):
    pts = [(cx - s, cy + s * 0.55), (cx - s * 0.4, cy + s * 0.1),
           (cx, cy + s * 0.35), (cx + s * 0.5, cy - s * 0.45), (cx + s, cy - s * 0.75)]
    d.line(pts, fill=color, width=6, joint="curve")
    d.polygon([(cx + s, cy - s * 0.75), (cx + s * 0.55, cy - s * 0.75),
               (cx + s, cy - s * 0.3)], fill=color)


def draw_drone(d, cx, cy, s, color):
    d.rounded_rectangle([cx - s * 0.55, cy - s * 0.25, cx + s * 0.55, cy + s * 0.25],
                        radius=10, outline=color, width=5)
    for x in (cx - s * 0.8, cx + s * 0.8):
        d.ellipse([x - s * 0.3, cy - s * 0.75, x + s * 0.3, cy - s * 0.25],
                  outline=color, width=4)
        d.line([x, cy - s * 0.25, x, cy], fill=color, width=4)
    d.ellipse([cx - s * 0.18, cy - s * 0.18, cx + s * 0.18, cy + s * 0.18], fill=color)


def draw_cyclone(d, cx, cy, s, color):
    for i, r in enumerate([s * 0.9, s * 0.65, s * 0.42, s * 0.2]):
        d.arc([cx - r, cy - r, cx + r, cy + r], i * 55, i * 55 + 250,
              fill=color, width=5)


def flag_stripes(d, x, y, w, h, colors):
    n = len(colors)
    for i, c in enumerate(colors):
        d.rectangle([x, y + i * h / n, x + w, y + (i + 1) * h / n], fill=c)


def panel(d, box, accent, label, headline, sub, icon, headline_size=27):
    x0, y0, x1, y1 = box
    d.rounded_rectangle(box, radius=18, fill=CARD)
    d.rectangle([x0, y0, x0 + 8, y1], fill=accent)
    ix, iy, ir = x0 + 62, y0 + 62, 34
    d.ellipse([ix - ir - 8, iy - ir - 8, ix + ir + 8, iy + ir + 8], fill=CARD2)
    icon(d, ix, iy, 26, accent)
    tx = x0 + 128
    d.text((tx, y0 + 22), label, font=font(19), fill=accent)
    lines = wrap(d, headline, font(headline_size), x1 - tx - 24)
    yy = y0 + 52
    for ln in lines[:3]:
        d.text((tx, yy), ln, font=font(headline_size), fill=WHITE)
        yy += headline_size + 6
    sub_lines = wrap(d, sub, font(19, bold=False), x1 - tx - 24)
    for ln in sub_lines[:2]:
        d.text((tx, yy + 4), ln, font=font(19, bold=False), fill=MUTED)
        yy += 25


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # header
    d.text((48, 34), "THE WORLD IN ONE DAY", font=font(24), fill=GOLD)
    d.text((48, 66), "FRIDAY, 20 NOVEMBER 2026", font=font(46), fill=WHITE)
    d.line([48, 132, 976, 132], fill=GOLD, width=3)
    # hero: summit
    hx0, hy0, hx1, hy1 = 48, 152, 976, 400
    d.rounded_rectangle([hx0, hy0, hx1, hy1], radius=18, fill=CARD)
    d.rectangle([hx0, hy0, hx0 + 8, hy1], fill=ACCENTS["summit"])
    draw_globe(d, 150, 272, 62, ACCENTS["summit"])
    # three small flags under the globe
    flag_stripes(d, 96, 354, 34, 22, [(178, 34, 52), (255, 255, 255), (60, 59, 110)])
    flag_stripes(d, 136, 354, 34, 22, [(222, 41, 16)])
    flag_stripes(d, 176, 354, 34, 22, [(255, 255, 255), (0, 57, 166), (213, 0, 50)])
    tx = 248
    d.text((tx, hy0 + 24), "LEAD STORY  ·  SHENZHEN, CHINA", font=font(20),
           fill=ACCENTS["summit"])
    d.text((tx, hy0 + 56), "TRUMP, PUTIN & XI SIGN", font=font(40), fill=WHITE)
    d.text((tx, hy0 + 106), "\u2018PEACE DECLARATION\u2019", font=font(40), fill=WHITE)
    d.text((tx, hy0 + 164),
           "First-ever trilateral summit ends with a joint pledge,",
           font=font(21, bold=False), fill=MUTED)
    d.text((tx, hy0 + 194),
           "as the APEC leaders\u2019 meeting closes in Shenzhen.",
           font=font(21, bold=False), fill=MUTED)
    # 2x2 grid
    gy, gh, gap = 416, 220, 16
    gw = (976 - 48 - gap) // 2
    panel(d, (48, gy, 48 + gw, gy + gh), ACCENTS["icj"], "JUSTICE  ·  THE HAGUE",
          "MYANMAR GUILTY OF GENOCIDE",
          "UN court: state guilty of genocide against the Rohingya.",
          draw_scales, 25)
    panel(d, (48 + gw + gap, gy, 976, gy + gh), ACCENTS["cop"], "CLIMATE  ·  COP31",
          "COP31 DRAFT DROPS FOSSIL-FUEL PHASE-OUT",
          "Deal text scrubs the phase-out as climate talks hit crunch time.",
          draw_leaf, 25)
    panel(d, (48, gy + gh + gap, 48 + gw, gy + 2 * gh + gap), ACCENTS["anthropic"],
          "TECH  ·  WALL STREET",
          "ANTHROPIC DEBUTS ON NASDAQ",
          "First pure-AI company lists in a record Wall Street debut.",
          draw_chart, 25)
    panel(d, (48 + gw + gap, gy + gh + gap, 976, gy + 2 * gh + gap), ACCENTS["ukraine"],
          "UKRAINE  ·  LONDON / BERLIN",
          "UK SENDS 1,000+ DRONES TO UKRAINE",
          "\u00a3260m package of long-range drones announced in Berlin.",
          draw_drone, 25)
    # bottom strip: cyclone
    by0, by1 = 888, 972
    d.rounded_rectangle([48, by0, 976, by1], radius=18, fill=CARD)
    d.rectangle([48, by0, 56, by1], fill=ACCENTS["cyclone"])
    draw_cyclone(d, 116, (by0 + by1) // 2, 30, ACCENTS["cyclone"])
    d.text((168, by0 + 12), "WEATHER  ·  INDIA", font=font(19), fill=ACCENTS["cyclone"])
    d.text((168, by0 + 40), "CYCLONE AKVAN HITS INDIA\u2019S EAST COAST",
           font=font(25), fill=WHITE)
    # footer
    d.text((48, 984), "Six stories from one day  ·  20 November 2026",
           font=font(16, bold=False), fill=MUTED)
    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
