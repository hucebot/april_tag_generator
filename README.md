# april_tag_generator

Code to generate april tag fiducial markers in PDF and SVG format.

## Usage

Install required packages `pip install -r requirements.txt`.

The function `generate_fiducial`, defined in `april_tag_generator.py`, create SVG and PDF files of the desired AprilTag.
Its parameters are:

- `tag_id` (int): ID of the desired tag
- `tag_family` (str): Tag family ("tag16h5", "tag25h9", "tag36h10", "tag36h11")
- `width` (float): Desired width of the fiducial marker (including white margins)
- `print_label` (bool): Enables printing a label under the tag

Script `april_tag_generator.py` shows an example generation.

Fro printing convenience, it might be necessary to assemble several tags in the same SVG. An example is given in script `april_tag_assembler.py`.
