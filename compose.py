#!/usr/bin/env python3
"""Compose the news-image-20261122 front page with PIL.

Builds a 1024x1024 newspaper front page for Sunday 22 November 2026:
a navy masthead with the date, the five-panel hero illustration, and five
short story rows in the same left-to-right order as the hero panels.
Run: python3 compose.py  -> writes assets/entry.png (PNG, under 1 MiB).
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
HERO = os.path.join(HERE, "assets",
                    "media-generation-news-hero-20261122-0-a1bc7861-567d-415e-af0d-c1221b78d167.png")
OUT = os.path.join(HERE, "assets", "entry.png")

W, H = 1024, 1024
PAPER = (247, 243, 234)
NAVY = (18, 24, 64)
INK = (20, 20, 28)
RED = (178, 34, 34)

STORIES = [
    ("1", "G20 OPENS IN AFRICA",
     "The G20 summit opens in Johannesburg, the first ever held in Africa."),
    ("2", "TANKERS HIT IN HORMUZ",
     "At least three oil tankers struck in and near the Strait of Hormuz."),
    ("3", "SEA DRONES HIT WARSHIP",
     "Suspected Ukrainian sea drones strike a Russian warship in Libya."),
    ("4", "DRONE HITS KYIV FLATS",
     "A Russian drone hits a block in Dymer; 2 killed and 11 missing."),
    ("5", "SHURI CASTLE RESTORED",
     "Okinawa celebrates the rebuilt main hall, seven years after the fire."),
]


def font(name, size):
    for path in (f"/usr/share/fonts/truetype/dejavu/{name}.ttf",
                 f"/usr/share/fonts/{name}.ttf"):
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size)


def main():
    page = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(page)

    # Masthead: navy band with paper name and date.
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.text((512, 26), "THE WORLD IN ONE PAGE",
           font=font("DejaVuSans-Bold", 44), fill=PAPER, anchor="mt")
    d.text((512, 82), "SUNDAY 22 NOVEMBER 2026  |  FIVE STORIES, ONE DAY",
           font=font("DejaVuSans-Bold", 22), fill=(212, 196, 140), anchor="mt")
    d.line([28, 118, W - 28, 118], fill=RED, width=4)

    # Hero illustration band.
    hero = Image.open(HERO).convert("RGB")
    hero = hero.resize((W - 56, 300))
    page.paste(hero, (28, 134))
    d.rectangle([28, 134, W - 28, 434], outline=NAVY, width=3)

    # Story rows, one per hero panel, in the same left-to-right order.
    y = 452
    row_h = 106
    for num, head, sub in STORIES:
        d.rectangle([28, y, 76, y + 58], fill=NAVY)
        d.text((52, y + 29), num, font=font("DejaVuSans-Bold", 34),
               fill=PAPER, anchor="mm")
        d.text((96, y + 6), head, font=font("DejaVuSans-Bold", 30), fill=INK)
        d.text((96, y + 48), sub, font=font("DejaVuSans", 21), fill=(70, 70, 80))
        d.line([28, y + row_h - 14, W - 28, y + row_h - 14],
               fill=(200, 192, 172), width=2)
        y += row_h

    # Footer line.
    d.text((512, 992), "G20  •  HORMUZ  •  LIBYA  •  DYMER  •  SHURI CASTLE",
           font=font("DejaVuSans-Bold", 18), fill=(90, 90, 100), anchor="mm")

    page.save(OUT, format="PNG", optimize=True)
    size = os.path.getsize(OUT)
    print(f"wrote {OUT}: {page.size}, {size} bytes")
    assert page.size == (1024, 1024)
    assert size <= 1048576, "entry.png exceeds the 1 MiB gate limit"


if __name__ == "__main__":
    main()
