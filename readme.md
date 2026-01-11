Minecraft‑style simple pie chart generator.

![chart](chart.png)

from piecraft import Pie

pie = Pie(200, title="Resources")
pie.add(40, "#FF6B6B", "Red")
pie.add(35, "#4D96FF", "Blue")
pie.add(25, "#6BCB77", "Green")
pie.save("chart.png")
