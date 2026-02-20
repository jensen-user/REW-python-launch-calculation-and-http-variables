#!/usr/bin/env python3
"""Generate app_icon.ico for the REW SPL Meter Bridge."""

from PIL import Image, ImageDraw, ImageFont


def generate_icon():
    sizes = [256, 128, 64, 48, 32, 16]
    images = []

    for size in sizes:
        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Dark blue-gray background circle
        pad = max(1, size // 32)
        draw.ellipse(
            [pad, pad, size - pad - 1, size - pad - 1],
            fill=(30, 40, 60, 255),
        )

        # Green inner arc (SPL meter style)
        arc_margin = size // 5
        draw.arc(
            [arc_margin, arc_margin, size - arc_margin - 1, size - arc_margin - 1],
            start=200,
            end=340,
            fill=(0, 200, 80, 255),
            width=max(2, size // 16),
        )

        # "REW" text
        font_size = size // 3
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except OSError:
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
            except OSError:
                font = ImageFont.load_default()

        text = "REW"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        x = (size - text_w) // 2
        y = (size - text_h) // 2 + size // 12  # Slightly below center
        draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)

        images.append(img)

    # Save as .ico with multiple sizes
    images[0].save(
        "app_icon.ico",
        format="ICO",
        sizes=[(s, s) for s in sizes],
        append_images=images[1:],
    )
    print("Generated app_icon.ico")


if __name__ == "__main__":
    generate_icon()
