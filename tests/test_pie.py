import tempfile
import os
from PIL import Image
from piecraft import Pie

def test_create_chart_file_and_size():
    pie = Pie(120, title="Test")
    pie.add(1, "#FF0000", "A")
    pie.add(2, "#00FF00", "B")
    fd, path = tempfile.mkstemp(suffix=".png")
    os.close(fd)
    try:
        pie.save(path)
        img = Image.open(path)
        assert img.size[0] >= 240  # expected width at least 2*radius
        # basic sanity: ensure file is not empty and has some non-background pixels
        pixels = img.getdata()
        # count non-background (not equal to dark background)
        non_bg = sum(1 for p in pixels if p[:3] != (30,30,30))
        assert non_bg > 0
    finally:
        os.remove(path)