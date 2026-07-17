from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


OUTPUT_DIR = Path(__file__).parent / "screenshots"
SIZE = (1179, 2556)


def font(size: int) -> ImageFont.FreeTypeFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).is_file():
            return ImageFont.truetype(candidate, size=size)
    raise RuntimeError("No demo font found")


def base_screen(title: str) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGBA", SIZE, (245, 247, 251, 255))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((54, 74, 1125, 2482), radius=76, fill=(255, 255, 255, 255), outline=(220, 226, 236, 255), width=4)
    draw.text((110, 150), "Demo App", font=font(42), fill=(37, 99, 235, 255))
    draw.text((110, 242), title, font=font(72), fill=(16, 24, 40, 255))
    return image, draw


def create_home() -> None:
    image, draw = base_screen("Today")
    cards = [
        ("Plan the release", "09:30", (232, 240, 254, 255)),
        ("Review screenshots", "13:00", (236, 253, 245, 255)),
        ("Publish the update", "17:30", (255, 247, 237, 255)),
    ]
    for index, (label, time, color) in enumerate(cards):
        y = 430 + index * 360
        draw.rounded_rectangle((110, y, 1069, y + 280), radius=42, fill=color)
        draw.text((170, y + 72), label, font=font(46), fill=(16, 24, 40, 255))
        draw.text((170, y + 158), time, font=font(34), fill=(71, 84, 103, 255))
    draw.rounded_rectangle((110, 1840, 1069, 2190), radius=44, fill=(37, 99, 235, 255))
    draw.text((190, 1960), "Add your next task", font=font(48), fill=(255, 255, 255, 255))
    image.save(OUTPUT_DIR / "home.png")


def create_detail() -> None:
    image, draw = base_screen("Project Details")
    draw.rounded_rectangle((110, 420, 1069, 720), radius=42, fill=(238, 242, 255, 255))
    draw.text((170, 500), "Store release", font=font(52), fill=(16, 24, 40, 255))
    draw.text((170, 590), "In progress", font=font(34), fill=(37, 99, 235, 255))
    fields = ["Checklist", "Screenshots", "Localization", "Review notes"]
    for index, label in enumerate(fields):
        y = 840 + index * 250
        draw.text((140, y), label, font=font(42), fill=(52, 64, 84, 255))
        draw.line((140, y + 104, 1039, y + 104), fill=(222, 228, 238, 255), width=3)
        draw.ellipse((950, y + 10, 1010, y + 70), fill=(34, 197, 94, 255))
    image.save(OUTPUT_DIR / "detail.png")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    create_home()
    create_detail()
    print(f"Created demo screenshots in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
