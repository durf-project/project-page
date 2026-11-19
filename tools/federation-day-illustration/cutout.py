"""Cut the group out of the Federation Day photo: two background-removal models on overlapping
tiles, merged; light grey wall and the screen's chat panel removed; cut off above the tables."""
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

a = np.array(Image.open('tiles-u2net_human_seg-520.png').getchannel('A')).astype(float)
b = np.array(Image.open('tiles-isnet-general-use-520.png').getchannel('A')).astype(float)
photo = Image.open('photo.jpg').convert('RGB').crop((0, 440, 1600, 960))
rgb = np.array(photo).astype(float)
R, B = rgb[..., 0], rgb[..., 2]
mx, mn = rgb.max(2), rgb.min(2)

m = np.maximum(a, b)
wall = (mx > 175) & ((mx - mn) < 28)              # light and grey: wall and screen glare
m[wall & (a < 245)] = 0
ys, xs = np.mgrid[0:m.shape[0], 0:m.shape[1]]
panel = (xs >= 1355) & (xs <= 1480) & (ys <= 50)  # the screen's chat panel (names): keep skin only
m[panel & ~(R > B + 12)] = 0
m = np.clip((m - 90) * 255 / 110, 0, 255)

M = Image.fromarray(m.astype('uint8')).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
CUT = 805 - 440                                    # just above the table tops
d = ImageDraw.Draw(M)
d.rectangle((0, CUT, 1600, M.height), fill=0)
d.ellipse((1176, 36, 1220, 82), fill=0)            # an avatar circle on the screen
out = photo.crop((0, 0, 1600, CUT)).convert('RGBA')
out.putalpha(M.crop((0, 0, 1600, CUT)))
out.save('people.png')
prev = Image.new('RGBA', out.size, (40, 160, 90, 255)); prev.alpha_composite(out)
prev.convert('RGB').save('people-prev.jpg')
