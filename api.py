from io import BytesIO
from flask import Flask, jsonify, request, render_template
from PIL import Image
import numpy as np
from detect import generate_boxes_and_masks
from image import compose_focus_effect
from model import load_model
import hashlib
import os

api = Flask(__name__)
detect_fn = load_model()

@api.route("/")
def index():
    return render_template("index.html")

@api.route("/upload", methods=["POST"])
def post_file():
	"""Upload a file."""
	CACHE_FOLDER = './cache/'
	STATIC_FOLDER = './static/'
	if not os.path.exists(CACHE_FOLDER):
		os.makedirs(CACHE_FOLDER)
	if not os.path.exists(STATIC_FOLDER):
		os.makedirs(STATIC_FOLDER)

	image = Image.open(BytesIO(request.data))
	image_np = np.array(image.convert('RGB'))
	id = hashlib.md5(image.tobytes()).hexdigest()

	(boxes, masks) = generate_boxes_and_masks(detect_fn, image_np, cache_location=CACHE_FOLDER + id, max_highlights=5)

	if len(masks) < 1:
		return jsonify({
			"detections": 0,
		})

	source, background, composition, frames = compose_focus_effect(image_np, boxes, masks)
	composition.save(STATIC_FOLDER + id + '.jpg', 'JPEG', optimize=True, quality=80, progressive=True)

	return jsonify({
		"detections": len(masks),
		"image": STATIC_FOLDER + id + '.jpg'
	})
