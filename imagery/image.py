from PIL import ImageFilter
import cv2
from datetime import datetime
from PIL import Image, ImageOps
import numpy as np
import matplotlib.pyplot as plt
import os

def get_image(image_name):
	image_path = 'images/' + image_name
	return Image.open(image_path)

def extract_object(image_name, image_np, mask_np, suffix = ''):
	if not os.path.exists('identified_images'):
		os.makedirs('identified_images')

	image = Image.fromarray(np.uint8(image_np)).convert('RGB')

	background = Image.new('RGBA', image.size, (255, 0, 0, 0))

	mask = Image.fromarray(np.uint8(mask_np)).convert('L').point(lambda x: 0 if x<128 else 255, '1').convert('RGB').filter(ImageFilter.GaussianBlur).convert('L')
	result = Image.composite(image, background, mask).convert('RGBA')
	result.save('playground/object' + suffix + '.png', 'PNG')

def save_background(image_name, image_np):
	image = Image.fromarray(np.uint8(image_np)).convert('RGB')
	result = image.convert('RGB')
	result.save('playground/rest.jpg', 'JPEG',optimize=True,quality=10)
