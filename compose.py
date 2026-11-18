#!/usr/bin/env python3
"""Compose the entry image for make.fun's news-image-20261118 bounty.

Takes the AI-generated six-panel collage in art/ (no text in it) and builds the
final 1024x1024 front page: a masthead naming the date, a caption bar on each
panel naming its story, and an "also today" ticker of further headlines.
All stories are the real world news of Wednesday 18 November 2026.
Output: entry.png beside this file (PNG, at most 1 MiB, 1024x1024).
"""
from PIL import Image, ImageDraw, ImageFont

COLLAGE = "art/media-generation-news-collage-20261118-0-575adc11-892d-4182-9d7e-359c4a6ad7cb.webp"
OUT = "entry.png"

W = 1024
PAPER = (246, 240, 226)
INK = (18, 24, 38)
RED = (178, 34, 44)
BAR = (10, 18, 34, 208)
WHITE = (250, 248, 242)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

CAPTIONS = [
    "TRUMP & MODI LEAD QUAD TALKS IN MANILA",
    "UKRAINE STRIKES THE CRIMEAN BRIDGE AGAIN",
    "IRANIAN DRONES HIT U.S. RADAR IN BAHRAIN",
    "NVIDIA REVENUE DOUBLES PAST $115BN",
    "ISRAEL: EISENKOT ASKED TO FORM A GOVERNMENT",
    "SIBERIA: TRANSPORT PLANE CRASH KILLS 19",
]

TICKER = [
    "North Korea fires a ballistic missile into the Sea of Japan",
    "U.S. loses measles-free status  ·  Ebola cases double in DR Congo",
    "15,000 arrested in France's cost-of-living protests",
]


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def main():
    canvas = Image.new("RGB", (W, W), PAPER)
    d = ImageDraw.Draw(canvas, "RGBA")

    # Masthead: kicker, then the date the image sums up, big and unmissable.
    d.text((28, 16), "T H E   W O R L D   I N   O N E   P I C T U R E", font=font(BOLD, 25), fill=RED)
    d.text((26, 46), "WEDNESDAY 18 NOVEMBER 2026", font=font(BOLD, 51), fill=INK)
    d.line([(28, 106), (W - 28, 106)], fill=RED, width=4)

    # The collage: 3 columns x 2 rows of square panels.
    collage = Image.open(COLLAGE).convert("RGB")
    cw = W - 32
    ch = round(collage.height * cw / collage.width)
    collage = collage.resize((cw, ch), Image.LANCZOS)
    top = 118
    canvas.paste(collage, (16, top))
    d = ImageDraw.Draw(canvas, "RGBA")

    cell_w, cell_h = cw / 3, ch / 2
    cap_font = font(BOLD, 20)
    for i, caption in enumerate(CAPTIONS):
        cx = 16 + (i % 3) * cell_w
        cy = top + (i // 3) * cell_h
        lines = wrap(d, caption, cap_font, cell_w - 20)
        bar_h = len(lines) * 25 + 12  # the bar grows upward, never past the cell
        d.rectangle([cx, cy + cell_h - bar_h, cx + cell_w, cy + cell_h], fill=BAR)
        ly = cy + cell_h - bar_h + 6
        for line in lines:
            d.text((cx + 10, ly), line, font=cap_font, fill=WHITE)
            ly += 25

    # Footer ticker: more of the day, one line each.
    fy = top + ch + 18
    d.text((28, fy), "ALSO TODAY", font=font(BOLD, 24), fill=RED)
    tick_font = font(REG, 23)
    for j, line in enumerate(TICKER):
        d.text((28, fy + 36 + j * 31), "•  " + line, font=tick_font, fill=INK)
    d.line([(28, W - 34), (W - 28, W - 34)], fill=RED, width=3)
    d.text((28, W - 28), "The day's world news in one image — 18 November 2026",
           font=font(BOLD, 17), fill=INK)

    # Flat illustration: a 256-colour palette keeps the PNG well under 1 MiB.
    canvas.quantize(colors=256, method=Image.MEDIANCUT).convert("RGB").save(OUT, optimize=True)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
