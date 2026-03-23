sed -i -e 's:advance_x .*::g' bcpxtract/FONTS/{Morpheus,Proportional,Text_Box}/*/*.font
find bcpxtract/ -iname "*.font" -exec python3 increase_font.py {} 2 bcpxtract \;
find bcpxtract/FONTS/{Small_Numbers,DROP_SHADOW_WHITE} -iname "*.font" -exec rg source_file {} \; | cut -d ' ' -f2 | python3 resize_font_image.py 2 bcpxtract/
for f in `find bcpxtract/FONTS/{Text_Box,Proportional} -iname "*.tga"|cut -d '.' -f1`; do python3 render_font.py Prociono.ttf $f.tga 2 ${f}.tga; done
for f in `find bcpxtract/FONTS/Morpheus/ -iname "*.tga"|cut -d '.' -f1`; do python3 render_font.py  MORPHEUS.TTF $f.tga 2 ${f}.tga; done
