"""
Transforms rectangular image into 1:1 square format suitable for Instagram
"""

from PIL import Image
import sys

imagepath = sys.argv[1]
if not imagepath:
    print("Usage: python3 instasquare.py xyz.png")
    sys.exit(1)
im = Image.open(imagepath, 'r')
(w, h) = im.size
greater = w if w > h else h
white = Image.new('RGB', (greater, greater), 'white')
bg_w, bg_h = white.size
offset = ((bg_w - w) // 2, (bg_h - h) // 2)
white.paste(im, offset)
white.save('result.png')
