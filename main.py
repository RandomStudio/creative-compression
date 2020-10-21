from detect import detect_objects_in_image, visualize_detections
from image import get_image, save_image
from model import download_labels, download_model, load_model

from models.research.object_detection.utils import label_map_util
import numpy as np
import os
import tensorflow as tf
import warnings

# Silence warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
tf.get_logger().setLevel('ERROR')
warnings.filterwarnings('ignore')

detect_fn = load_model()
labels_path = download_labels('mscoco_label_map.pbtxt')
category_index = label_map_util.create_category_index_from_labelmap(labels_path, use_display_name=True)

for image_name in os.listdir('./images/'):
	print('Running inference for {}... '.format(image_name))

	image = get_image(image_name)
	image_np = np.array(image.convert('RGB'))

	detections = detect_objects_in_image(image_np, detect_fn)
	image_np_with_detections = visualize_detections(image_np, detections, category_index)

	save_image(image_name, image_np_with_detections)

	print('Done')

print('Task complete')