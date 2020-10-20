from functions import download_model
from functions import download_labels
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from models.research.object_detection.builders import model_builder
from models.research.object_detection.utils import config_util
from models.research.object_detection.utils import visualization_utils as viz_utils
from models.research.object_detection.utils import label_map_util
import os
import time
import tensorflow as tf
import warnings

# Silence warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
tf.get_logger().setLevel('ERROR')
warnings.filterwarnings('ignore')


################

PATH_TO_MODEL_DIR = download_model(
	'centernet_hg104_1024x1024_coco17_tpu-32', '20200711')
PATH_TO_LABELS = download_labels('mscoco_label_map.pbtxt')

PATH_TO_CFG = PATH_TO_MODEL_DIR + "/pipeline.config"
PATH_TO_CKPT = PATH_TO_MODEL_DIR + "/checkpoint"

IMAGE_PATHS = ['images/' + file for file in os.listdir('./images/')]

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

for image_path in IMAGE_PATHS:

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
	detections = {key: value[0, :num_detections].numpy()
				  for key, value in detections.items()}
	detections['num_detections'] = num_detections

	# detection_classes should be ints.
	detections['detection_classes'] = detections['detection_classes'].astype(
		np.int64)

	label_id_offset = 1
	image_np_with_detections = image_np.copy()

	viz_utils.visualize_boxes_and_labels_on_image_array(
		image_np_with_detections,
		detections['detection_boxes'],
		detections['detection_classes']+label_id_offset,
		detections['detection_scores'],
		category_index,
		use_normalized_coordinates=True,
		max_boxes_to_draw=200,
		min_score_thresh=.30,
		agnostic_mode=False)

	width, height = image.size
	plt.figure(figsize=(width / 100, height / 100), dpi=100)
	plt.imshow(image_np_with_detections)
	plt.savefig('identified_' + image_path, dpi=100)
	print('Done')
plt.show(block=True)

# sphinx_gallery_thumbnail_number = 2
