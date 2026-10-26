"""Creates the Android launcher icons from icon.png (run by the build workflow)."""
import os, shutil
from PIL import Image, ImageDraw

RES = 'android/app/src/main/res'
SIZES = {'mdpi': 48, 'hdpi': 72, 'xhdpi': 96, 'xxhdpi': 144, 'xxxhdpi': 192}
src = Image.open('icon.png').convert('RGBA')

# adaptive-icon xmls would override our PNGs, so remove them
shutil.rmtree(os.path.join(RES, 'mipmap-anydpi-v26'), ignore_errors=True)

for name, px in SIZES.items():
    d = os.path.join(RES, 'mipmap-' + name)
    os.makedirs(d, exist_ok=True)
    icon = src.resize((px, px), Image.LANCZOS)
    icon.save(os.path.join(d, 'ic_launcher.png'))
    icon.save(os.path.join(d, 'ic_launcher_foreground.png'))
    mask = Image.new('L', (px * 4, px * 4), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, px * 4 - 1, px * 4 - 1), fill=255)
    round_icon = icon.copy()
    round_icon.putalpha(mask.resize((px, px), Image.LANCZOS))
    round_icon.save(os.path.join(d, 'ic_launcher_round.png'))
print('icons written')
