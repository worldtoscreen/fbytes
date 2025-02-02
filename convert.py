class Config:
    FONT_PATH = ""  # e.g. C:/Path/To/TTF.ttf
    USE_CUSTOM_NAMES = True  # Some fonts may provide icon names, some may not. You might not want to use this.
    IS_UTF8 = True  # Used for ImGui & DirectX, recommended!
    MAX_SIZE = 1048576  # Max Size for SFPro Icons
    SAVE_HEADER = True  # Save a C-Style header
    HEADER_NAME = 'icon_map.h'  # Header name
    CREATE_VECTOR = True  # debugging purposes - create a list of every single macro.

from fontTools.ttLib import TTFont
from datetime import datetime as dt

OUT = "#pragma once\n"
if Config.CREATE_VECTOR:
    OUT += f'#include <vector>\n\n'
NAMES = []

def oprint(s):
    print(s)

    global OUT
    OUT += s

font = TTFont(Config.FONT_PATH)

cmap = font["cmap"].getBestCmap()

if not cmap:
    print("No Unicode mapping found in the font.")
    exit(0)

def convert_to_utf8(codepoint):
    cp_int = int(codepoint, 16)
    char = chr(cp_int)
    utf8_bytes = char.encode("utf-8")
    return " ".join(f"0x{b:02X}" for b in utf8_bytes)

def get_vector(names_array):
    return f'std::vector<std::string> all_icons = {{ {''.join(f' {n}, ' for n in names_array)} }} '

found = 1
first = None
last = None

oprint(f'/* Auto-Generated by https://github.com/worldtoscreen/fbyte  */\n')
now = dt.now()

# just now thinking I could use a list for this... oh well!
days = {
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday',
    4: 'Friday',
    5: 'Saturday',
    6: 'Sunday'
}

months = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December',
}

def get_c_style_str(bytes):
    # e.g. bytes=0xEF 0x8D 0xA2
    s = '\"'
    for b in bytes.split(' '):
        bstr = b.split('0x')[1].lower()
        s += f'\\x{bstr}'

    return s + "\""

oprint(f'// Generated Timestamp: {days[now.weekday()]}, {months[now.month]} {now.day} {now.year} [timestamp={int(now.timestamp())}]\n\n')

for codepoint, glyph_name in cmap.items():
    if codepoint >= Config.MAX_SIZE:
        print(f'SKIPPING {codepoint}')
        continue

    cp = f'{codepoint:04X}'

    if Config.IS_UTF8:
        cp = convert_to_utf8(cp)
    else:
        pass

    unicode = f'U+{codepoint:04X}'
    name = f'ICON_{found}' if Config.USE_CUSTOM_NAMES else str(glyph_name)

    oprint(f'#define {name} {get_c_style_str(cp)} // {unicode}\n')
    NAMES.append(name)

    if first is None:
        first = unicode

    print(f'{codepoint}={unicode}')
    last = unicode

    found += 1

oprint(f'\n\n')

oprint(f'#define ICON_MIN_FA {first.replace('U+', '0x')}\n')
oprint(f'#define ICON_MAX_FA {last.replace('U+', '0x')}')

if Config.SAVE_HEADER:
    with open(Config.HEADER_NAME, 'w') as f:
        f.write(f'{OUT}\n\n{get_vector(NAMES)}')
