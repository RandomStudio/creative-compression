import io
import binascii
import tensorflow.compat.v1 as tf
import cartoonize.guided_filter as guided_filter
import cartoonize.network as network
import json
from potrace import Bitmap
from PIL import Image, ImageCms, ImageOps, ImageFilter
import numpy as np
import re
import cv2
from sklearn.cluster import MiniBatchKMeans


def get_image_np(image_name):
	image_path = 'images/' + image_name
	image = Image.open(image_path)

	iccProfile = image.info.get('icc_profile')
	iccBytes = io.BytesIO(iccProfile)
	originalColorProfile = ImageCms.ImageCmsProfile(iccBytes)

	return (np.array(image.convert('RGB')), originalColorProfile)


def chunk_image(image_np, destination):
	chunk = 0
	chunk_size = 20
	image = Image.fromarray(image_np)
	width, height = image.size
	output_filenames = []
	for row in range(0, height, chunk_size):
		for col in range(0, width, chunk_size):
			box = (col, row, col + width, row + height)
			a = image.crop(box)
			output = a.crop((0, 0, chunk_size, chunk_size))
			filename = destination + '/chunk-' + str(chunk) + '.jpg'
			output_filenames.append(filename)
			output.save(filename, quality=80, optimize=True, progressive=True)
			chunk += 1

	with open(destination + '/manifest.json', 'w') as outfile:
		json.dump(output_filenames, outfile)

def get_scan_offsets(destination):
	with open(destination + '/layered.jpg', 'rb') as f:
		content = f.read()

	hex = binascii.hexlify(content)
	hexStrings = [hex[i:i+2].decode('utf-8') for i in range(0, len(hex), 2)]

	found_marker = True
	scan_open = False
	offsets = []
	scan = {
		"start": 0,
		"scan": 0,
		"end": 0,
	}
	
	for (offset, hex) in enumerate(hexStrings):
		if hex != 'ff' and found_marker == False:
			continue
		
		## JPEG markers all start with a FF byte
		if hex == 'ff':
			found_marker = True
			continue

		# JPEG markers are made of 2 bytes. Following stops non headers being counted
		if hex == '00':
			found_marker = False
			continue
		if hex[0] == 'd' and hex[1].isnumeric() and int(hex[1]) <= 7:
			found_marker = False
			continue
		
		# Offset should start from beginning of FF marker
		offset = offset - 1
		if scan_open == True:
			scan['end'] = offset
			offsets.append(scan.copy())
			scan['start'] = offset
			scan_open = False

		if str(hex) == 'da':
			scan['scan'] = offset
			scan_open = True

		found_marker = False

	with open(destination + '/offsets.json', 'w') as outfile:
		json.dump(offsets, outfile)

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

#		layers = []
#		for step in range(5, 1, -1):
#			[left, top, right, bottom] = dimensions.copy()
#			difference = [left / step, top / step, width - ((width - right) / step), height - ((height - bottom) / step)]
#			print(difference)
#			temp_width = 100 / step
#			temp_height = 100 / step
#			imgSmall = normal.copy().resize((int(temp_width), int(temp_height)),resample=Image.BILINEAR)
#			imgSmall = ImageOps.expand(imgSmall, border=1, fill='#000000')
#			imgSmall = imgSmall.resize(image.size, Image.NEAREST)
#			imgSmall = imgSmall.crop(difference)
#
#			[left, top, right, bottom] = difference
#			layers.append((imgSmall, int(left), int(top)))
#
#		layerGroups.append(layers)
#
#	allLayers = [val for tup in zip(*layerGroups) for val in tup]
#	for (layerImage, layerLeft, layerTop) in allLayers:
#		image.paste(layerImage, (layerLeft, layerTop))
#
#	#for (layerImage, layerLeft, layerTop) in layers:
#	#		image.paste(layerImage, (layerLeft, layerTop)) 
#
#	#[left, top, right, bottom] = dimensions
#	#close_crop = normal.copy().crop(dimensions)
#	#close_crop = close_crop.resize((int(width / 4), int(width / 4)),resample=Image.BILINEAR)
#	#close_crop = close_crop.resize((int(right - left), int(bottom - top)), Image.NEAREST)
#	#image.paste(close_crop, (int(left), int(top)))
#
#	for coords in boxes_coords:
#		ymin, xmin, ymax, xmax = coords
#		offsets = (xmin * width, ymin * height, xmax * width, ymax * height)
#		box = normal.copy().crop(offsets)
#		image.paste(box, (int(xmin * width), int(ymin * height)))
#
	background.save(destination + '/bg.jpg', 'JPEG', optimize=True, quality=80, progressive=True)
	#target.convert('RGB').save(destination + '/target.jpg', 'JPEG', optimize=True, quality=80, progressive=True)
	#background.convert('RGBA')
	#background.paste(target, (0, 0))
	background.convert('RGB').save(destination + '/image.jpg', 'JPEG', optimize=True, quality=80, progressive=True)
	original.save(destination + '/normal.jpg', 'JPEG', optimize=True, quality=80, progressive=True)

def extract_box(destination, image_np, coords, suffix=''):
	image = Image.fromarray(np.uint8(image_np)).convert('RGB')
	image.save(destination + '/rest.jpg', 'JPEG', optimize=True, quality=8)
	image.save(destination + '/normal.jpg', 'JPEG', optimize=True, quality=80)

	width, height = image.size

	ymin, xmin, ymax, xmax = coords
	(left, right, top, bottom) = (xmin * width, xmax * width,
								  ymin * height, ymax * height)

	image_crop = image.crop((left, top, right, bottom))
	image_crop.save(destination + '/crop' + suffix + '.jpg', optimize=True, quality=80)

	crop_width, crop_height = image_crop.size

	width = (crop_width / width) * 100
	height = (crop_height / height) * 100
	return (ymin, xmin, width, height)


def extract_mask(destination, image_np, mask_np, suffix=''):
	image = Image.fromarray(np.uint8(image_np)).convert('RGB')
	image.save(destination + '/rest.jpg', 'JPEG', optimize=True, quality=8)
	image.save(destination + '/normal.jpg', 'JPEG', optimize=True, quality=80)

	background = image.copy()
	background.putalpha(0)

	mask = Image.fromarray(np.uint8(mask_np)).convert('L').point(
		lambda x: 0 if x < 128 else 255, '1').convert('RGB').filter(ImageFilter.GaussianBlur(10)).convert('L')
	mask.save(destination + '/mask' + suffix + '.png', 'PNG')
	result = Image.composite(image, background, mask).convert('RGBA')
	result.save(destination + '/object' + suffix + '.png', 'PNG')


def distance(col1, col2):
	(r1, g1, b1) = col1
	(r2, g2, b2) = col2
	return (r1 - r2)**2 + (g1 - g2) ** 2 + (b1 - b2) ** 2

def get_colors(img, numcolors=10, resize=150):
	img = img.copy()
	img.thumbnail((resize, resize))

	# Reduce to palette
	paletted = img.convert('P', palette=Image.ADAPTIVE, colors=numcolors)

	# Find dominant colors
	palette = paletted.getpalette()
	color_counts = sorted(paletted.getcolors(), reverse=True)
	colors = list()
	for i in range(numcolors):
		palette_index = color_counts[i][1]
		dominant_color = palette[palette_index*3:palette_index*3+3]
		colors.append(tuple(dominant_color))

	return colors

# https://github.com/SystemErrorWang/White-box-Cartoonization
def vectorize_image(image_np, destination, icc_profile):
	image = Image.fromarray(image_np).convert('RGB')
	width, height = image.size

	refColours = get_colors(image)
	#refColours = ([
	#	[86, 29, 37],
	#	[206, 129, 71],
	#	[236, 221, 123],
	#	[33, 161, 121],
	#	[4, 31, 30],
	#	[68, 94, 147],
	#	[229, 234, 250]
	#])
	
	pixels = image.load()

	for i in range(width):
		for j in range(height):
			mindist = distance(refColours[0], pixels[i,j])
			nearest = refColours[0]
			for index in range(1, len(refColours)):
				d = distance(refColours[index], pixels[i,j])
				if d < mindist:
					mindist = d
					nearest = refColours[index]
			pixels[i,j] = tuple(nearest)

	denoised = cv2.fastNlMeansDenoisingColored(np.array(image), None, 30, 10, 7, 21)

	image = cv2.cvtColor(denoised, cv2.COLOR_BGR2LAB)
	image = image.reshape((image.shape[0] * image.shape[1], 3))
	clt = MiniBatchKMeans(n_clusters=32)
	labels = clt.fit_predict(image)
	quant = clt.cluster_centers_.astype("uint8")[labels]
	quant = quant.reshape((height, width, 3))
	quant_np = cv2.cvtColor(quant, cv2.COLOR_LAB2BGR)
	tf.disable_eager_execution()
	tf.reset_default_graph()

	input_photo = tf.placeholder(tf.float32, [1, None, None, 3])
	network_out = network.unet_generator(input_photo)
	final_out = guided_filter.guided_filter(
		input_photo, network_out, r=1, eps=5e-3)

	all_vars = tf.trainable_variables()
	gene_vars = [var for var in all_vars if 'generator' in var.name]
	saver = tf.train.Saver(var_list=gene_vars)

	config = tf.ConfigProto()
	config.gpu_options.allow_growth = True
	sess = tf.Session(config=config)

	sess.run(tf.global_variables_initializer())
	saver.restore(sess, tf.train.latest_checkpoint('cartoonize/saved_models'))

	batch_image = image_np.astype(np.float32) / 127.5 - 1
	batch_image = np.expand_dims(batch_image, axis=0)
	output = sess.run(final_out, feed_dict={input_photo: batch_image})
	output = (np.squeeze(output)+1)*127.5
	output = np.clip(output, 0, 255).astype(np.uint8)

	Image.fromarray(output).save(destination + '/background.jpg', 'JPEG', optimize=True, quality=50, icc_profile=icc_profile.tobytes())