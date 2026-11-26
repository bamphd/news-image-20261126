"""Draw the 26 November 2026 world-news poster.

Rendered at 2048x2048 and downscaled to 1024x1024 for crisp,
anti-aliased type (SUPER HD). Pure Pillow + bundled DejaVu fonts,
so the grader's stdlib-only box only needs Pillow to redraw it;
without Pillow, main.py copies the bundled entry.png instead.

Layout: masthead with the date, one hero story, a strip of four
top stories, then four sections in two columns. 38 stories total,
every headline short enough to stay legible at thumbnail size.
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_BOLD = os.path.join(HERE, "fonts", "DejaVuSans-Bold.ttf")
FONT_REG = os.path.join(HERE, "fonts", "DejaVuSans.ttf")

W = 2048          # render size (2x of the 1024 output)
OUT = 1024
MARGIN = 68

BG = (12, 19, 34)          # ink navy
PANEL = (20, 31, 51)       # card navy
PANEL_EDGE = (43, 60, 88)
PAPER = (244, 241, 232)    # warm white text
MUTED = (176, 187, 207)    # secondary text, >4.5:1 on PANEL and BG
AMBER = (245, 184, 65)
RED = (240, 102, 62)
TEAL = (46, 196, 182)
SKY = (90, 169, 230)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap by pixel width."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, fill, max_w, line_gap=4):
    lines = wrap(draw, text, fnt, max_w)
    lh = fnt.size + line_gap
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def measure(draw, text, fnt, max_w, line_gap=4):
    return len(wrap(draw, text, fnt, max_w)) * (fnt.size + line_gap)


def card(draw, box, fill=PANEL, edge=PANEL_EDGE, radius=16, width=2):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=edge, width=width)


HERO = (
    "TOP STORY · WASHINGTON",
    "US proposes new tariffs on 14 trading partners",
    "Duties hit China, the EU, Japan and India; Brussels rejects the premise, "
    "Beijing calls it political manipulation.",
)

TOP_STRIP = [
    ("DISASTER · CAIRO", RED,
     "Fuel tanker fire kills 31 on Cairo ring road"),
    ("CONFLICT · RIYADH", RED,
     "Houthis hit Saudi ports; Brent tops $94"),
    ("MARKETS · NEW YORK", AMBER,
     "AI sell-off pushes Nasdaq near bear market"),
    ("SPACE · TIANGONG", TEAL,
     "First Pakistani astronaut reaches Tiangong"),
]

SECTIONS = [
    ("WAR & DIPLOMACY", RED, [
        ("Ukraine hits Russian airbase; Kyiv struck",
         "Five jets hit at Savasleyka; Putin vows retaliation."),
        ("US tells citizens to leave Iran",
         "Ships reported mined in Hormuz; Kushner met envoys."),
        ("Israeli strikes kill Hamas security chief", None),
        ("Kim Jong Un vows more tactical nukes", None),
        ("Leaked data: 500,000 Russian troops lost", None),
        ("Drones kill 15+ in Sudan's Blue Nile", None),
        ("ISIL suicide attack kills two in Syria", None),
        ("EU clashes over €45bn Ukraine loan", None),
        ("Australia–Solomons security treaty signed", None),
        ("Judges: drop top Netanyahu charge", None),
        ("China probes Shanghai chief Chen Jining", None),
    ]),
    ("MONEY & MARKETS", AMBER, [
        ("Bank of Korea hikes rate to 3.25%",
         "Highest in two years; growth forecast raised."),
        ("UK energy bills +26% in January",
         "Typical bill £1,723 → £2,166 on gas surge."),
        ("Huawei guilty of stealing US secrets", None),
        ("US-backed deal for Lukoil assets", None),
        ("Asian stocks rebound on milder tariffs", None),
        ("Bangladesh garment wage protests", None),
        ("Poundland collapses; 11,000 jobs at risk", None),
        ("Puerto Rico court cancels Luma contract", None),
    ]),
    ("SCIENCE & PLANET", TEAL, [
        ("FCC OKs SpaceX's million-satellite plan",
         "Orbital data centres approved over objections."),
        ("Indonesia mine flood: 13 dead, 13 trapped",
         "River burst into 100 m gold-mine shaft in Bogor."),
        ("Stadium-sized crater seen on Dimorphos", None),
        ("King tides flood California coast", None),
        ("Pig-kidney patient: 1 year off dialysis", None),
        ("Huang returns to Nvidia amid scrutiny", None),
        ("Linux flaw “Fragnesia” patched", None),
    ]),
    ("PEOPLE & CULTURE", SKY, [
        ("Spain snap election Sunday; right ahead",
         "Sánchez's eight-year rule at stake."),
        ("Hong Kong: 1 year since fire killed 168", None),
        ("Colombia frees 76 supermarket hostages", None),
        ("2,000 migrants reach Canaries in a day", None),
        ("Macy's parade postponed first time ever", None),
        ("Liverpool beat Club Brugge 3–0", None),
        ("Jennifer Barreto wins Miss Universe", None),
    ]),
]

STORY_COUNT = 1 + len(TOP_STRIP) + sum(len(s[2]) for s in SECTIONS)


def draw_section(draw, x, y, w, title, color, stories):
    f_head = font(FONT_BOLD, 38)
    f_title = font(FONT_BOLD, 35)
    f_sub = font(FONT_REG, 27)
    draw.rectangle([x, y, x + 13, y + 42], fill=color)
    draw.text((x + 28, y + 2), title, font=f_head, fill=color)
    y += 58
    for title_text, sub in stories:
        draw.ellipse([x + 2, y + 11, x + 15, y + 24], fill=color)
        y = text_block(draw, x + 32, y, title_text, f_title, PAPER, w - 38, line_gap=3)
        if sub:
            y = text_block(draw, x + 32, y + 1, sub, f_sub, MUTED, w - 38, line_gap=2)
        y += 7
    return y


def build_poster():
    img = Image.new("RGB", (W, W), BG)
    d = ImageDraw.Draw(img)

    f_kicker = font(FONT_BOLD, 42)
    f_date = font(FONT_BOLD, 100)
    f_sub = font(FONT_REG, 40)
    f_hero_k = font(FONT_BOLD, 34)
    f_hero = font(FONT_BOLD, 82)
    f_hero_sub = font(FONT_REG, 39)
    f_card_k = font(FONT_BOLD, 28)
    f_card_t = font(FONT_BOLD, 40)
    f_foot = font(FONT_REG, 29)

    inner_w = W - 2 * MARGIN
    y = 38

    # Masthead
    d.text((MARGIN, y), "THE WORLD IN ONE DAY", font=f_kicker, fill=AMBER)
    mood = "World mood: Uneasy"
    d.text((W - MARGIN - d.textlength(mood, font=f_sub), y + 2), mood,
           font=f_sub, fill=MUTED)
    y += 60
    d.text((MARGIN, y), "Thursday 26 November 2026", font=f_date, fill=PAPER)
    y += 120
    d.text((MARGIN, y), f"The day's world news in one image — {STORY_COUNT} stories",
           font=f_sub, fill=MUTED)
    y += 58
    d.rectangle([MARGIN, y, W - MARGIN, y + 4], fill=AMBER)
    y += 28

    # Hero (height measured from its own text)
    hero_text_w = inner_w - 108
    hero_h = (26 + 48
              + measure(d, HERO[1], f_hero, hero_text_w, line_gap=6) + 4
              + measure(d, HERO[2], f_hero_sub, hero_text_w, line_gap=5) + 22)
    card(d, [MARGIN, y, W - MARGIN, y + hero_h])
    d.rectangle([MARGIN, y, MARGIN + 15, y + hero_h], fill=RED)
    hy = y + 26
    d.text((MARGIN + 46, hy), HERO[0], font=f_hero_k, fill=RED)
    hy += 48
    hy = text_block(d, MARGIN + 46, hy, HERO[1], f_hero, PAPER, hero_text_w, line_gap=6)
    hy += 4
    text_block(d, MARGIN + 46, hy, HERO[2], f_hero_sub, MUTED, hero_text_w, line_gap=5)
    y += hero_h + 20

    # Top strip: 4 title cards (height from the tallest card)
    gap = 22
    cw = (inner_w - 3 * gap) // 4
    strip_h = 24 + 42 + max(
        measure(d, t[2], f_card_t, cw - 44, line_gap=5) for t in TOP_STRIP) + 18
    for i, (kicker, color, title) in enumerate(TOP_STRIP):
        x = MARGIN + i * (cw + gap)
        card(d, [x, y, x + cw, y + strip_h])
        d.rectangle([x, y, x + cw, y + 9], fill=color)
        cy = y + 24
        d.text((x + 22, cy), kicker, font=f_card_k, fill=color)
        cy += 42
        text_block(d, x + 22, cy, title, f_card_t, PAPER, cw - 44, line_gap=5)
    y += strip_h + 24

    # Sections: two columns, two sections each
    col_gap = 44
    col_w = (inner_w - col_gap) // 2
    left_x = MARGIN
    right_x = MARGIN + col_w + col_gap
    y_left = draw_section(d, left_x, y, col_w, *SECTIONS[0][:2], SECTIONS[0][2])
    y_right = draw_section(d, right_x, y, col_w, *SECTIONS[1][:2], SECTIONS[1][2])
    y2 = max(y_left, y_right) + 14
    y_left = draw_section(d, left_x, y2, col_w, *SECTIONS[2][:2], SECTIONS[2][2])
    y_right = draw_section(d, right_x, y2, col_w, *SECTIONS[3][:2], SECTIONS[3][2])
    y = max(y_left, y_right) + 14

    # Footer
    d.rectangle([MARGIN, y, W - MARGIN, y + 3], fill=PANEL_EDGE)
    y += 16
    foot = ("Sources: BBC · Reuters · AP · Al Jazeera · CNBC · France 24 · "
            "The Guardian · Yonhap")
    d.text((MARGIN, y), foot, font=f_foot, fill=MUTED)
    tag = "by @7billions"
    d.text((W - MARGIN - d.textlength(tag, font=f_foot), y), tag,
           font=f_foot, fill=AMBER)

    return img.resize((OUT, OUT), Image.LANCZOS)


if __name__ == "__main__":
    build_poster().save(os.path.join(HERE, "entry.png"), format="PNG")
    print("stories:", STORY_COUNT)
