"""
Transforms rectangular image into 1:1 square format suitable for Instagram
"""

from PIL import Image
import sys
from pathlib import Path

PREFIX = 'SQ_'

imagepath = sys.argv[1]
if not imagepath:
    print("Usage: python3 instasquare.py /path/to/folder/with/images")
    sys.exit(1)
src_path = Path(imagepath)
for g in src_path.glob('**/*'):
    suffix = g.suffix
    stem = g.stem
    if stem[:3] == PREFIX:
        continue
    parent = g.parent
    new_name = "".join([PREFIX, str(stem), suffix])
    new_place = Path(parent, new_name)

    im = Image.open(str(g), 'r')
    (w, h) = im.size
    greater = w if w > h else h
    white = Image.new('RGB', (greater, greater), 'white')
    bg_w, bg_h = white.size
    offset = ((bg_w - w) // 2, (bg_h - h) // 2)
    white.paste(im, offset)
    white.save(str(new_place))
