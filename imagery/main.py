from detect import generate_boxes, generate_masks
from image import extract_box, extract_mask, get_image_np, save_background, vectorize_image
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
MODE = MODES['LAYERED_BOX']


detect_fn = load_model()
for image_name in os.listdir('./images/'):
	print('Loading {}... '.format(image_name))

	image_np = get_image_np(image_name)
	cache_location = CACHE_PATH + image_name

	if MODE == MODES['LAYERED_BOX']:
		boxes_coords = generate_boxes(detect_fn, image_np, cache_location)

		dimensions = []
		for index, coords in enumerate(boxes_coords):
			crop_dimensions = extract_box(image_name, image_np, coords, str(index))
			dimensions.append(crop_dimensions)

		with open('playground/coords.json', 'w') as outfile:
			json.dump(dimensions, outfile)

	if MODE == MODES['LAYERED_MASK']:
		masks_np = generate_masks(detect_fn, image_name, cache_location)

		for index, box_np in enumerate(masks_np):
			extract_mask(image_name, image_np, box_np, str(index))

	save_background(image_np)

	print('Completed ' + image_name)

print('Task complete')