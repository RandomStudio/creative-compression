from datetime import datetime
from PIL import Image
import matplotlib.pyplot as plt
import os

def get_image(image_name):
	image_path = 'images/' + image_name
	return Image.open(image_path)

def save_image(image_name, image_np_with_detections):
	if not os.path.exists('identified_images'):
		os.makedirs('identified_images')
	image = get_image(image_name)
	width, height = image.size
	plt.figure(figsize=(width / 100, height / 100), dpi=100)
	plt.imshow(image_np_with_detections)
	plt.savefig('identified_images/' + datetime.now().strftime("%d-%m-%Y_%H-%M-%S")  + '_' + image_name, dpi=100)
