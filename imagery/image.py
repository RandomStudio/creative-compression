from PIL import ImageFilter
import cv2
from datetime import datetime
from PIL import Image, ImageOps
import numpy as np
import matplotlib.path as mpath
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import os

def get_image(image_name):
	image_path = 'images/' + image_name
	return Image.open(image_path)

def extract_object(image_name, image_np, mask_np, suffix = ''):
	if not os.path.exists('identified_images'):
		os.makedirs('identified_images')

	image = Image.fromarray(np.uint8(image_np)).convert('RGB')

	background = image.copy()
	background.putalpha(0)

	mask = Image.fromarray(np.uint8(mask_np)).convert('L').point(lambda x: 0 if x<128 else 255, '1').convert('RGB').filter(ImageFilter.GaussianBlur(10)).convert('L')
	result = Image.composite(image, background, mask).convert('RGBA')
	result.save('playground/object' + suffix + '.png', 'PNG')

def save_background(image_name, image_np):
	image = Image.fromarray(np.uint8(image_np)).convert('RGB')
	result = image.convert('RGB')
	result.save('playground/rest.jpg', 'JPEG',optimize=True,quality=10)

from potrace import Bitmap

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
