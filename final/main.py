from detect import generate_boxes_and_masks
from image import compose_focus_effect, get_image_np
from model import load_model
from glob import glob
import os
import tensorflow as tf
import warnings

def main():
	CACHE_PATH = 'cache/'
	os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
	tf.get_logger().setLevel('ERROR')
	warnings.filterwarnings('ignore')

	detect_fn = load_model()

	if not os.path.exists(CACHE_PATH):
		os.makedirs(CACHE_PATH)

	extensions = ['jpg', 'jpeg', 'png']

	for extension in extensions:
		for image_path in glob('./input_images/*.' + extension):
			image_name = os.path.basename(image_path)
			cache_file = CACHE_PATH + image_name

			print('Loading {}... '.format(image_name))
			image_np = get_image_np(image_name)

			boxes_and_masks = generate_boxes_and_masks(detect_fn, image_np, cache_file, max_highlights=5)
			compose_focus_effect(image_name, image_np, boxes_and_masks)

			print('Completed ' + image_name)

	print('Task complete')

if __name__ == "__main__":
    main()