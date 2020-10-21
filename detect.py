from functions import download_model
from functions import download_labels
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from object_detection.utils import ops as utils_ops
from models.research.object_detection.builders import model_builder
from models.research.object_detection.utils import config_util
from models.research.object_detection.utils import visualization_utils as vis_utils
from models.research.object_detection.utils import label_map_util
import os
import time
import tensorflow as tf
import warnings
from datetime import datetime

# Silence warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
tf.get_logger().setLevel('ERROR')
warnings.filterwarnings('ignore')


################

PATH_TO_MODEL_DIR = download_model(
	'mask_rcnn_inception_resnet_v2_1024x1024_coco17_gpu-8', '20200711')
PATH_TO_LABELS = download_labels('mscoco_label_map.pbtxt')

PATH_TO_CFG = PATH_TO_MODEL_DIR + "/pipeline.config"
PATH_TO_CKPT = PATH_TO_MODEL_DIR + "/checkpoint"

IMAGE_NAMES = os.listdir('./images/')

################

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

################

category_index = label_map_util.create_category_index_from_labelmap(
	PATH_TO_LABELS, use_display_name=True)

################
if not os.path.exists('identified_images'):
    os.makedirs('identified_images')

for image_name in IMAGE_NAMES:
	image_path = 'images/' + image_name

	print('Running inference for {}... '.format(image_path))

	image = Image.open(image_path)
	image_np = np.array(image.convert('RGB'))

	print('================================')
	input_tensor = tf.convert_to_tensor(
		np.expand_dims(image_np, 0), dtype=tf.float32)

	detections = detect_fn(input_tensor)

	# All outputs are batches tensors.
	# Convert to numpy arrays, and take index [0] to remove the batch dimension.
	# We're only interested in the first num_detections.
	num_detections = int(detections.pop('num_detections'))

	import itertools
	detections = dict(itertools.islice(detections.items(), num_detections))
	detections['num_detections'] = num_detections

	label_id_offset = 1
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
	vis_utils.visualize_boxes_and_labels_on_image_array(
			image_np_with_detections,
			boxes,
			classes,
			scores,
			category_index,
			instance_masks=mask,
			use_normalized_coordinates=True,
			line_thickness=3)

	width, height = image.size
	plt.figure(figsize=(width / 100, height / 100), dpi=100)
	plt.imshow(image_np_with_detections)

	plt.savefig('identified_images/' + datetime.now().strftime("%d-%m-%Y_%H-%M-%S")  + '_' + image_name, dpi=100)

	print('Done')
plt.show(block=True)
