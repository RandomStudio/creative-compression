from PIL import Image, ImageCms, ImageOps
from PIL import ImageFilter
import numpy as np

def get_image_np(image_name):
	image_path = 'input_images/' + image_name
	image = Image.open(image_path)

	return np.array(image.convert('RGB'))

def compose_focus_effect(destination, image_np, boxes_and_masks):
	source = Image.fromarray(np.uint8(image_np))
	background = create_background_layer(source)

	(boxes, masks) = boxes_and_masks
	box_overlays = create_bounding_box_overlays(boxes, source)
	mask_overlays = create_mask_overlays(masks, source)
	composition = compose_image(source, background, box_overlays, mask_overlays)
	save_versions(source, composition, destination)

def create_background_layer(source):
	background = source.copy()
	width, height = source.size
	background = background.resize((8, 8),resample=Image.BILINEAR)
	background = background.resize((width, height), Image.NEAREST)
	return background

def create_bounding_box_overlay(coords, source):
	source_width, source_height = source.size
	ymin, xmin, ymax, xmax = coords
	offsets = (xmin * source_width, ymin * source_height, xmax * source_width, ymax * source_height)

	[left, top, right, bottom] = offsets
	width = right - left
	height = bottom - top

	def adjustOffset(offset, step, index):
		dimension = width if index % 2 == 0 else height
		if index < 2:
			return int(offset - (step * (dimension / 5)))
		return int(offset + (step * (dimension / 5)))

	def compose_overlay(step):
		#if step == 1:
		#	return (source.copy().crop(offsets), int(offsets[0]), int(offsets[1])) 

		adjustedOffsets = [adjustOffset(offset, step, index) for index, offset in enumerate(offsets)]
		[left, top, right, bottom] = adjustedOffsets
		shrink_size = int(width / step)
		destroyed_source = source.copy().resize((shrink_size, shrink_size), resample=Image.BILINEAR).resize(source.size, Image.NEAREST)
		bounding_box_overlay = destroyed_source.crop(adjustedOffsets)
		#bounding_box_overlay = ImageOps.expand(bounding_box_overlay, border=5, fill="#000")
		return (bounding_box_overlay, int(left), int(top))

	layers = [compose_overlay(step) for step in range(1, 5)]

	return layers

def create_bounding_box_overlays(boxes_coords, source):
	layerGroups = [create_bounding_box_overlay(coords, source) for coords in boxes_coords]
	allLayers = [val for tup in zip(*layerGroups) for val in tup]
	allLayers.reverse()
	return allLayers

def create_mask_overlays(mask_nps, source):
	def compose_mask(mask_np):
		background = source.copy()
		background.putalpha(0)

		mask = Image.fromarray(
				np.uint8(mask_np)
			).convert('L').point(
				lambda x: 0 if x < 128 else 255, '1'
			).convert(
				'RGB'
			).filter(
				ImageFilter.GaussianBlur(10)
			).convert('L')

		return Image.composite(source, background, mask).convert('RGBA')

	masks = [compose_mask(mask_np) for mask_np in mask_nps]
	return masks

def compose_image(source, background, box_overlays, mask_overlays):
	source = source.copy()
	composition = background.copy()

	for (image, left, top) in box_overlays:
		composition.paste(image, (left, top))

	for i, mask in enumerate(mask_overlays):
		composition = Image.composite(source, composition, mask)

	return composition

def save_versions(source, composition, destination):
	composition.save(destination + '/image.jpg', 'JPEG', optimize=True, quality=80, progressive=True)
	source.save(destination + '/normal.jpg', 'JPEG', optimize=True, quality=80, progressive=True)
