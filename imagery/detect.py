from model import download_labels
from image import get_image
from pathlib import Path
import tensorflow as tf
import itertools
import numpy as np
import os

from models.research.object_detection.utils import label_map_util
from models.research.object_detection.utils import visualization_utils as vis_utils

from object_detection.utils import ops as utils_ops

def detect_objects_in_image(image_np, detect_fn):
	print('================================')
	input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)

	detections = detect_fn(input_tensor)

	# All outputs are batches tensors.
	# Convert to numpy arrays, and take index [0] to remove the batch dimension.
	# We're only interested in the first num_detections.
	num_detections = int(detections.pop('num_detections'))

	detections = dict(itertools.islice(detections.items(), num_detections))
	detections['num_detections'] = num_detections

	# Handle models with masks:
	if "detection_masks" in detections:
			# Reframe the the bbox mask to the image size.
			detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
						detections["detection_masks"][0], detections["detection_boxes"][0],
						image_np.shape[0], image_np.shape[1])      
			detection_masks_reframed = tf.cast(detection_masks_reframed > 0.5,
																		tf.uint8)
			detections["detection_masks_reframed"] = [mask for index, mask in enumerate(detection_masks_reframed.numpy()) if detections["detection_scores"][0][index] > 0.7]

	return detections

labels_path = download_labels('mscoco_label_map.pbtxt')
category_index = label_map_util.create_category_index_from_labelmap(labels_path, use_display_name=True)

def run_cached_inference(detect_fn, image_name, CACHE_PATH):
	if not os.path.exists('cache'):
		os.makedirs('cache')

	print('Running inference for {}... '.format(image_name))

	IMAGE_NP_PATH = image_name + '_image.npy'
	if not Path(CACHE_PATH + IMAGE_NP_PATH).is_file():
		image = get_image(image_name)
		image_np = np.array(image.convert('RGB'))

		detections = detect_objects_in_image(image_np, detect_fn)
		#image_np_with_detections = visualize_detections(image_np, detections, category_index)

		for index, detection_mask in enumerate(detections.get('detection_masks_reframed')):
			mask_np = image_np.shape[0] * detection_mask
			np.save(CACHE_PATH + image_name + '_mask_' + str(index), mask_np)

		np.save(CACHE_PATH + IMAGE_NP_PATH, image_np)
		return detections

def visualize_detections(image_np, detections, category_index):
	image_np_with_detections = image_np.copy()

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