import sys
import re
import platform
from pathlib import Path
import os
from PIL import Image

file_name, scale_factor = sys.argv[1:3]
sf = int(scale_factor)

def fix_line(line: str) -> str:
    start_words = ["height", "glyph_gap", "space_size"]
    words = re.split(r'\s+', line)
    if len(words) == 0:
        return line
    if words[0] in start_words:
        for i in range(1, len(words)):
            words[i] = str(int(words[i])*sf)
    if words[0] == "advance_x":
        words[2] = str(int(words[2])*sf)
    return " ".join(words)



lines = open(file_name, "r").read().split("\n")
fixed_lines  = [fix_line(l) for l in lines]

f = open(file_name, "w")
f.write("\n".join(fixed_lines))
