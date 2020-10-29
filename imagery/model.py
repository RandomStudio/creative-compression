import itertools
import numpy as np
import os
import pathlib
import tensorflow as tf
import time

from models.research.object_detection.builders import model_builder
from models.research.object_detection.utils import config_util
from models.research.object_detection.utils import label_map_util
from object_detection.utils import ops as utils_ops

# Download and extract model
def download_model(model_name, model_date):
	base_url = 'http://download.tensorflow.org/models/object_detection/tf2/'
	model_file = model_name + '.tar.gz'
	model_dir = tf.keras.utils.get_file(fname=model_name,
										origin=base_url + model_date + '/' + model_file,
										untar=True)
	print(model_dir)
	return str(model_dir)

# Download labels file
def download_labels(filename):
	base_url = 'https://raw.githubusercontent.com/tensorflow/models/master/research/object_detection/data/'
	label_dir = tf.keras.utils.get_file(fname=filename,
										origin=base_url + filename,
										untar=False)
	label_dir = pathlib.Path(label_dir)
	return str(label_dir)


def load_model():
	PATH_TO_MODEL_DIR = download_model(
		'mask_rcnn_inception_resnet_v2_1024x1024_coco17_gpu-8', '20200712')
	PATH_TO_CFG = PATH_TO_MODEL_DIR + "/pipeline.config"
	PATH_TO_CKPT = PATH_TO_MODEL_DIR + "/checkpoint"

	print('Loading model... ', end='')
	start_time = time.time()

	# Load pipeline config and build a detection model
	configs = config_util.get_configs_from_pipeline_file(PATH_TO_CFG)
	model_config = configs['model']
	detection_model = model_builder.build(
	model_config=model_config, is_training=False)

	# Restore checkpoint
	ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
	ckpt.restore(os.path.join(PATH_TO_CKPT, 'ckpt-0')).expect_partial()


	@tf.function
	def detect_fn(image):
		"""Detect objects in image."""
		
		image, shapes = detection_model.preprocess(image)
		prediction_dict = detection_model.predict(image, shapes)
		detections = detection_model.postprocess(prediction_dict, shapes)

		return detections


	end_time = time.time()
	elapsed_time = end_time - start_time
	print('Done! Took {} seconds'.format(elapsed_time))
	return detect_fn


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
			detections['detection_masks_reframed'] = tf.cast(detection_masks_reframed > 0.5,
																		tf.uint8)

	return detections
