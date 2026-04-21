#!/usr/bin/env python3
"""Generate a GLOBORAMA app icon (1024x1024) using brand colors."""

from PIL import Image, ImageDraw, ImageFont
import math
import os

SIZE = 1024
CENTER = SIZE // 2
RADIUS = SIZE // 2

# Brand colors
TEAL = (55, 148, 144)
DARK_TEAL = (23, 81, 87)
PURPLE_START = (102, 126, 234)
PURPLE_END = (118, 75, 162)
CREAM = (250, 244, 208)


def lerp_color(c1, c2, t):
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))


def main():
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Gradient background (top-left purple to bottom-right teal)
    for y in range(SIZE):
        for x in range(SIZE):
            t = (x + y) / (2 * SIZE)
            color = lerp_color(PURPLE_START, TEAL, t)
            dist = math.sqrt((x - CENTER) ** 2 + (y - CENTER) ** 2)
            if dist <= RADIUS:
                img.putpixel((x, y), (*color, 255))

    # Draw a simple globe circle outline
    globe_r = int(SIZE * 0.32)
    globe_cx, globe_cy = CENTER, int(SIZE * 0.42)

    # Globe fill - slightly darker
    for y in range(globe_cy - globe_r, globe_cy + globe_r + 1):
        for x in range(globe_cx - globe_r, globe_cx + globe_r + 1):
            dist = math.sqrt((x - globe_cx) ** 2 + (y - globe_cy) ** 2)
            if dist <= globe_r:
                # Semi-transparent cream fill
                bg = img.getpixel((x, y))
                blend = lerp_color(bg[:3], CREAM, 0.15)
                img.putpixel((x, y), (*blend, 255))

    # Globe outline
    outline_width = 8
    for angle in range(360 * 4):
        a = math.radians(angle / 4)
        for w in range(outline_width):
            r = globe_r - outline_width // 2 + w
            px = int(globe_cx + r * math.cos(a))
            py = int(globe_cy + r * math.sin(a))
            if 0 <= px < SIZE and 0 <= py < SIZE:
                img.putpixel((px, py), (*CREAM, 255))

    # Horizontal line through globe (equator)
    for x in range(globe_cx - globe_r, globe_cx + globe_r + 1):
        dist = abs(x - globe_cx)
        if dist <= globe_r:
            for w in range(-3, 4):
                py = globe_cy + w
                if 0 <= py < SIZE:
                    img.putpixel((x, py), (*CREAM, 200))

    # Vertical meridian
    for y in range(globe_cy - globe_r, globe_cy + globe_r + 1):
        dist = abs(y - globe_cy)
        if dist <= globe_r:
            for w in range(-3, 4):
                px = globe_cx + w
                if 0 <= px < SIZE:
                    img.putpixel((px, y), (*CREAM, 200))

    # Curved meridian (elliptical arc)
    for angle in range(360 * 2):
        a = math.radians(angle / 2)
        rx = globe_r * 0.5
        ry = globe_r
        px = int(globe_cx + rx * math.cos(a))
        py = int(globe_cy + ry * math.sin(a))
        dist_from_center = math.sqrt((px - globe_cx) ** 2 + (py - globe_cy) ** 2)
        if dist_from_center <= globe_r and 0 <= px < SIZE and 0 <= py < SIZE:
            for w in range(-2, 3):
                if 0 <= px + w < SIZE:
                    img.putpixel((px + w, py), (*CREAM, 180))

    # Add "G" text at bottom
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia Bold.ttf", int(SIZE * 0.22))
    except OSError:
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Georgia.ttf", int(SIZE * 0.22))
        except OSError:
            font = ImageFont.load_default()

    text = "G"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = CENTER - tw // 2
    ty = int(SIZE * 0.72) - th // 2
    draw.text((tx, ty), text, fill=(*CREAM, 255), font=font)

    # Save
    out_dir = os.path.join(os.path.dirname(__file__), "..", "Globorama", "Assets.xcassets", "AppIcon.appiconset")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "app_icon_1024.png")
    img.save(out_path, "PNG")
    print(f"Icon saved to {out_path}")

    # Update Contents.json
    contents = """{
  "images" : [
    {
      "filename" : "app_icon_1024.png",
      "idiom" : "universal",
      "platform" : "ios",
      "size" : "1024x1024"
    }
  ],
  "info" : {
    "author" : "xcode",
    "version" : 1
  }
}"""
    contents_path = os.path.join(out_dir, "Contents.json")
    with open(contents_path, "w") as f:
        f.write(contents)
    print(f"Contents.json updated at {contents_path}")


if __name__ == "__main__":
    main()
