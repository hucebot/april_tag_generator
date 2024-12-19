#!/usr/bin/env python
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg
import svgutils.transform as sg
from svgutils.compose import *

x_px = 189
y_px = 227

fig = sg.SVGFigure()

tags = []
for i in range(40):
    tag = sg.fromfile(f"april_tag36h11_{i}_5cm.svg")
    plt = tag.getroot()
    plt.moveto((i % 8) * x_px, (i // 8) * y_px)
    tags.append(plt)
fig.append(tags)
fig.save("table_small_tags.svg")

fig = sg.SVGFigure()

tags = []
for i in range(8):
    tag = sg.fromfile(f"april_tag36h11_{100+i}_10cm.svg")
    plt = tag.getroot()
    plt.moveto((i % 4) * x_px * 2, (i // 4) * y_px * 2)
    tags.append(plt)
fig.append(tags)
fig.save("table_big_tags.svg")
