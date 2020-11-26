from PIL import Image, ImageCms, ImageOps, ImageFilter
import numpy as np
import os

def get_image_np(image_name):
	image_path = 'input_images/' + image_name
	image = Image.open(image_path)
	return np.array(image.convert('RGB'))

def compose_focus_effect(source, boxes, clientWidth):
	#source = Image.fromarray(np.uint8(image_np))
	background = create_background_layer(source)
	box_overlays = create_bounding_box_overlays(boxes, source, clientWidth)
	# mask_overlays = create_mask_overlays(masks, source)
	composition, frames = compose_image(source, background, box_overlays)
	return source, background, composition, frames

def create_background_layer(source):
	background = source.copy()
	width, height = source.size
	background = background.resize((8, 8),resample=Image.BILINEAR)
	background = background.resize((width, height), Image.NEAREST)
	return background

def create_bounding_box_overlay(coords, source, scale):
	STEPS = 5
	#ymin, xmin, ymax, xmax = coords
	startX, startY, width, height = coords
	endX = startX + width
	endY = startY + height
	xmin, xmax = sorted([startX, endX])
	ymin, ymax = sorted([startY, endY])
	#offsets = (xmin * source_width, ymin * source_height, xmax * source_width, ymax * source_height)
	offsets = (xmin * scale, ymin * scale, xmax * scale, ymax * scale)
	[left, top, right, bottom] = offsets
	width = right - left
	height = bottom - top

	def adjustOffset(offset, step, index):
		dimension = width if index % 2 == 0 else height
		if index < 2:
			return int(offset - (step * (dimension / 5)))
		return int(offset + (step * (dimension / 5)))

	def compose_overlay(step):
		adjustedOffsets = [adjustOffset(offset, step, index) for index, offset in enumerate(offsets)]
		[left, top, right, bottom] = adjustedOffsets

		square_root_width = width**(1/2)
		square_root_height = height**(1/2)
		width_bit = (width / 2) / square_root_width
		height_bit = (height / 2) / square_root_height

		small_width = (width**(1/(step + 2))) * width_bit
		small_height = (height**(1/(step + 2))) * height_bit

		# total_parts = sum(range(0, STEPS))
		# covered_parts = sum(range(0, STEPS - step)) + 1

		# small_width = ((width - 16) / total_parts) * covered_parts
		# small_height = ((height - 16) / total_parts) * covered_parts
		destroyed_source = source.copy().resize((int(small_width), int(small_height)), resample=Image.BILINEAR).resize(source.size, Image.NEAREST) if step > 0 else source.copy()
		bounding_box_overlay = destroyed_source.crop(adjustedOffsets)
		#bounding_box_overlay = ImageOps.expand(bounding_box_overlay, border=5, fill="#000")
		return (bounding_box_overlay, int(left), int(top))

	layers = [compose_overlay(step) for step in range(0, STEPS)]

	return layers

def create_bounding_box_overlays(boxes_coords, source, clientWidth):
	source_width, source_height = source.size
	scale = source_width / int(clientWidth)
	layerGroups = [create_bounding_box_overlay(coords, source, scale) for coords in boxes_coords]
	allLayers = [val for tup in zip(*layerGroups) for val in tup]
	allLayers.reverse()
	return allLayers

def create_mask_overlays(mask_nps, source):
	def compose_mask(mask_np, index):
		background = source.copy()
		background.putalpha(0)

		mask = Image.fromarray(
				np.uint8(mask_np)
			).convert('L').point(
				lambda x: 0 if x < 128 else 255, '1'
			).convert(
				'RGB'
			).filter(
				ImageFilter.GaussianBlur(2)
			).convert('L').resize(source.size)

		return Image.composite(source, background, mask).convert('RGBA')

	masks = [compose_mask(mask_np, index) for index, mask_np in enumerate(mask_nps)]

	return masks

def compose_image(source, background, box_overlays):
	frames = []
	source = source.copy()
	composition = background.copy()

	for (image, left, top) in box_overlays:
		composition.paste(image, (left, top))
		#frames.append(composition.copy())

	#for i, mask in enumerate(mask_overlays):
	#	composition = Image.composite(source, composition, mask)
	#	frames.append(composition.copy())

	return [composition, frames]

def save_versions(source, composition, destination):
	composition.save(destination + '/image.jpg', 'JPEG', optimize=True, quality=80, progressive=True)
	source.save(destination + '/normal.jpg', 'JPEG', optimize=True, quality=80, progressive=True)

def save_animation(source, background, frames, destination):
	if not os.path.exists(destination):
		os.makedirs(destination + '/frames')

	animation = [source, background]
	animation.extend(frames)
	def resizeFrame(frame):
		width, height = frame.size
		newHeight = int((1920 / width) * height)
		return frame.resize((1920, newHeight))
	animation = [resizeFrame(frame) for frame in animation]
	[frame.save(destination + '/frames/frame' +  str(index) + '.jpg', 'JPEG', optimize=True, quality=90, progressive=True) for index, frame in enumerate(animation)]
	animation[0].save(destination + '/animation.webp',
               save_all=True,
               append_images=animation[1:],
               duration=100,
               loop=0)
