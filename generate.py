#!/usr/bin/env python3
"""Compose the vocaine v2 magazine-cover entry for news-image-20261119.

Reads assets/hero.png (original generated illustration, no text),
lays out a magazine cover (masthead date band, five story cover lines
down the left rail, hero art dominating the right), and writes
entry.png (1024x1024, <=1 MiB) next to this script.

Run: python3 generate.py
Requires Pillow (build-time only; main.py is stdlib-only).
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
MASTHEAD_H = 104
FOOTER_H = 60
RAIL_W = 332
NAVY = (14, 26, 43)
NAVY2 = (20, 38, 62)
GOLD = (201, 162, 39)
GOLD_LT = (226, 190, 90)
CREAM = (246, 241, 231)
INK = (24, 24, 22)
GREY = (90, 86, 76)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

STORIES = [
    ("SHENZHEN  ·  SUMMIT",
     "Trump, Xi, Putin hold first three-way summit",
     "Ukraine and trade lead the agenda as the three leaders meet in Shenzhen."),
    ("THE HAGUE  ·  JUSTICE",
     "World court rules on Rohingya genocide case",
     "The ICJ delivers its judgment in Gambia's case against Myanmar."),
    ("GAZA  ·  CONFLICT",
     "Israeli troops cross Gaza ceasefire line",
     "First major ground push beyond the \u2018yellow line\u2019 since the 2025 truce."),
    ("ANTALYA  ·  CLIMATE",
     "COP31 ministers race to unblock talks",
     "Negotiators push for a final text as the summit enters its decisive phase."),
    ("MARKETS  ·  TECH",
     "Anthropic prices record IPO at $83 a share",
     "The Claude maker heads for Nasdaq in one of the biggest AI listings ever."),
]


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_size(draw, text, path, start, max_w, max_lines=3):
    size = start
    while size > 12:
        fnt = font(path, size)
        if len(wrap(draw, text, fnt, max_w)) <= max_lines:
            return fnt
        size -= 1
    return font(path, 12)


def main():
    hero = Image.open(os.path.join(HERE, "assets", "hero.png")).convert("RGB")
    # Hero area: x=RAIL_W..W, y=MASTHEAD_H..H-FOOTER_H
    hw, hh = W - RAIL_W, H - MASTHEAD_H - FOOTER_H
    scaled = hero.resize((hw, round(hero.height * hw / hero.width)), Image.LANCZOS)
    # Centre-crop vertically, biased slightly upward so the map stays in frame.
    top = int((scaled.height - hh) * 0.42)
    hero_crop = scaled.crop((0, top, hw, top + hh))

    page = Image.new("RGB", (W, H), CREAM)
    page.paste(hero_crop, (RAIL_W, MASTHEAD_H))
    d = ImageDraw.Draw(page)

    # Masthead band.
    d.rectangle([0, 0, W, MASTHEAD_H], fill=NAVY)
    d.rectangle([0, MASTHEAD_H - 4, W, MASTHEAD_H], fill=GOLD)
    small = font(SANS_B, 21)
    label = "T H E   W O R L D   I N   O N E   I M A G E"
    lw = d.textlength(label, font=small)
    d.text(((W - lw) / 2, 12), label, font=small, fill=GOLD_LT)
    big = font(SERIF_B, 58)
    date = "19 NOVEMBER 2026"
    dw = d.textlength(date, font=big)
    d.text(((W - dw) / 2, 40), date, font=big, fill=(255, 255, 255))

    # Left rail: five story blocks.
    rail_top, rail_bot = MASTHEAD_H + 6, H - FOOTER_H - 4
    block_h = (rail_bot - rail_top) // len(STORIES)
    pad = 20
    text_w = RAIL_W - 2 * pad
    for i, (kicker, headline, summary) in enumerate(STORIES):
        y0 = rail_top + i * block_h
        if i:
            d.line([(pad, y0), (RAIL_W - pad, y0)], fill=(200, 190, 165), width=1)
        y = y0 + 12
        kf = font(SANS_B, 16)
        d.text((pad, y), kicker, font=kf, fill=(150, 112, 10))
        y += 24
        hf = fit_size(d, headline, SERIF_B, 26, text_w, max_lines=3)
        for line in wrap(d, headline, hf, text_w):
            d.text((pad, y), line, font=hf, fill=INK)
            y += hf.size + 4
        y += 2
        sf = fit_size(d, summary, SANS, 18, text_w, max_lines=2)
        for line in wrap(d, summary, sf, text_w):
            d.text((pad, y), line, font=sf, fill=GREY)
            y += sf.size + 5

    # Footer band.
    d.rectangle([0, H - FOOTER_H, W, H], fill=NAVY)
    d.rectangle([0, H - FOOTER_H, W, H - FOOTER_H + 3], fill=GOLD)
    ff = font(SANS_B, 19)
    foot = "THURSDAY  ·  FIVE STORIES THAT SHAPED THE WORLD"
    fw = d.textlength(foot, font=ff)
    d.text(((W - fw) / 2, H - FOOTER_H + 20), foot, font=ff, fill=GOLD_LT)

    out = os.path.join(HERE, "entry.png")
    page.save(out, "PNG", optimize=True)
    print("saved", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
