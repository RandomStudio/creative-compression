import io
from PIL import Image, ImageCms
import numpy as np

def get_image_np(image_name):
	image_path = 'input_images/' + image_name
	image = Image.open(image_path)

	return np.array(image.convert('RGB'))


def crop_focus_area(destination, image_np, boxes_coords, mask_nps):
	original = Image.fromarray(np.uint8(image_np)).convert('RGB')
	width, height = original.size

	# left, top, right, bottom
	dimensions = [width, height, 0, 0]
	background = original.copy()
	background = background.resize((8, 8),resample=Image.BILINEAR)
	background = background.resize((width, height), Image.NEAREST)

	layerGroups = []
	for coords in boxes_coords:
		ymin, xmin, ymax, xmax = coords
		offsets = (xmin * width, ymin * height, xmax * width, ymax * height)

		layers = []
		for step in range(1, 5):
			[left, top, right, bottom] = offsets
			box_width = right - left
			box_height = bottom - top
			temp_left = int(left - (step * (box_width / 5)))
			temp_right = int(right + (step * (box_width / 5)))
			temp_top = int(top - (step * (box_height / 5)))
			temp_bottom = int(bottom + (step * (box_height / 5)))

			size = int(box_width / step)
			imgSmall = original.copy().resize((size, size), resample=Image.BILINEAR)
			imgSmall = imgSmall.resize(original.size, Image.NEAREST)
			imgSmall = imgSmall.crop([temp_left, temp_top, temp_right, temp_bottom])
			layers.append((imgSmall, int(temp_left), int(temp_top)))
		
		layerGroups.append(layers)
	
	allLayers = [val for tup in zip(*layerGroups) for val in tup]
	allLayers.reverse()
	for (image, left, top) in allLayers:
		background.paste(image, (left, top))

	for mask_np in mask_nps:
		mask = Image.fromarray(np.uint8(mask_np)).convert('L').point(lambda x: 0 if x < 128 else 255, '1')
		print(mask.size)
		background = Image.composite(original, background, mask)

	background.save(destination + '/image.jpg', 'JPEG', optimize=True, quality=80, progressive=True)
	original.save(destination + '/normal.jpg', 'JPEG', optimize=True, quality=80, progressive=True)
