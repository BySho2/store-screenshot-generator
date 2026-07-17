from __future__ import annotations

import argparse
import copy
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from PIL import Image, ImageDraw, ImageFilter, ImageFont


PRESETS = {
    "app-store-iphone-6.9": (1320, 2868),
    "app-store-iphone-6.5": (1242, 2688),
    "google-play-phone-portrait": (1080, 1920),
}
SUPPORTED_LOCALES = {"ja", "en"}
SUPPORTED_INPUTS = {".png", ".jpg", ".jpeg", ".webp"}


class ConfigError(ValueError):
    pass


@dataclass(frozen=True)
class RenderContext:
    config_path: Path
    config: dict[str, Any]
    theme: dict[str, Any]
    overwrite: bool


@dataclass(frozen=True)
class OutputTarget:
    name: str
    preset: str
    canvas_size: tuple[int, int]
    output_dir: Path
    filename: str


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ConfigError(f"File not found: {path}")
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ConfigError(f"Invalid YAML in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ConfigError(f"Expected a YAML object in {path}")
    return data


def resolve_path(base: Path, raw: str) -> Path:
    path = Path(raw).expanduser()
    return path if path.is_absolute() else (base / path).resolve()


def parse_hex_color(value: str, *, alpha: int = 255) -> tuple[int, int, int, int]:
    raw = value.lstrip("#")
    if len(raw) != 6:
        raise ConfigError(f"Color must use #RRGGBB format: {value}")
    try:
        return tuple(int(raw[i : i + 2], 16) for i in (0, 2, 4)) + (alpha,)
    except ValueError as exc:
        raise ConfigError(f"Invalid color: {value}") from exc


def output_targets(config: dict[str, Any], base: Path) -> list[OutputTarget]:
    outputs = config.get("outputs")
    if not isinstance(outputs, list) or not outputs:
        raise ConfigError("'outputs' must be a non-empty list")
    targets: list[OutputTarget] = []
    names: set[str] = set()
    for index, output in enumerate(outputs, start=1):
        if not isinstance(output, dict):
            raise ConfigError(f"Output {index} must be an object")
        name = str(output.get("name", "")).strip()
        preset = str(output.get("preset", "")).strip()
        directory = output.get("directory")
        if not name:
            raise ConfigError(f"Output {index} is missing 'name'")
        if name in names:
            raise ConfigError(f"Duplicate output name: {name}")
        names.add(name)
        if preset not in PRESETS:
            options = ", ".join(sorted(PRESETS))
            raise ConfigError(f"Unknown output preset '{preset}'. Available: {options}")
        if not directory:
            raise ConfigError(f"Output '{name}' is missing 'directory'")
        targets.append(
            OutputTarget(
                name=name,
                preset=preset,
                canvas_size=PRESETS[preset],
                output_dir=resolve_path(base, str(directory)),
                filename=str(output.get("filename", "screenshot_{locale}_{index:02d}.png")),
            )
        )
    return targets


def default_font_candidates(locale: str) -> list[str]:
    if locale == "ja":
        return [
            "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc",
            "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
            "C:/Windows/Fonts/YuGothB.ttc",
            "C:/Windows/Fonts/meiryo.ttc",
        ]
    return [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ]


def resolve_font(config: dict[str, Any], base: Path, locale: str, role: str) -> Path:
    configured = config.get("fonts", {}).get(locale, {}).get(role)
    candidates = [str(resolve_path(base, configured))] if configured else default_font_candidates(locale)
    for candidate in candidates:
        path = Path(candidate)
        if path.is_file():
            return path
    raise ConfigError(
        f"No usable {role} font found for '{locale}'. Set fonts.{locale}.{role} in config.yaml."
    )


def validate(context: RenderContext) -> None:
    config = context.config
    locales = config.get("locales")
    if not isinstance(locales, list) or not locales:
        raise ConfigError("'locales' must be a non-empty list")
    invalid = set(locales) - SUPPORTED_LOCALES
    if invalid:
        raise ConfigError(f"Initial release supports only ja and en: {sorted(invalid)}")
    if len(locales) != len(set(locales)):
        raise ConfigError("'locales' contains duplicates")
    output_targets(config, context.config_path.parent)

    slides = config.get("slides")
    if not isinstance(slides, list) or not slides:
        raise ConfigError("'slides' must be a non-empty list")
    base = context.config_path.parent
    for index, slide in enumerate(slides, start=1):
        if not isinstance(slide, dict):
            raise ConfigError(f"Slide {index} must be an object")
        source_value = slide.get("screenshot")
        if not source_value:
            raise ConfigError(f"Slide {index} is missing 'screenshot'")
        source = resolve_path(base, source_value)
        if source.suffix.lower() not in SUPPORTED_INPUTS:
            raise ConfigError(f"Unsupported screenshot format for slide {index}: {source.suffix}")
        if not source.is_file():
            raise ConfigError(f"Screenshot not found for slide {index}: {source}")
        for locale in locales:
            text = slide.get("text", {}).get(locale)
            if not isinstance(text, dict) or not str(text.get("title", "")).strip():
                raise ConfigError(f"Slide {index} is missing title text for '{locale}'")
            if not str(text.get("body", "")).strip():
                raise ConfigError(f"Slide {index} is missing body text for '{locale}'")
    for locale in locales:
        resolve_font(config, base, locale, "title")
        resolve_font(config, base, locale, "body")


def interpolate_color(stops: list[tuple[int, int, int, int]], t: float) -> tuple[int, int, int, int]:
    if len(stops) == 1:
        return stops[0]
    position = t * (len(stops) - 1)
    left = min(int(position), len(stops) - 2)
    local = position - left
    return tuple(int(stops[left][i] * (1 - local) + stops[left + 1][i] * local) for i in range(4))


def make_background(size: tuple[int, int], theme: dict[str, Any]) -> Image.Image:
    width, height = size
    colors = [parse_hex_color(value) for value in theme["background"]["colors"]]
    line = Image.new("RGBA", (1, height))
    pixels = line.load()
    for y in range(height):
        pixels[0, y] = interpolate_color(colors, y / max(height - 1, 1))
    image = line.resize(size)

    glow_color = parse_hex_color(theme["background"].get("accent_glow", "#FFFFFF"), alpha=42)
    overlay = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw.ellipse((-width // 4, -height // 10, width // 2, height // 4), fill=glow_color)
    overlay = overlay.filter(ImageFilter.GaussianBlur(max(width // 20, 16)))
    return Image.alpha_composite(image, overlay)


def japanese_break_positions(text: str) -> list[str]:
    prohibited_start = set("、。，．・：；？！)]｝〕〉》」』】〙〗〟’”ぁぃぅぇぉっゃゅょァィゥェォッャュョー")
    prohibited_end = set("([｛〔〈《「『【〘〖〝‘“")
    units: list[str] = []
    for char in text:
        if char == "\n":
            units.append("\n")
        elif units and char in prohibited_start and units[-1] != "\n":
            units[-1] += char
        elif units and units[-1][-1] in prohibited_end and units[-1] != "\n":
            units[-1] += char
        else:
            units.append(char)
    return units


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, width: int, locale: str) -> str:
    if locale == "ja":
        tokens = japanese_break_positions(text)
        separator = ""
    else:
        tokens = text.replace("\n", " \n ").split(" ")
        separator = " "
    lines: list[str] = []
    current = ""
    for token in tokens:
        if token == "\n":
            lines.append(current.rstrip())
            current = ""
            continue
        candidate = token if not current else current + separator + token
        if current and draw.textbbox((0, 0), candidate, font=font)[2] > width:
            lines.append(current.rstrip())
            current = token
        else:
            current = candidate
    if current or not lines:
        lines.append(current.rstrip())
    return "\n".join(lines)


def fit_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    font_path: Path,
    locale: str,
    max_width: int,
    max_height: int,
    max_size: int,
    min_size: int,
    max_lines: int | None = None,
) -> tuple[ImageFont.FreeTypeFont, str, int]:
    for size in range(max_size, min_size - 1, -2):
        font = ImageFont.truetype(str(font_path), size=size)
        wrapped = wrap_text(draw, text, font, max_width, locale)
        spacing = max(int(size * 0.18), 4)
        bbox = draw.multiline_textbbox((0, 0), wrapped, font=font, spacing=spacing)
        height = bbox[3] - bbox[1]
        line_count = wrapped.count("\n") + 1
        if height <= max_height and (max_lines is None or line_count <= max_lines):
            return font, wrapped, spacing
    raise ConfigError(f"Text does not fit for locale '{locale}': {text!r}")


def contain_image(image: Image.Image, max_width: int, max_height: int) -> Image.Image:
    scale = min(max_width / image.width, max_height / image.height, 1.0)
    size = (max(1, round(image.width * scale)), max(1, round(image.height * scale)))
    return image.resize(size, Image.Resampling.LANCZOS)


def add_shadow(image: Image.Image) -> Image.Image:
    padding = max(round(min(image.size) * 0.06), 28)
    canvas = Image.new("RGBA", (image.width + padding * 2, image.height + padding * 2), (0, 0, 0, 0))
    mask = image.getchannel("A")
    shadow_mask = Image.new("L", canvas.size, 0)
    shadow_mask.paste(mask, (padding, padding))
    shadow_mask = shadow_mask.filter(ImageFilter.GaussianBlur(max(padding // 3, 8)))
    canvas.paste((0, 0, 0, 115), (0, 0), shadow_mask)
    canvas.alpha_composite(image, (padding, padding))
    return canvas


def render(
    context: RenderContext,
    target: OutputTarget,
    locale: str,
    index: int,
    slide: dict[str, Any],
    base: Image.Image,
) -> Path:
    config, theme = context.config, context.theme
    width, height = target.canvas_size
    image = base.copy()
    draw = ImageDraw.Draw(image)
    margin = round(width * 0.087)
    text_width = width - margin * 2

    accent = theme.get("accent", {})
    if accent.get("enabled", True):
        draw.rounded_rectangle(
            (margin - 18, round(height * 0.048), margin - 10, round(height * 0.194)),
            radius=4,
            fill=parse_hex_color(accent["color"]),
        )

    font_base = context.config_path.parent
    title_theme = theme["headline"]
    body_theme = theme["body"]
    texts = slide["text"][locale]
    title_font, title, title_spacing = fit_text(
        draw,
        str(texts["title"]),
        resolve_font(config, font_base, locale, "title"),
        locale,
        text_width,
        round(height * 0.13),
        int(title_theme["max_size"]),
        int(title_theme["min_size"]),
        int(title_theme.get("max_lines", 3)),
    )
    title_y = round(height * 0.078)
    draw.multiline_text(
        (margin, title_y), title, font=title_font, fill=parse_hex_color(title_theme["color"]), spacing=title_spacing
    )
    title_box = draw.multiline_textbbox((margin, title_y), title, font=title_font, spacing=title_spacing)

    body_font, body, body_spacing = fit_text(
        draw,
        str(texts["body"]),
        resolve_font(config, font_base, locale, "body"),
        locale,
        text_width,
        round(height * 0.08),
        int(body_theme["max_size"]),
        int(body_theme["min_size"]),
    )
    body_y = title_box[3] + round(height * 0.018)
    draw.multiline_text(
        (margin, body_y), body, font=body_font, fill=parse_hex_color(body_theme["color"]), spacing=body_spacing
    )

    panel_top = round(height * 0.286)
    panel_bottom = height - round(height * 0.06)
    panel = theme.get("panel", {})
    if panel.get("enabled", True):
        color = parse_hex_color(panel.get("color", "#FFFFFF"), alpha=int(panel.get("opacity", 14)))
        draw.rounded_rectangle(
            (round(width * 0.066), panel_top, width - round(width * 0.066), panel_bottom),
            radius=round(width * 0.046),
            fill=color,
            outline=parse_hex_color("#FFFFFF", alpha=28),
            width=2,
        )

    source = resolve_path(context.config_path.parent, slide["screenshot"])
    with Image.open(source) as original:
        phone = original.convert("RGBA")
    device = theme["device"]
    phone = contain_image(
        phone,
        round(width * float(device["max_width_ratio"])),
        round(height * float(device["max_height_ratio"])),
    )
    rendered = add_shadow(phone) if device.get("shadow", True) else phone
    phone_x = (width - rendered.width) // 2
    phone_y = panel_top + max((panel_bottom - panel_top - rendered.height) // 2, 0)
    image.alpha_composite(rendered, (phone_x, phone_y))

    app_name_value = config.get("app", {}).get("name", "")
    if isinstance(app_name_value, dict):
        app_name = str(app_name_value.get(locale, "")).strip()
    else:
        app_name = str(app_name_value).strip()
    if app_name:
        footer_font = ImageFont.truetype(str(resolve_font(config, font_base, locale, "body")), size=24)
        footer_box = draw.textbbox((0, 0), app_name, font=footer_font)
        draw.text(
            (width - margin - (footer_box[2] - footer_box[0]), height - round(height * 0.052)),
            app_name,
            font=footer_font,
            fill=(255, 255, 255, 128) if theme["background"]["colors"][0] != "#FFFFFF" else (16, 24, 40, 128),
        )

    filename_template = target.filename
    try:
        filename = filename_template.format(locale=locale, index=index)
    except (KeyError, ValueError) as exc:
        raise ConfigError(f"Invalid output filename template: {filename_template}") from exc
    output_path = target.output_dir / locale / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.exists() and not context.overwrite:
        raise ConfigError(f"Output already exists: {output_path}. Re-run with --overwrite to replace it.")
    image.convert("RGB").save(output_path, "PNG", optimize=True)
    return output_path


def build_context(config_path: Path, overwrite: bool) -> RenderContext:
    config_path = config_path.resolve()
    config = load_yaml(config_path)
    theme_value = config.get("theme")
    if not theme_value:
        raise ConfigError("Missing 'theme' path in config")
    theme = load_yaml(resolve_path(config_path.parent, theme_value))
    context = RenderContext(
        config_path=config_path,
        config=config,
        theme=theme,
        overwrite=overwrite,
    )
    validate(context)
    return context


def run(config_path: Path, overwrite: bool = False) -> list[Path]:
    context = build_context(config_path, overwrite)
    outputs: list[Path] = []
    for target in output_targets(context.config, context.config_path.parent):
        background = make_background(target.canvas_size, context.theme)
        for locale in context.config["locales"]:
            for index, slide in enumerate(context.config["slides"], start=1):
                outputs.append(render(context, target, locale, index, slide, background))
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate localized App Store and Google Play listing images from app screenshots."
    )
    parser.add_argument("--config", type=Path, required=True, help="Path to config.yaml")
    parser.add_argument("--overwrite", action="store_true", help="Replace existing generated files")
    args = parser.parse_args()
    try:
        outputs = run(args.config, overwrite=args.overwrite)
    except (ConfigError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"Generated {len(outputs)} screenshots:")
    for path in outputs:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
