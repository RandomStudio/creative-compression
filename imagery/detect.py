from model import detect_objects_in_image, download_labels
from pathlib import Path
import tensorflow as tf
import numpy as np
import os
import shelve 

from models.research.object_detection.utils import visualization_utils as vis_utils

def do_inference(detect_fn, image_np, cache_location):
	cache = shelve.open(cache_location)
	if 'cached_detections' in cache:
		print('Loaded detections from cache.')
		return cache['cached_detections']

	print('Running inference...')
	cache['cached_detections'] = detect_objects_in_image(image_np, detect_fn)
	cache.sync()
	#image_np_with_detections = visualize_detections(image_np, detections, category_index)
	return cache['cached_detections']

def generate_boxes(detect_fn, image_np, cache_location):
	detections = do_inference(detect_fn, image_np, cache_location)

	boxes_coords = []
	for index, detection_mask in enumerate(detections.get('detection_boxes')[0]):
		if detections["detection_scores"][0][index] > 0.7:
			boxes_coords.append(np.asarray(detection_mask).tolist())

	return boxes_coords

def generate_masks(detect_fn, image_np, cache_location):
	detections = do_inference(detect_fn, image_np, cache_location)

	masks_np = []
	for detection_mask in detections.get('detection_masks_reframed'):
		masks_np.append(image_np.shape[0] * detection_mask)

	return masks_np

def visualize_detections(image_np, detections, category_index):
	image_np_with_detections = image_np.copy()
	#labels_path = download_labels('mscoco_label_map.pbtxt')
	#category_index = label_map_util.create_category_index_from_labelmap(labels_path, use_display_name=True)

	boxes = np.asarray(detections["detection_boxes"][0])
	classes = np.asarray(detections["detection_classes"][0]).astype(np.int64)
	scores = np.asarray(detections["detection_scores"][0])
	mask = np.asarray(detections["detection_masks_reframed"])

	# Visualizing the results
	vis_utils.visualize_boxes_and_labels_on_image_array(
			image_np_with_detections,
			boxes,
			classes,
			scores,
			category_index,
			instance_masks=mask,
			use_normalized_coordinates=True,
			line_thickness=3)

	return image_np_with_detections