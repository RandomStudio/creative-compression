import cv2
from datetime import datetime
from PIL import Image, ImageOps
import numpy as np
import matplotlib.pyplot as plt
import os

def get_image(image_name):
	image_path = 'images/' + image_name
	return Image.open(image_path)

def mask_image(image_name, image_np, mask_np):
	if not os.path.exists('identified_images'):
		os.makedirs('identified_images')

	filename, file_extension = os.path.splitext(image_name)

	image = Image.fromarray(np.uint8(image_np)).convert('RGB')

	background = Image.new('RGBA', image.size, (255, 0, 0, 0))

	mask = Image.fromarray(np.uint8(mask_np)).convert('L').point(lambda x: 0 if x<128 else 255, '1')

	result = Image.composite(image, background, mask)
	result.save('identified_images/' + datetime.now().strftime("%d-%m-%Y_%H-%M-%S")  + '_object' + '_' + filename + '.png', 'PNG')
	result.save('playground/object.png', 'PNG')

	inverted_mask = ImageOps.invert(mask.convert('RGB')).convert('L')
	result = Image.composite(image, background, inverted_mask).convert('RGB')
	result.save('identified_images/' + datetime.now().strftime("%d-%m-%Y_%H-%M-%S")  + '_rest' + '_' + filename + '.jpg', 'JPEG',optimize=True,quality=10)
	result.save('playground/rest.jpg', 'JPEG',optimize=True,quality=10)
