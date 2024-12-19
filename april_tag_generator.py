#!/usr/bin/env python
import numpy as np
from moms_apriltag import TagGenerator2
from moms_apriltag.generator2 import tag_sizes_v2
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg
import svgwrite
from svgwrite import cm


def generate_fiducial(
    tag_id: int = 0,
    tag_family: str = "tag36h11",
    width: float = 5,
    print_label: bool = True,
) -> None:
    """
    Generate an april tag fiducial marker in PDF and SVG format.

            Parameters:
                    tag_id (int): ID of the desired tag
                    tag_family (str): Tag family ("tag16h5", "tag25h9", "tag36h10", "tag36h11")
                    width (float): Desired width of the fiducial marker (including white margins)
                    print_label (bool): Enables printing a label under the tag
    """

    filename = f"april_{tag_family}_{tag_id}_{width}cm"
    tg = TagGenerator2(tag_family)
    tag_per_side = tag_sizes_v2[tag_family]
    tag = tg.generate(tag_id)

    # define fiducial marker and tag size
    square_side = width / (tag_per_side + 2)
    if print_label:
        # add space for label
        height = width + 2 * square_side
    else:
        height = width
    fiducial_size = np.array((width, height))
    square_size = np.array((square_side, square_side))
    april_org = np.array((square_side, square_side))

    dwg = svgwrite.Drawing(
        filename=f"{filename}.svg", size=(fiducial_size[0] * cm, fiducial_size[1] * cm)
    )

    if print_label:
        # define font size and locations for id text and reference axes
        font_size = width / 5
        caption_org = np.array((square_side * 1.25, width + square_side * 1.25))
        axis_org = np.array((width - square_side * 2, width + square_side * 1.25))
        y_point = axis_org + np.array((0.75 * square_side, 0))
        z_point = axis_org + np.array((0, -0.75 * square_side))

        g = dwg.g(
            style=f"font-family:Comic Sans MS, Arial;font-weight:bold;font-style:oblique;stroke:black;stroke-width:1;fill:none"
        )

    dwg.add(
        dwg.rect(
            (0, 0),
            (fiducial_size[0] * cm, fiducial_size[1] * cm),
            fill="white",
            stroke="black",
            stroke_width=0.5,
        )
    )
    dwg.add(
        dwg.rect(
            (april_org[0] * cm, april_org[1] * cm),
            (tag_per_side * square_size[0] * cm, tag_per_side * square_size[1] * cm),
            fill="black",
            stroke="black",
            stroke_width=0.1,
        )
    )

    for i in range(tag_per_side):
        for j in range(tag_per_side):
            if tag[i, j] == 255:
                x = april_org[0] + square_size[0] * j
                y = april_org[0] + square_size[0] * i
                dwg.add(
                    dwg.rect(
                        (x * cm, y * cm),
                        (square_size[0] * cm, square_size[1] * cm),
                        fill="white",
                        stroke="white",
                        stroke_width=0.1,
                    )
                )

    if print_label:
        dwg.add(g)
        # write id number
        dwg.add(
            dwg.text(
                f"id: {tag_id}",
                insert=(caption_org[0] * cm, caption_org[1] * cm),
                font_size=f"{font_size}em",
            )
        )

        # draw reference for y-z axes orientation
        dwg.add(
            dwg.line(
                (axis_org[0] * cm, axis_org[1] * cm),
                (y_point[0] * cm, y_point[1] * cm),
                fill="black",
                stroke="black",
                stroke_width=font_size,
            )
        )
        dwg.add(
            dwg.text(
                "y",
                insert=(y_point[0] * 1.04 * cm, y_point[1] * cm),
                font_size=f"{font_size}em",
            )
        )

        dwg.add(
            dwg.line(
                (axis_org[0] * cm, axis_org[1] * cm),
                (z_point[0] * cm, z_point[1] * cm),
                fill="black",
                stroke="black",
                stroke_width=font_size,
            )
        )
        dwg.add(
            dwg.text(
                "z",
                insert=(z_point[0] * 0.9 * cm, z_point[1] * 1.05 * cm),
                font_size=f"{font_size}em",
            )
        )
        dwg.add(
            dwg.circle(
                (axis_org[0] * cm, axis_org[1] * cm),
                r=font_size,
                fill="black",
                stroke="black",
                stroke_width=font_size,
            )
        )

    # generate SVG file
    dwg.save()

    # generate PDF file
    drawing = svg2rlg(f"{filename}.svg")
    renderPDF.drawToFile(drawing, f"{filename}.pdf")


if __name__ == "__main__":

    tags = []
    for i in range(0, 40):
        tag_svg = generate_fiducial(tag_id=i, width=5, print_label=True)

    for i in range(100, 108):
        generate_fiducial(tag_id=i, width=10, print_label=True)
