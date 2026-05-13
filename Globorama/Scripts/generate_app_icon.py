#!/usr/bin/env python3
"""Generate GLOBORAMA app icon (1024x1024) from the original web logo."""

from PIL import Image, ImageDraw, ImageFont
import os

SIZE = 1024
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(SCRIPT_DIR, "..", "..", "assets", "globorama-logo.jpg")
OUT_DIR = os.path.join(SCRIPT_DIR, "..", "Globorama", "Assets.xcassets", "AppIcon.appiconset")

# Colors sampled from the original logo
BG_TEAL = (28, 78, 82)
CREAM = (237, 228, 186)


def main():
    logo = Image.open(LOGO_PATH).convert("RGBA")

    # The globe is in the left portion of the banner — tight crop around the actual globe
    globe_crop = logo.crop((5, 8, 290, 296))
    globe_size = int(SIZE * 0.55)
    globe = globe_crop.resize((globe_size, globe_size), Image.LANCZOS)

    # Apply circular mask to remove square background edges
    circle_mask = Image.new("L", (globe_size, globe_size), 0)
    circle_draw = ImageDraw.Draw(circle_mask)
    circle_draw.ellipse((0, 0, globe_size - 1, globe_size - 1), fill=255)
    globe.putalpha(circle_mask)

    # Create icon with the original dark teal background
    icon = Image.new("RGBA", (SIZE, SIZE), (*BG_TEAL, 255))
    draw = ImageDraw.Draw(icon)

    # Round the icon corners (iOS does this automatically, but fill corners for clean export)
    corner_r = int(SIZE * 0.22)
    mask = Image.new("L", (SIZE, SIZE), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([(0, 0), (SIZE - 1, SIZE - 1)], radius=corner_r, fill=255)

    # Paste globe centered horizontally, positioned in upper portion
    globe_x = (SIZE - globe_size) // 2
    globe_y = int(SIZE * 0.08)
    icon.paste(globe, (globe_x, globe_y), globe)

    # Add "GLOBORAMA" text below the globe, matching the logo font style
    font_size = int(SIZE * 0.10)
    font = None
    for font_path in [
        "/System/Library/Fonts/Supplemental/Impact.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]:
        try:
            font = ImageFont.truetype(font_path, font_size)
            break
        except OSError:
            continue
    if font is None:
        font = ImageFont.load_default()

    text = "GLOBORAMA"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    tx = (SIZE - tw) // 2
    ty = globe_y + globe_size + int(SIZE * 0.04)
    draw.text((tx, ty), text, fill=(*CREAM, 255), font=font)

    # Add small sparkle stars like the original logo
    star_font_size = int(SIZE * 0.05)
    try:
        star_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Unicode.ttf", star_font_size)
    except OSError:
        star_font = font

    sparkle = "✦"
    # Top right sparkle
    draw.text((int(SIZE * 0.78), int(SIZE * 0.12)), sparkle, fill=(*CREAM, 200), font=star_font)
    # Bottom left sparkle (smaller)
    small_star_font_size = int(SIZE * 0.035)
    try:
        small_star_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Unicode.ttf", small_star_font_size)
    except OSError:
        small_star_font = font
    draw.text((int(SIZE * 0.15), int(SIZE * 0.82)), sparkle, fill=(*CREAM, 150), font=small_star_font)
    draw.text((int(SIZE * 0.80), int(SIZE * 0.78)), sparkle, fill=(*CREAM, 150), font=small_star_font)

    # Subtitle text
    sub_font_size = int(SIZE * 0.04)
    try:
        sub_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", sub_font_size)
    except OSError:
        sub_font = font
    subtitle = "GEOGRAPHY GAME"
    sub_bbox = draw.textbbox((0, 0), subtitle, font=sub_font)
    stw = sub_bbox[2] - sub_bbox[0]
    sx = (SIZE - stw) // 2
    sy = ty + int(SIZE * 0.12)
    draw.text((sx, sy), subtitle, fill=(*CREAM, 160), font=sub_font)

    # Flatten to RGB (no alpha channel — Apple rejects icons with transparency)
    os.makedirs(OUT_DIR, exist_ok=True)
    out_path = os.path.join(OUT_DIR, "app_icon_1024.png")
    final = Image.new("RGB", (SIZE, SIZE), BG_TEAL)
    final.paste(icon, mask=icon.split()[3])
    final.save(out_path, "PNG")
    print(f"Icon saved to {out_path}")


if __name__ == "__main__":
    main()
