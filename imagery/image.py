import tensorflow.compat.v1 as tf
import cartoonize.guided_filter as guided_filter
import cartoonize.network as network
import json
from potrace import Bitmap
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
from matplotlib import cm, colors, pyplot as plt
import os
import cv2
from sklearn.cluster import MiniBatchKMeans


def get_image_np(image_name):
	image_path = 'images/' + image_name
	image = Image.open(image_path)
	return np.array(image.convert('RGB'))


def chunk_image(image_np, destination):
	print('chunk')
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


def extract_box(destination, image_np, coords, suffix=''):
	image = Image.fromarray(np.uint8(image_np)).convert('RGB')
	image.save(destination + '/rest.jpg', 'JPEG', optimize=True, quality=8)
	image.save(destination + '/normal.jpg', 'JPEG', optimize=True, quality=80)

	width, height = image.size

	ymin, xmin, ymax, xmax = coords
	(left, right, top, bottom) = (xmin * width, xmax * width,
								  ymin * height, ymax * height)

	image_crop = image.crop((left, top, right, bottom))
	image_crop.save(destination + '/crop' + suffix +
					'.jpg', optimize=True, quality=80)

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


# https://github.com/SystemErrorWang/White-box-Cartoonization
def vectorize_image(image_np, destination):
	image = Image.fromarray(image_np).convert('RGB')
	width, height = image.size

	refColours = ([
		[86, 29, 37],
		[206, 129, 71],
		[236, 221, 123],
		[33, 161, 121],
		[4, 31, 30],
		[68, 94, 147],
		[229, 234, 250]
	])

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

	batch_image = quant_np.astype(np.float32) / 127.5 - 1
	batch_image = np.expand_dims(batch_image, axis=0)
	output = sess.run(final_out, feed_dict={input_photo: batch_image})
	output = (np.squeeze(output)+1)*127.5
	output = np.clip(output, 0, 255).astype(np.uint8)

	Image.fromarray(output).save(destination + '/background.png', 'PNG')