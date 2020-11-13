from PIL import Image
from model import detect_objects_in_image
import numpy as np
import shelve
import cv2

def do_inference(detect_fn, image_np, cache_location):
	if cache_location == None:
		return detect_objects_in_image(image_np, detect_fn)
	cache = shelve.open(cache_location)
	if 'cached_detections' in cache:
		print('Loaded detections from cache.')
		return cache['cached_detections']

	print('Running inference...')
	cache['cached_detections'] = detect_objects_in_image(image_np, detect_fn)
	cache.sync()
	return cache['cached_detections']

def generate_boxes_and_masks(detect_fn, image_np, cache_location=None, max_highlights=None):
	image = Image.fromarray(image_np.copy())
	width, height = image.size
	smallSize = (int((640 / height) * width), 640)
	image = image.resize(smallSize)
	detection_image_np = np.array(image.convert('RGB'))

	detections = do_inference(detect_fn, detection_image_np, cache_location)

	boxes = []
	masks = []
	for index, detection_mask in enumerate(detections.get('detection_masks_reframed')):
		if detections["detection_scores"][0][index] > 0.8 and (max_highlights == None or index < max_highlights):
			boxes.append(np.asarray(detections.get('detection_boxes')[0][index]).tolist())
			masks.append(detection_image_np.shape[0] * detection_mask)

	return (boxes, masks)
