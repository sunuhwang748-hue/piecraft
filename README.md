# piecraft

Minecraft‑style simple pie chart generator.

```python
from piecraft import Pie
<img width="100" height="161" alt="chart" src="https://github.com/user-attachments/assets/f8a4cf88-997a-4f79-ac6f-16ef06c38c36" />

pie = Pie(200, title="Resources")
pie.add(40, "#FF6B6B", "Red")
pie.add(35, "#4D96FF", "Blue")
pie.add(25, "#6BCB77", "Green")
pie.save("chart.png")
```
