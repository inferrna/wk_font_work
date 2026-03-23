# wk_font_work
Change fonts in Warrior Kings® game resources

You need an extracted game resources to work with. I'm on linux, so I used this fork of wktools https://github.com/inferrna/wktools

The run-it-all script `change_font.sh` also assumes the following
1. Source files extracted with `bcpview` into bcpxtract directory 
2. Font files Prociono.ttf and MORPHEUS.TTF placed into the same directory as your scripts. You can use any fonts

## Details
### increase_font.py
Increases parameters in `*.font` file by integer value (currently 2)

### render_font.py
Re-renders font image from provided true-type font file. Also tries to restore the original font gradient color.

### resize_font_image.py
Upscales font image by integer value (currently 2)

## Steps
1. Run `bcpview` to exctract game resources ("Tools->Extract all files")
2. Run `change_font.sh` to change fonts
3. Run `bcppack bcpxtract new_data.bcp 2` to repack modified resources
