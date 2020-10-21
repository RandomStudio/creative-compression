import tensorflow as tf
import itertools
import numpy as np
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
			detections["detection_masks_reframed"] = detection_masks_reframed.numpy()

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