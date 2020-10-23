from potrace import Bitmap
from PIL import Image, ImageFilter
import numpy as np
import matplotlib.path as mpath
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import os

def get_image_np(image_name):
	image_path = 'images/' + image_name
	image = Image.open(image_path)
	return np.array(image.convert('RGB'))

def extract_box(image_name, image_np, coords, suffix = ''):
	if not os.path.exists('identified_images'):
		os.makedirs('identified_images')

	image = Image.fromarray(np.uint8(image_np)).convert('RGB')
	width, height = image.size

	ymin, xmin, ymax, xmax = coords
	(left, right, top, bottom) = (xmin * width, xmax * width,
                                  ymin * height, ymax * height)

	image_crop = image.crop((left, top, right, bottom))
	image_crop.save('playground/crop' + suffix + '.jpg', optimize=True, quality=80)
	crop_width, crop_height = image_crop.size

	width = (crop_width / width) * 100
	height = (crop_height / height) * 100
	return (ymin, xmin, width, height)

def extract_mask(image_name, image_np, mask_np, suffix = ''):
	if not os.path.exists('identified_images'):
		os.makedirs('identified_images')

	image = Image.fromarray(np.uint8(image_np)).convert('RGB')

	background = image.copy()
	background.putalpha(0)

	mask = Image.fromarray(np.uint8(mask_np)).convert('L').point(lambda x: 0 if x<128 else 255, '1').convert('RGB').filter(ImageFilter.GaussianBlur(10)).convert('L')
	mask.save('playground/mask' + suffix + '.png', 'PNG')
	result = Image.composite(image, background, mask).convert('RGBA')
	result.save('playground/object' + suffix + '.png', 'PNG')

def save_background(image_np):
	image = Image.fromarray(np.uint8(image_np)).convert('RGB')
	result = image.convert('RGB')
	result.save('playground/rest.jpg', 'JPEG', optimize=True, quality=8)

def vectorize_image(image_np):
	image = Image.fromarray(np.uint8(image_np)).convert('1')
	bitmap = Bitmap(np.asarray(image))
	path = bitmap.trace()

	Path = mpath.Path

	fig, ax = plt.subplots()
	pp1 = mpatches.PathPatch(
		Path([(0, 0), (1, 0), (1, 1), (0, 0)],
			[Path.MOVETO, Path.CURVE3, Path.CURVE3, Path.CLOSEPOLY]),
		fc="none", transform=ax.transData)

	ax.add_patch(pp1)
	ax.plot([0.75], [0.25], "ro")
	ax.set_title('The red point should be on the path')

	plt.show()
