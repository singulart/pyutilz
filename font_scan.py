import os
from fontTools.ttLib import TTFont

def get_postscript_name(font_path):
    try:
        font = TTFont(font_path, fontNumber=0, lazy=True)
        name_record = font['name'].getName(nameID=6, platformID=3, platEncID=1)
        if not name_record:
            name_record = font['name'].getName(nameID=6, platformID=1, platEncID=0)
        return str(name_record) if name_record else None
    except Exception as e:
        print(f"Error reading {font_path}: {e}")
        return None

def scan_fonts(font_dir):
    font_map = {}
    for root, _, files in os.walk(font_dir):
        for file in files:
            if file.lower().endswith((".ttf", ".otf")):
                path = os.path.join(root, file)
                ps_name = get_postscript_name(path)
                if ps_name:
                    font_map[ps_name] = path
    return font_map

if __name__ == "__main__":
    font_dir = "/System/Library/Fonts/"  # <-- Replace with your directory
    font_map = scan_fonts(font_dir)

    print("\nPostScript Name → File Path Mapping:\n")
    for ps_name, path in sorted(font_map.items()):
        print(f"{ps_name}: {path}")

