import pathlib
import os
import tensorflow as tf
import time
from models.research.object_detection.builders import model_builder
from models.research.object_detection.utils import config_util

# Download and extract model
def download_model(model_name, model_date):
	base_url = 'http://download.tensorflow.org/models/object_detection/tf2/'
	model_file = model_name + '.tar.gz'
	model_dir = tf.keras.utils.get_file(fname=model_name,
										origin=base_url + model_date + '/' + model_file,
										untar=True)
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
		'mask_rcnn_inception_resnet_v2_1024x1024_coco17_gpu-8', '20200711')
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