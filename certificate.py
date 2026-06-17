# -*- coding: utf-8 -*-
"""
📜 Sertifikat rasmini (PNG) chizadi.

make_certificate(...) BytesIO qaytaradi — uni Telegram'ga rasm sifatida
yuborish mumkin. Pillow (PIL) kutubxonasidan foydalanadi.
"""

import os
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

# O'lcham va ranglar
W, H = 1200, 860
CREAM = (251, 247, 239)
NAVY = (26, 60, 110)
GOLD = (193, 150, 40)
GRAY = (90, 90, 90)

# Shrift qidiriladigan papkalar (Windows / Linux / Mac)
_FONT_DIRS = [
    "C:/Windows/Fonts",
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts/truetype/liberation",
    "/Library/Fonts",
]


def _font(names, size):
    """Berilgan nomlardan birinchi topilgan shriftni yuklaydi, bo'lmasa standart."""
    for d in _FONT_DIRS:
        for n in names:
            path = os.path.join(d, n)
            if os.path.exists(path):
                try:
                    return ImageFont.truetype(path, size)
                except Exception:
                    pass
    return ImageFont.load_default()


def _bold(size):
    return _font(["arialbd.ttf", "DejaVuSans-Bold.ttf", "LiberationSans-Bold.ttf"], size)


def _regular(size):
    return _font(["arial.ttf", "DejaVuSans.ttf", "LiberationSans-Regular.ttf"], size)


def _fit(draw, text, make_font, start_size, max_width, min_size=28):
    """Matn max_width ga sig'guncha shrift o'lchamini kichraytiradi."""
    size = start_size
    font = make_font(size)
    while size > min_size and draw.textlength(text, font=font) > max_width:
        size -= 4
        font = make_font(size)
    return font


def make_certificate(name: str, level_label: str, percent: int, date_str: str) -> BytesIO:
    """Sertifikat PNG rasmini yaratadi va BytesIO qaytaradi."""
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # Ramka
    draw.rectangle([25, 25, W - 25, H - 25], outline=GOLD, width=10)
    draw.rectangle([45, 45, W - 45, H - 45], outline=NAVY, width=2)

    cx = W // 2

    # Sarlavha
    draw.text((cx, 130), "CERTIFICATE", font=_bold(74), fill=NAVY, anchor="mm")
    draw.text((cx, 200), "OF ACHIEVEMENT", font=_regular(34), fill=GOLD, anchor="mm")
    draw.line([(cx - 200, 240), (cx + 200, 240)], fill=GOLD, width=3)

    # Ism
    draw.text((cx, 300), "This certificate is proudly presented to",
              font=_regular(26), fill=GRAY, anchor="mm")
    name_font = _fit(draw, name, _bold, 64, W - 240)
    draw.text((cx, 370), name, font=name_font, fill=NAVY, anchor="mm")
    draw.line([(cx - 260, 415), (cx + 260, 415)], fill=GRAY, width=1)

    # Daraja
    draw.text((cx, 470), "for successfully completing the",
              font=_regular(24), fill=GRAY, anchor="mm")
    lvl_font = _fit(draw, f"{level_label} English Level", _bold, 40, W - 240)
    draw.text((cx, 525), f"{level_label} English Level", font=lvl_font, fill=NAVY, anchor="mm")

    # Ball
    draw.text((cx, 600), f"with a score of {percent}%",
              font=_bold(34), fill=GOLD, anchor="mm")

    # Pastki qism: sana va footer
    draw.text((cx, 720), f"Date: {date_str}", font=_regular(24), fill=GRAY, anchor="mm")
    draw.text((cx, 770), "English Learning Bot  ·  @englishlevel_test_bot",
              font=_regular(22), fill=NAVY, anchor="mm")

    bio = BytesIO()
    img.save(bio, format="PNG")
    bio.seek(0)
    bio.name = "certificate.png"
    return bio
