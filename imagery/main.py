from pathlib import Path
from detect import run_cached_inference
from image import extract_object, save_background
from model import load_model

import numpy as np
import os
import tensorflow as tf
import warnings

# Silence warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
tf.get_logger().setLevel('ERROR')
warnings.filterwarnings('ignore')

CACHE_PATH = 'cache/'

detect_fn = load_model()

for image_name in os.listdir('./images/'):
	detections = run_cached_inference(detect_fn, image_name, CACHE_PATH)

	image_np = np.load(CACHE_PATH + image_name + '_image.npy')

	for index in range(1, 11):
		image_mask = np.load(CACHE_PATH + image_name + '_mask_' + str(index) + '.npy')
		extract_object(image_name, image_np, image_mask, str(index))

	save_background(image_name, image_np)
	print('Done')

print('Task complete')