import cv2
from datetime import datetime
from PIL import Image, ImageOps
import numpy as np
import matplotlib.pyplot as plt
import os

def get_image(image_name):
	image_path = 'images/' + image_name
	return Image.open(image_path)

def save_image(image_name, image_np, mask_np, prefix = ''):
	if not os.path.exists('identified_images'):
		os.makedirs('identified_images')


	image = Image.fromarray(np.uint8(image_np)).convert('RGB')

	background = Image.new('RGBA', image.size, (255, 0, 0, 0))

	mask = Image.fromarray(np.uint8(mask_np)).convert('L').point(lambda x: 0 if x<128 else 255, '1')

	result = Image.composite(image, background, mask)
	result.save('identified_images/' + datetime.now().strftime("%d-%m-%Y_%H-%M-%S")  + '_object' + '_' + image_name, 'PNG')

	inverted_mask = ImageOps.invert(mask.convert('RGB')).convert('L')
	result = Image.composite(image, background, inverted_mask)
	result.save('identified_images/' + datetime.now().strftime("%d-%m-%Y_%H-%M-%S")  + '_rest' + '_' + image_name, 'PNG')
