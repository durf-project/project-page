import sys
from rembg import remove, new_session
from PIL import Image, ImageChops
im = Image.open('photo.jpg').convert('RGB')
Y0, Y1 = 440, 960
m = sys.argv[1]; W = int(sys.argv[2]); step = int(sys.argv[3])
s = new_session(m)
mask = Image.new('L', (1600, Y1 - Y0), 0)
x = 0
while True:
    x0 = min(x, 1600 - W)
    tile = im.crop((x0, Y0, x0 + W, Y1))
    a = remove(tile, session=s, only_mask=True)
    part = Image.new('L', mask.size, 0); part.paste(a, (x0, 0))
    mask = ImageChops.lighter(mask, part)
    if x0 + W >= 1600: break
    x += step
out = im.crop((0, Y0, 1600, Y1)).convert('RGBA'); out.putalpha(mask)
out.save(f'tiles-{m}-{W}.png')
bg = Image.new('RGBA', out.size, (40, 160, 90, 255)); bg.alpha_composite(out); bg.convert('RGB').save(f'tprev-{m}-{W}.jpg')
