from copy import copy
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageEnhance
from fontTools.ttLib import TTFont
import numpy as np

def trim_background(im: Image.Image, target_height: int, border_color: tuple):
    if im.height <= target_height:
        return im
    # Create a background image of the same size and mode as the original, filled with the border color
    bg = Image.new(im.mode, im.size, border_color)
    # Find the difference between the image and the background
    diff = ImageChops.difference(im, bg)
    # Get the bounding box of the non-background region
    bbox = diff.getbbox()

    if bbox:
        # If a bounding box is found, crop the original image to that box
        upper = bbox[1]
        lower = bbox[3]
        print(f"upper = {upper}, lower = {lower}")
        box_h = lower - upper
        diff = target_height - box_h
        while diff>0:
            if lower<im.height:
                lower+=1
                diff-=1
            if upper>0 and diff>0:
                upper -= 1
                diff-=1
        return im.crop((0, upper, im.width, lower))
    else:
        # Otherwise, return the original image
        return im

def get_glyph_characters(ttf_path: str, rng: range) -> list[str]:
    font = TTFont(ttf_path)
    cmap = font["cmap"].getBestCmap()
    chars = [chr(codepoint) for codepoint in cmap.keys() if codepoint in rng]
    return chars

def render_glyphs_single_line(ttf_path: str, rng: range, best_colors: np.ndarray, target_height: int, padding: int, output: str):
    chars = get_glyph_characters(ttf_path, rng)

    font_size = target_height
    while True:
        font = ImageFont.truetype(ttf_path, font_size)

        # Measure total width
        widths = []
        max_height = 0

        for ch in chars:
            bbox = font.getbbox(ch)
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]
            widths.append(w)
            max_height = max(max_height, h)

        total_width = sum(widths) + padding * (len(chars) + 1)
        total_height = 2*max_height

        # Create image
        img = Image.new("RGBA", (total_width, total_height), (0,0,0,0))
        draw = ImageDraw.Draw(img)

        x = padding
        for ch, w in zip(chars, widths):
            draw.text((x, 0), ch, spacing=padding, font=font, fill="white")
            if ch == "\"":
                bbox = font.getbbox(ch)
                im_ch = img.crop((bbox[0]+x,bbox[1],bbox[2]+x,bbox[3],))
                ch_arr = np.array(im_ch)
                mins = ch_arr.max(axis=0).max(axis=1)
                start = 0
                end = mins.shape[0]-1
                for i in range(start, end):
                    if mins[i]==0:
                        start += 1
                    else:
                        break
                for i in range(end, start, -1):
                    if mins[i]==0:
                        end -= 1
                    else:
                        break
                for i in range(start+1, end):
                    if mins[i]==0:
                        img.putpixel((bbox[0]+x+i, bbox[1]), (255,255,255,8))


                # print(ch_arr.shape)
                # print(mins)
                # img.save("/tmp/ch.png")
                # exit(0)

            x += w + padding

        img = trim_background(img, target_height, (0,0,0,0))
        if img.height<=target_height:
            assert img.height==target_height, f"{img.height} != {target_height}"
            break
        else:
            font_size -= 1

    img_array = np.array(img)
    img_array = np.minimum(img_array, best_colors[:, np.newaxis, :]).astype(np.uint8)
    print(img_array.max())
    img = Image.fromarray(img_array)
    # brightness_enhancer = ImageEnhance.Brightness(img)
    # img = brightness_enhancer.enhance(1.5)
    img.save(output)
    print(f"Saved to {output}")

if __name__ == "__main__":
    import sys
    # bcpxtract/FONTS/Morpheus/20/33_126.tga
    font_file, base_file, scale, out_image = sys.argv[1:6]
    font_words = base_file.split("/")
    base_font_size = int(font_words[3])
    glyps_idxs_raw = font_words[4].split(".")[0].split("_")
    first_glyph = int(glyps_idxs_raw[0])
    last_glyph = int(glyps_idxs_raw[1])

    cf = int(scale)

    base_image = trim_background(Image.open(base_file), base_font_size//2, (0,0,0,0))
    base_array = np.array(base_image, dtype=np.uint16)
    h, w, c = base_array.shape
    #print(base_array.shape)
    luma: np.ndarray = base_array[:,:,0:3].sum(axis=2) # Sum colors
    #print(luma.shape)
    #print(luma.argmax(axis=1))
    best_colors = base_array[range(0, h), luma.argmax(axis=1)]

    target_height = base_font_size*cf
    scaled_bc = np.zeros(shape=(target_height, c), dtype=base_array.dtype)
    for i in range(0, c):
        print(f"bc[{i}] before = {best_colors[:,i]}")
        scaled_bc[:,i] = np.interp(np.arange(0,target_height), np.arange(0,h)*cf, best_colors[:,i])
        print(f"bc[{i}] after = {scaled_bc[:,i]}")
    scaled_bc[:,3] = 255
    print(scaled_bc)


    render_glyphs_single_line(font_file, range(first_glyph, last_glyph+2), scaled_bc, target_height=target_height, padding=6, output=out_image)
