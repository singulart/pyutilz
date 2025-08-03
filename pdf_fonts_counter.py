import sys
import pymupdf
from collections import defaultdict

def flags_decomposer(flags):
    """Make font flags human readable."""
    l = []
    if flags & 2 ** 0:
        l.append("superscript")
    if flags & 2 ** 1:
        l.append("italic")
    if flags & 2 ** 2:
        l.append("serifed")
    if flags & 2 ** 3:
        l.append("monospaced")
    if flags & 2 ** 4:
        l.append("bold")
    return ", ".join(l)

# Helper to create a hashable and comparable key
def make_font_style_key(span):
    font = span["font"]
    size = round(span["size"], 2)  # rounding to avoid floating-point noise
    color = f"#{span['color']:06x}".lower()
    # print("Text: '%s'" % s["text"])
    # print(font)
    return (font, size, color)

# Open PDF and extract spans
doc = pymupdf.open(sys.argv[1])
font_usage_counter = defaultdict(int)

for page in doc:
    blocks = page.get_text("dict", flags=11)["blocks"]
    for b in blocks:
        for l in b.get("lines", []):
            for s in l.get("spans", []):
                key = make_font_style_key(s)
                font_usage_counter[key] += 1

# Print the result
for (font, size, color), count in sorted(font_usage_counter.items(), key=lambda x: -x[1]):
    print(f"'{font}', size {size}, color {color} – {count} times")

