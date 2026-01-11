from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Tuple, List, Union
from PIL import Image, ImageDraw, ImageFont
import math

ColorInput = Union[str, Tuple[int, int], Tuple[int, int, int], Tuple[int, int, int, int]]

@dataclass
class _Item:
    value: float
    color: Tuple[int, int, int, int]
    name: Optional[str] = None

def _parse_color(color: ColorInput) -> Tuple[int, int, int, int]:
    """Accept '#RRGGBB' or RGB(A) tuple/list. Return RGBA tuple with values clamped 0-255."""
    if isinstance(color, str):
        s = color.strip().lstrip("#")
        if len(s) == 3:
            # short hex like 'f00' -> 'ff0000'
            s = "".join(ch*2 for ch in s)
        if len(s) != 6:
            raise ValueError(f"Invalid hex color: {color!r}")
        r = int(s[0:2], 16)
        g = int(s[2:4], 16)
        b = int(s[4:6], 16)
        a = 255
    elif isinstance(color, (tuple, list)):
        if len(color) == 2:
            r, g = color
            b = 0
            a = 255
        elif len(color) == 3:
            r, g, b = color
            a = 255
        elif len(color) == 4:
            r, g, b, a = color
        else:
            raise ValueError("Color tuple must be length 2..4")
    else:
        raise ValueError("Unsupported color type")
    # clamp
    r = max(0, min(255, int(r)))
    g = max(0, min(255, int(g)))
    b = max(0, min(255, int(b)))
    a = max(0, min(255, int(a)))
    return (r, g, b, a)

def _darken_rgba(c: Tuple[int,int,int,int], factor: float) -> Tuple[int,int,int,int]:
    r, g, b, a = c
    r = max(0, min(255, int(r * factor)))
    g = max(0, min(255, int(g * factor)))
    b = max(0, min(255, int(b * factor)))
    return (r, g, b, a)

class Pie:
    """
    Pie chart generator with pixelated (Minecraft-like) rendering.

    Example:
        pie = Pie(200, title="Resources")
        pie.add(40, "#FF6B6B", "Red")
        pie.add(35, "#4D96FF", "Blue")
        pie.add(25, "#6BCB77", "Green")
        pie.save("chart.png")
    """

    def __init__(self, radius: int, title: Optional[str] = None, pixel_scale: int = 8):
        if radius <= 0:
            raise ValueError("radius must be > 0")
        if pixel_scale < 1:
            raise ValueError("pixel_scale must be >= 1")
        self.radius = radius
        self.title = title
        self.pixel_scale = pixel_scale
        self.items: List[_Item] = []

    def add(self, value: float, color: ColorInput, name: Optional[str] = None):
        if value < 0:
            raise ValueError("value must be non-negative")
        rgba = _parse_color(color)
        self.items.append(_Item(value, rgba, name))

    def save(self, path: str, font_path: Optional[str] = None, font_size: int = 14, bg: Tuple[int,int,int,int]=(30,30,30,255)):
        """
        Save the pie chart to path.

        - font_path: optional TTF path for labels
        - font_size: integer for label font
        - bg: background RGBA tuple
        """
        total = sum(item.value for item in self.items)
        if total <= 0:
            raise ValueError("sum of all item values must be > 0")

        # layout
        padding = 40
        cx = cy = self.radius + padding
        depth = max(1, int(self.radius * 0.15))  # layers for fake 3D

        # full image size including legend area
        img_w = self.radius * 2 + padding * 2
        img_h = self.radius * 2 + depth + padding * 2 + 60  # extra room for legend

        # create base images
        base = Image.new("RGBA", (img_w, img_h), bg)
        pie_layer = Image.new("RGBA", (img_w, img_h), (0,0,0,0))
        draw = ImageDraw.Draw(pie_layer)

        # draw depth (from bottom up) on pie_layer
        start_angle = 0.0
        # ensure deterministic order
        for d in range(depth, 0, -1):
            angle = start_angle
            for item in self.items:
                sweep = item.value / total * 360.0
                bbox = [cx - self.radius, cy - self.radius + d, cx + self.radius, cy + self.radius + d]
                draw.pieslice(bbox, angle, angle + sweep, fill=_darken_rgba(item.color, 0.72))
                angle += sweep

        # draw top layer
        angle = start_angle
        for item in self.items:
            sweep = item.value / total * 360.0
            bbox = [cx - self.radius, cy - self.radius, cx + self.radius, cy + self.radius]
            draw.pieslice(bbox, angle, angle + sweep, fill=item.color)
            angle += sweep

        # Now pixelate the pie region for blocky look:
        # crop the pie bounding box (include a small margin to preserve edges)
        margin = 2
        left = max(0, cx - self.radius - margin)
        upper = max(0, cy - self.radius - margin)
        right = min(img_w, cx + self.radius + margin)
        lower = min(img_h, cy + self.radius + depth + margin)  # include depth region
        pie_crop = pie_layer.crop((left, upper, right, lower))

        # reduce-res then enlarge using nearest neighbor to get block/pixel effect
        down_w = max(1, (right - left) // self.pixel_scale)
        down_h = max(1, (lower - upper) // self.pixel_scale)
        small = pie_crop.resize((down_w, down_h), resample=Image.BILINEAR)
        pix = small.resize((right - left, lower - upper), resample=Image.NEAREST)

        # paste pixelated pie back onto base
        base.paste(pix, (left, upper), pix)

        # draw legend and labels on base (non-pixelated for readability)
        draw_base = ImageDraw.Draw(base)

        # load font (fallback to default)
        try:
            font = ImageFont.truetype(font_path, font_size) if font_path else ImageFont.load_default()
        except Exception:
            font = ImageFont.load_default()

        # legend: small colored squares and labels
        legend_x = padding
        legend_y = cy + self.radius + depth + 10
        box_size = 14
        spacing = 4
        for item in self.items:
            # color box
            draw_base.rectangle([legend_x, legend_y, legend_x + box_size, legend_y + box_size], fill=item.color)
            # label with percent
            percent = item.value / total * 100.0
            label = f"{(item.name + ' ') if item.name else ''}{percent:.1f}%"
            draw_base.text((legend_x + box_size + 8, legend_y - 1), label, fill=(230,230,230), font=font)
            legend_y += box_size + spacing

        # title
        if self.title:
            draw_base.text((padding, 10), self.title, fill=(240,240,240), font=font)

        # Save final
        base.save(path)