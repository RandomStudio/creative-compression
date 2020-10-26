from detect import generate_boxes, generate_masks
from image import extract_box, extract_mask, get_image_np, vectorize_image
from model import load_model
import numpy as np
import os
import json
import tensorflow as tf
import warnings

# Silence warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
tf.get_logger().setLevel('ERROR')
warnings.filterwarnings('ignore')

MODES = {
	'LAYERED_BOX': 'LAYERED_BOX',
	'LAYERED_MASK': 'LAYERED_MASK',
	'VECTOR_BACKGROUND': 'VECTOR_BACKGROUND',
}

CACHE_PATH = 'cache/'
MODE = MODES['VECTOR_BACKGROUND']


detect_fn = load_model()
for image_name in os.listdir('./images/'):
	print('Loading {}... '.format(image_name))

	image_np = get_image_np(image_name)
	cache_location = CACHE_PATH + image_name

	if MODE == MODES['LAYERED_BOX']:
		destination = 'playground/boxes'
		if not os.path.exists(destination):
			os.makedirs(destination)

		boxes_coords = generate_boxes(detect_fn, image_np, cache_location)
		dimensions = []
		for index, coords in enumerate(boxes_coords):
			crop_dimensions = extract_box(destination, image_np, coords, str(index))
			dimensions.append(crop_dimensions)

		with open(destination + '/coords.json', 'w') as outfile:
			json.dump(dimensions, outfile)

	if MODE == MODES['LAYERED_MASK']:
		masks_np = generate_masks(detect_fn, image_np, cache_location, max_highlights=5)

		destination = 'playground/masks'
		if not os.path.exists(destination):
			os.makedirs(destination)

		for index, box_np in enumerate(masks_np):
			extract_mask(destination, image_np, box_np, str(index))

	if MODE == MODES['VECTOR_BACKGROUND']:
		destination = 'playground/vectorize'
		if not os.path.exists(destination):
			os.makedirs(destination)

		boxes_coords = generate_boxes(detect_fn, image_np, cache_location)
		dimensions = []
		for index, coords in enumerate(boxes_coords):
			crop_dimensions = extract_box(destination, image_np, coords, str(index))
			dimensions.append(crop_dimensions)

		with open(destination + '/coords.json', 'w') as outfile:
			json.dump(dimensions, outfile)

		vectorize_image(image_np, destination)

	print('Completed ' + image_name)

print('Task complete')