#!/usr/bin/env python3
"""Draw the 24 November 2026 world-news front page (1024x1024 PNG).

Original design, drawn from scratch with PIL: a newspaper front page with
a masthead, a big lead panel on the Iran war blockade showdown, and nine
region blocks, each with its own small drawn scene and short headlines.
Every headline comes from the verified 24 Nov 2026 shortlist.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

CREAM = (247, 242, 231)
PAPER = (255, 253, 247)
INK = (20, 33, 61)
RED = (178, 34, 34)
GOLD = (201, 162, 39)
GREY = (90, 96, 108)
SKY = (186, 214, 235)
SEA = (46, 98, 140)

F_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(size, bold=False):
    return ImageFont.truetype(F_BOLD if bold else F_REG, size)


def wrap(d, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_lines(d, text, max_w, start_size, min_size=12):
    """Wrap text, shrinking the font until every line fits (or min size)."""
    size = start_size
    while size > min_size:
        fnt = font(size)
        lines = wrap(d, text, fnt, max_w)
        if all(d.textlength(ln, font=fnt) <= max_w for ln in lines):
            return lines, fnt
        size -= 1
    fnt = font(min_size)
    return wrap(d, text, fnt, max_w), fnt


def tint(rgb, f=0.88):
    """Mix a colour toward white for scene backgrounds."""
    return tuple(int(255 - (255 - c) * (1 - f) + c * f * 0 + c) if False else
                 int(c + (255 - c) * f) for c in rgb)


# ---------------------------------------------------------------- scenes
def scene_lead(d, x, y, w, h):
    """Oil tanker, warship and a dashed blockade line on the sea."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 231, 240))
    d.ellipse([x + w - 52, y + 8, x + w - 16, y + 44], fill=(244, 196, 66))
    d.rectangle([x, y + h - 62, x + w, y + h], fill=SEA)
    d.rectangle([x, y + h - 62, x + w, y + h - 58], fill=(120, 170, 205))
    # tanker (left)
    tx, ty = x + 16, y + h - 96
    d.polygon([(tx, ty + 34), (tx + 150, ty + 34), (tx + 138, ty + 58),
               (tx + 12, ty + 58)], fill=(38, 48, 66))
    d.rectangle([tx + 8, ty + 22, tx + 142, ty + 34], fill=(178, 34, 34))
    for i in range(4):
        d.rectangle([tx + 16 + i * 32, ty + 2, tx + 42 + i * 32, ty + 22],
                    fill=(232, 236, 240), outline=(150, 160, 172))
    d.rectangle([tx + 128, ty - 12, tx + 140, ty + 22], fill=(90, 96, 108))
    # warship (right)
    wx, wy = x + w - 128, y + h - 104
    d.polygon([(wx, wy + 40), (wx + 118, wy + 40), (wx + 104, wy + 62),
               (wx + 14, wy + 62)], fill=(96, 104, 116))
    d.rectangle([wx + 34, wy + 16, wx + 78, wy + 40], fill=(120, 128, 140))
    d.rectangle([wx + 52, wy - 8, wx + 58, wy + 16], fill=(96, 104, 116))
    d.polygon([(wx + 58, wy - 8), (wx + 76, wy - 2), (wx + 58, wy + 4)],
              fill=(178, 34, 34))
    # dashed blockade line between the ships
    bx = x + 150
    for i in range(5):
        yy = y + 58 + i * 0
        d.line([(bx, y + 52), (bx, y + 52)], fill=RED, width=1)
    for i in range(6):
        d.line([(x + 168 + i * 14, y + 46), (x + 168 + i * 14 + 8, y + 46)],
               fill=RED, width=3)
    d.text((x + 168, y + 20), "BLOCKADE", font=font(13, True), fill=RED)
    # gulls
    for gx, gy in [(x + 60, y + 24), (x + 92, y + 36), (x + 210, y + 18)]:
        d.arc([gx, gy, gx + 16, gy + 8], 200, 340, fill=INK, width=2)


def scene_parliament(d, x, y, w, h):
    """Parliament building with dome and tricolour flag (fits 62px strip)."""
    d.rectangle([x, y, x + w, y + h], fill=tint((180, 83, 9)))
    bx, by = x + 60, y + 34
    d.rectangle([bx, by, bx + 210, by + 24], fill=(214, 198, 164),
                outline=(150, 130, 100))
    for i in range(6):
        cx = bx + 12 + i * 34
        d.rectangle([cx, by + 4, cx + 12, by + 24], fill=(255, 253, 247),
                    outline=(180, 170, 150))
    d.rectangle([bx - 8, by + 24, bx + 218, by + 28], fill=(120, 100, 70))
    d.pieslice([bx + 82, y + 14, bx + 128, y + 38], 180, 360,
               fill=(201, 162, 39), outline=(150, 120, 40))
    d.rectangle([bx + 102, y + 2, bx + 106, y + 14], fill=INK)
    d.rectangle([bx + 106, y + 2, bx + 128, y + 6], fill=(255, 153, 51))
    d.rectangle([bx + 106, y + 6, bx + 128, y + 10], fill=(255, 255, 255))
    d.rectangle([bx + 106, y + 10, bx + 128, y + 14], fill=(19, 136, 8))


def scene_capitol(d, x, y, w, h):
    """Capitol dome beside a gold $ coin (US aid)."""
    d.rectangle([x, y, x + w, y + h], fill=tint((153, 27, 27)))
    bx, by = x + 30, y + 34
    d.rectangle([bx, by, bx + 150, by + 24], fill=(228, 222, 206),
                outline=(160, 150, 130))
    for i in range(5):
        cx = bx + 12 + i * 28
        d.rectangle([cx, by + 4, cx + 10, by + 24], fill=(255, 253, 247),
                    outline=(180, 170, 150))
    d.pieslice([bx + 55, y + 12, bx + 95, y + 38], 180, 360,
               fill=(255, 253, 247), outline=(150, 150, 150))
    d.rectangle([bx + 72, y + 2, bx + 78, y + 12], fill=INK)
    d.ellipse([x + w - 78, y + 8, x + w - 18, y + 56], fill=(244, 196, 66),
              outline=(160, 120, 20), width=2)
    d.text((x + w - 62, y + 18), "$", font=font(26, True), fill=(120, 84, 10))


def scene_whitehouse(d, x, y, w, h):
    """White House front with flag (fits 62px strip)."""
    d.rectangle([x, y, x + w, y + h], fill=(168, 188, 214))
    bx, by = x + 70, y + 34
    d.rectangle([bx, by, bx + 190, by + 24], fill=(255, 255, 255),
                outline=(170, 175, 185))
    d.rectangle([bx + 70, y + 26, bx + 120, by], fill=(255, 255, 255),
                outline=(170, 175, 185))
    d.polygon([(bx + 66, y + 26), (bx + 124, y + 26), (bx + 95, y + 16)],
              fill=(235, 235, 235), outline=(170, 175, 185))
    for i in range(5):
        cx = bx + 14 + i * 34
        d.rectangle([cx, by + 4, cx + 10, by + 24], fill=(225, 228, 232),
                    outline=(190, 195, 200))
    d.rectangle([bx + 92, y + 4, bx + 96, y + 16], fill=INK)
    for i, col in enumerate([(178, 34, 34), (255, 255, 255), (178, 34, 34),
                             (255, 255, 255), (178, 34, 34)]):
        d.rectangle([bx + 96, y + 4 + i * 3, bx + 118, y + 7 + i * 3],
                    fill=col)
    d.rectangle([bx + 96, y + 4, bx + 105, y + 13], fill=(30, 58, 95))


def scene_satellite(d, x, y, w, h):
    """Satellite over the Earth, defending space."""
    d.rectangle([x, y, x + w, y + h], fill=(16, 24, 48))
    import random
    rnd = random.Random(24)
    for _ in range(26):
        sx = x + rnd.randint(4, w - 4)
        sy = y + rnd.randint(4, h - 30)
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(255, 255, 255))
    d.pieslice([x - 40, y + h - 26, x + w + 40, y + h + 90], 180, 360,
               fill=(46, 98, 180))
    d.arc([x - 40, y + h - 26, x + w + 40, y + h + 90], 180, 360,
          fill=(120, 170, 205), width=2)
    cx, cy = x + w // 2, y + 26
    d.rectangle([cx - 52, cy - 4, cx - 14, cy + 10], fill=(30, 58, 140))
    d.rectangle([cx + 14, cy - 4, cx + 52, cy + 10], fill=(30, 58, 140))
    d.rectangle([cx - 14, cy - 8, cx + 14, cy + 12], fill=(200, 205, 212))
    d.rectangle([cx - 4, cy + 12, cx + 4, cy + 22], fill=(200, 205, 212))
    d.line([(cx, cy - 8), (cx, cy - 20)], fill=(255, 255, 255), width=2)
    d.ellipse([cx - 3, cy - 23, cx + 3, cy - 17], fill=(244, 196, 66))


def scene_jets(d, x, y, w, h):
    """Two jets over the sea, dashed flight path."""
    d.rectangle([x, y, x + w, y + h], fill=(186, 214, 235))
    d.ellipse([x + 20, y + 8, x + 70, y + 22], fill=(255, 255, 255))
    d.ellipse([x + 240, y + 30, x + 300, y + 44], fill=(255, 255, 255))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(120, 170, 205))
    for i in range(14):
        d.line([(x + 8 + i * 23, y + 44), (x + 8 + i * 23 + 12, y + 44)],
               fill=(255, 255, 255), width=2)
    for jx, jy, s in [(x + 90, y + 22, 1.0), (x + 190, y + 36, 0.8)]:
        L = int(46 * s)
        d.polygon([(jx, jy), (jx + L, jy + int(7 * s)),
                   (jx + L - 8, jy + int(12 * s)), (jx + 10, jy + int(9 * s))],
                  fill=(52, 58, 68))
        d.polygon([(jx + 14, jy - int(6 * s)), (jx + 26, jy),
                   (jx + 14, jy + int(4 * s))], fill=(52, 58, 68))


def scene_blast(d, x, y, w, h):
    """Restaurant building with a small blast burst and smoke."""
    d.rectangle([x, y, x + w, y + h], fill=tint((15, 118, 110)))
    bx, by = x + 70, y + 30
    d.rectangle([bx, by, bx + 190, by + 34], fill=(120, 118, 110))
    for i in range(5):
        d.rectangle([bx + 12 + i * 36, by + 8, bx + 30 + i * 36, by + 22],
                    fill=(255, 240, 180))
    cx, cy = x + w // 2, y + 14
    for r, col in [(20, (255, 122, 26)), (14, (255, 196, 66)),
                   (8, (255, 240, 180))]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    for px, py, r in [(x + 44, y + 10, 8), (x + 60, y + 6, 6),
                      (x + w - 54, y + 12, 7), (x + w - 34, y + 8, 6)]:
        d.ellipse([px - r, py - r, px + r, py + r], fill=(170, 170, 170))


def scene_scales(d, x, y, w, h):
    """Scales of justice on a plinth."""
    d.rectangle([x, y, x + w, y + h], fill=tint((146, 64, 14)))
    cx = x + w // 2
    d.rectangle([cx - 70, y + h - 12, cx + 70, y + h - 4], fill=(120, 100, 70))
    d.rectangle([cx - 3, y + 12, cx + 3, y + h - 12], fill=(120, 100, 70))
    d.ellipse([cx - 6, y + 6, cx + 6, y + 18], fill=(201, 162, 39))
    d.line([(cx - 62, y + 20), (cx + 62, y + 20)], fill=(120, 100, 70),
           width=4)
    for s in (-1, 1):
        px = cx + s * 58
        d.line([(px, y + 20), (px - 14, y + 38)], fill=(120, 100, 70), width=2)
        d.line([(px, y + 20), (px + 14, y + 38)], fill=(120, 100, 70), width=2)
        d.pieslice([px - 16, y + 34, px + 16, y + 52], 0, 180,
                   fill=(201, 162, 39))


def scene_chart(d, x, y, w, h):
    """Market chart: steep rise, then a fall."""
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    for gy in range(1, 4):
        yy = y + gy * h // 4
        d.line([(x + 8, yy), (x + w - 8, yy)], fill=(230, 230, 230), width=1)
    pts_up = [(x + 14, y + h - 12), (x + 80, y + h - 22), (x + 150, y + 34),
              (x + 205, y + 12)]
    d.line(pts_up, fill=(22, 163, 74), width=4, joint="curve")
    pts_dn = [(x + 205, y + 12), (x + 260, y + 30), (x + w - 14, y + 44)]
    d.line(pts_dn, fill=(220, 38, 38), width=4, joint="curve")
    d.polygon([(x + w - 26, y + 32), (x + w - 8, y + 44), (x + w - 26, y + 52)],
              fill=(220, 38, 38))
    d.rectangle([x + 14, y + 8, x + 44, y + 26], fill=(30, 58, 95))
    d.text((x + 19, y + 10), "NV", font=font(12, True), fill=(255, 255, 255))


def scene_cricket(d, x, y, w, h):
    """Cricket stumps, bat and ball on the pitch."""
    d.rectangle([x, y, x + w, y + h], fill=(34, 120, 60))
    d.rectangle([x, y + h - 18, x + w, y + h], fill=(120, 90, 50))
    sx = x + 60
    for i in range(3):
        d.rectangle([sx + i * 12, y + 22, sx + i * 12 + 7, y + 52],
                    fill=(244, 196, 66))
    d.rectangle([sx, y + 18, sx + 32, y + 22], fill=(244, 196, 66))
    # bat, leaning
    bx, by = x + 150, y + 14
    d.polygon([(bx, by), (bx + 16, by), (bx + 10, by + 30),
               (bx - 6, by + 30)], fill=(210, 180, 140),
              outline=(120, 90, 50))
    d.rectangle([bx + 3, by - 12, bx + 9, by + 2], fill=(120, 90, 50))
    # red ball flying
    d.ellipse([x + w - 62, y + 12, x + w - 38, y + 36], fill=(178, 34, 34))
    d.arc([x + w - 62, y + 12, x + w - 38, y + 36], 90, 270,
          fill=(255, 255, 255), width=2)


# ---------------------------------------------------------------- content
LEAD_BULLETS = [
    "Vance & Rubio meet Qatar PM at White House",
    "Iran: will use \u201call tools\u201d against US blockade",
    "Gaza strike kills Hamas security chief + 6",
]

# (header, colour, scene fn, [headline lines])
REGIONS = [
    ("SOUTH ASIA", (180, 83, 9), scene_parliament, [
        "India: Winter Session delay questioned",
        "HRW: Modi govt weakened checks on it",
        "Nepal: 5.4 quake in Koshi, felt in India",
        "Pakistan: 4.1 quake in the morning",
        "Hasina to return 16 Dec; \u2018in handcuffs\u2019",
    ]),
    ("MIDDLE EAST", (153, 27, 27), scene_capitol, [
        "Huckabee doubts $3.8bn aid ending",
        "US may train Syrian soldiers in demining",
    ]),
    ("US / AMERICAS", (30, 58, 95), scene_whitehouse, [
        "Trump: DOJ to speed up death sentences",
        "Rep. Gomez to resign after ethics probe",
        "Omar home-search papers unsealed",
        "US citizen wrongly deported by ICE",
        "Pentagon: Canada \u2018must get serious\u2019",
        "Ex-Hegseth aide: Hegseth should resign",
    ]),
    ("EUROPE", (29, 78, 216), scene_satellite, [
        "NATO: will defend against space threats",
        "UK sanctions 5 Myanmar generals",
        "Break-in at Prince William\u2019s Anmer Hall",
        "GTA VI hacker gets 7 years, walks free",
        "EU: ban Russian flags at sports events",
    ]),
    ("EAST ASIA", (109, 40, 217), scene_jets, [
        "Russian jets enter S. Korea defence zone",
        "Japan pays full 2027 ICC bill this year",
        "China cobalt firms race Congo export ban",
        "N. Korea threatens to shut Swiss office",
        "China AI campaign targets Taiwan vote",
    ]),
    ("SE ASIA & PACIFIC", (15, 118, 110), scene_blast, [
        "Hanoi blast kills 6, injures 10",
        "Landmine deaths hit 5-year high: 7,000",
        "US blacklists Singapore cloud firm",
    ]),
    ("AFRICA", (146, 64, 14), scene_scales, [
        "Amnesty: Tigray strikes may be war crimes",
        "Kenya & DR Congo restore full relations",
        "Uebert Angel arrested in Zimbabwe",
    ]),
    ("BUSINESS & TECH", (22, 101, 52), scene_chart, [
        "Nvidia soars 31.5% Mon, falls 5\u20138% Tue",
        "Anthropic shares fall below IPO price",
        "Markets: Nasdaq \u22121.4%, S&P \u22120.9%",
        "Goldman: gold $4,650 by 2027",
    ]),
    ("SPORT", (157, 23, 77), scene_cricket, [
        "England beat Australia by 8 wkts",
        "Sooryavanshi, 15, smashes 204 off 53",
        "2031 Women\u2019s World Cup: USA, Mexico + 2",
    ]),
]


def draw_scene(fn, x, y, w, h):
    """Render a scene onto a temp image (clipped) and return it."""
    tmp = Image.new("RGB", (w, h), PAPER)
    d2 = ImageDraw.Draw(tmp)
    fn(d2, 0, 0, w, h)
    return tmp


def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    # outer frame
    d.rectangle([4, 4, W - 5, H - 5], outline=INK, width=3)

    # ---- masthead
    title = "THE WORLD IN ONE DAY"
    tf = font(46, True)
    d.text(((W - d.textlength(title, font=tf)) / 2, 10), title,
           font=tf, fill=INK)
    sub = "TUESDAY 24 NOVEMBER 2026  \u00b7  39 STORIES FROM 9 REGIONS"
    sf = font(19, True)
    d.text(((W - d.textlength(sub, font=sf)) / 2, 62), sub,
           font=sf, fill=RED)
    d.line([(40, 88), (W - 40, 88)], fill=RED, width=3)

    # ---- lead panel
    lx, ly, lw, lh = 12, 96, 1000, 196
    d.rectangle([lx, ly, lx + lw, ly + lh], fill=PAPER, outline=RED, width=2)
    d.rectangle([lx, ly, lx + 8, ly + lh], fill=RED)
    img.paste(draw_scene(scene_lead, 0, 0, 330, lh - 16),
              (lx + 14, ly + 8))
    tx = lx + 360
    d.text((tx, ly + 12), "LEAD \u2014 IRAN WAR", font=font(20, True), fill=RED)
    d.text((tx, ly + 38), "THE BLOCKADE SHOWDOWN", font=font(25, True),
           fill=INK)
    by = ly + 76
    for bullet in LEAD_BULLETS:
        d.ellipse([tx, by + 6, tx + 8, by + 14], fill=RED)
        lines, bf = fit_lines(d, bullet, lw - 380, 17)
        yy = by
        for ln in lines:
            d.text((tx + 18, yy), ln, font=bf, fill=INK)
            yy += 22
        by = yy + 4
    d.text((tx, ly + lh - 26),
           "Blockade first imposed 13 Apr, reinstated 14 Jul 2026.",
           font=font(13), fill=GREY)

    # ---- region grid: 3 x 3
    gx, gy = 12, 300
    cw, ch, gap = 330, 228, 5
    for i, (name, colour, scene, lines) in enumerate(REGIONS):
        cx = gx + (i % 3) * (cw + gap)
        cy = gy + (i // 3) * (ch + gap)
        d.rectangle([cx, cy, cx + cw, cy + ch], fill=PAPER,
                    outline=(200, 192, 175), width=1)
        d.rectangle([cx, cy, cx + cw, cy + 30], fill=colour)
        hf = font(16, True)
        d.text((cx + 10, cy + 6), name, font=hf, fill=(255, 255, 255))
        img.paste(draw_scene(scene, 0, 0, cw - 2, 62), (cx + 1, cy + 31))
        ly2 = cy + 100
        for story in lines:
            sl, sfnt = fit_lines(d, story, cw - 20, 14)
            assert len(sl) == 1, f"headline wraps: {story!r} -> {sl}"
            d.text((cx + 10, ly2), sl[0], font=sfnt, fill=INK)
            ly2 += 19
        assert ly2 <= cy + ch - 4, f"cell overflow: {name}"

    # ---- footer
    foot = ("All 39 stories happened or were first reported on 24 November 2026  "
            "\u00b7  Sources: AP, Reuters, BBC, NYT, WSJ, SCMP, Cricinfo")
    ff = font(12)
    d.text(((W - d.textlength(foot, font=ff)) / 2, 1002), foot,
           font=ff, fill=GREY)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
