
from PIL import Image, ImageDraw, ImageFont
import math

class Pie:
    def __init__(self, radius: int, title: str | None = None):
        self.radius = radius
        self.title = title
        self.items = []  # (value, color, name)

    def add(self, value: float, color: str, name: str | None = None):
        self.items.append((value, color, name))

    def save(self, path: str):
        size = self.radius * 2 + 80
        depth = int(self.radius * 0.15)  # fake 3D depth

        img = Image.new("RGBA", (size, size + depth + 60), (30, 30, 30, 255))
        draw = ImageDraw.Draw(img)

        total = sum(v for v, _, _ in self.items)
        cx = cy = self.radius + 40

        start = 0
        # draw depth layers
        for d in range(depth, 0, -1):
            angle = start
            for v, color, _ in self.items:
                sweep = v / total * 360
                draw.pieslice(
                    [cx - self.radius, cy - self.radius + d,
                     cx + self.radius, cy + self.radius + d],
                    angle, angle + sweep,
                    fill=_darken(color, 0.75)
                )
                angle += sweep

        # draw top
        angle = start
        for v, color, _ in self.items:
            sweep = v / total * 360
            draw.pieslice(
                [cx - self.radius, cy - self.radius,
                 cx + self.radius, cy + self.radius],
                angle, angle + sweep,
                fill=color
            )
            angle += sweep

        # legend
        y = cy + self.radius + depth + 10
        x = 40
        for v, color, name in self.items:
            draw.rectangle([x, y, x + 14, y + 14], fill=color)
            label = f"{name + ' ' if name else ''}{v / total * 100:.1f}%"
            draw.text((x + 20, y - 1), label, fill=(230, 230, 230))
            y += 20

        # title
        if self.title:
            draw.text((40, 10), self.title, fill=(240, 240, 240))

        img.save(path)

def _darken(hex_color: str, factor: float):
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    r = int(r * factor)
    g = int(g * factor)
    b = int(b * factor)
    return (r, g, b, 255)
