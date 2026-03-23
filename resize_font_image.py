import sys
import re
import platform
from pathlib import Path
import os
from PIL import Image

scale_factor, base_dir = sys.argv[1:3]
sf = int(scale_factor)


def find_real_path(insensitive_path) -> Path:
    p = Path(insensitive_path.replace("\\", os.sep))
    # Find all potential matches in the directory using case_sensitive=False
    print(f"Find actual location of {insensitive_path} -> {p}")
    for actual_path in Path(base_dir).rglob(p.name, case_sensitive=False):
        print(f"Examine {actual_path}")
        if str(p)[1:].lower() in str(actual_path).lower() and actual_path.is_file():
            print(f"Found {actual_path} for {insensitive_path}")
            return actual_path
    raise FileNotFoundError(f"No file found for path: {insensitive_path}")

def resize_tga(filepath: str):
    real_path = find_real_path(filepath)
    img = Image.open(real_path)
    new_size = (int(img.width * sf), int(img.height * sf))
    resized_img = img.resize(new_size, resample=Image.NEAREST)
    resized_img.save(real_path)

for line in sys.stdin:
    file_name = re.sub('\s+', "", line)
    print(f"Got {file_name}")
    resize_tga(file_name) # Name cones from *.font file
