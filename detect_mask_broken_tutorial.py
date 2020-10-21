import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
import pathlib

from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image
from IPython.display import display

from object_detection.utils import ops as utils_ops
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

# patch tf1 into `utils.ops`
utils_ops.tf = tf.compat.v1

# Patch the location of gfile
tf.gfile = tf.io.gfile

def load_model(model_name):
	model_dir = tf.keras.utils.get_file(
		fname=model_name, 
		origin='http://download.tensorflow.org/models/object_detection/tf2/20200711/'+ model_name + '.tar.gz',
		untar=True)

	model_dir = pathlib.Path(model_dir)/"saved_model"

	model = tf.saved_model.load(str(model_dir))

	return model


PATH_TO_LABELS = 'models/research/object_detection/data/mscoco_label_map.pbtxt'
category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)

# If you want to test the code with your images, just add path to the images to the TEST_IMAGE_PATHS.
PATH_TO_TEST_IMAGES_DIR = pathlib.Path('images/')
TEST_IMAGE_PATHS = sorted(list(PATH_TO_TEST_IMAGES_DIR.glob("*.jpg")))

def run_inference_for_single_image(masking_model, image_path):
	print("Running inference for : ",image_path)
	image = Image.open(image_path)
	image_np = np.array(image.convert('RGB'))
	
	# The input needs to be a tensor, convert it using `tf.convert_to_tensor`.
	input_tensor = tf.convert_to_tensor(image_np)
	# The model expects a batch of images, so add an axis with `tf.newaxis`.
	input_tensor = input_tensor[tf.newaxis, ...]

	# input_tensor = np.expand_dims(image_np, 0)
	detections = masking_model(input_tensor)

	# All outputs are batches tensors.
	# Convert to numpy arrays, and take index [0] to remove the batch dimension.
	# We're only interested in the first num_detections.
	num_detections = int(detections.pop("num_detections"))

	# detections = {key: value[0, :num_detections].numpy()
	#             for key, value in detections.items()}

	import itertools
	detections = dict(itertools.islice(detections.items(), num_detections))

	detections["num_detections"] = num_detections

	# detection_classes should be ints.
	# detections["detection_classes"] = detections["detection_classes"].astype(np.int64)

	image_np_with_detections = image_np.copy()

	# Handle models with masks:
	if "detection_masks" in detections:
			# Reframe the the bbox mask to the image size.
			detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
						detections["detection_masks"][0], detections["detection_boxes"][0],
						image_np.shape[0], image_np.shape[1])      
			detection_masks_reframed = tf.cast(detection_masks_reframed > 0.5,
																		tf.uint8)
			detections["detection_masks_reframed"] = detection_masks_reframed.numpy()

	boxes = np.asarray(detections["detection_boxes"][0])
	classes = np.asarray(detections["detection_classes"][0]).astype(np.int64)
	scores = np.asarray(detections["detection_scores"][0])
	mask = np.asarray(detections["detection_masks_reframed"])

	# Visualizing the results
	vis_util.visualize_boxes_and_labels_on_image_array(
			image_np_with_detections,
			boxes,
			classes,
			scores,
			category_index,
			instance_masks=mask,
			use_normalized_coordinates=True,
			line_thickness=3)

	display(Image.fromarray(image_np_with_detections))
	print("Done")

masking_model = load_model('mask_rcnn_inception_resnet_v2_1024x1024_coco17_gpu-8')

for image_path in TEST_IMAGE_PATHS:	
	run_inference_for_single_image(masking_model, image_path)