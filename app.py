from io import BytesIO
from flask import Flask, jsonify, send_file, request, render_template
from PIL import Image
import numpy as np
import json
from image import compose_focus_effect
import hashlib
import os

app = Flask(__name__)
# detect_fn = load_model()

CACHE_FOLDER = './cache/'
STATIC_FOLDER = 'static/'
if not os.path.exists(CACHE_FOLDER):
	os.makedirs(CACHE_FOLDER)
if not os.path.exists(STATIC_FOLDER):
	os.makedirs(STATIC_FOLDER)

@app.after_request # blueprint can also be app~~
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    header['Access-Control-Allow-Headers'] = '*'
    return response

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def post_file():
	"""Upload a file."""

	image = Image.open(BytesIO(request.data))
	id = hashlib.md5(image.tobytes()).hexdigest()

	filename = id + '.png'
	image.save(STATIC_FOLDER + filename, 'PNG')

	return jsonify({
		"filename": filename
	})

@app.route("/composition/<filename>", methods=["GET"])
def get_composition(filename):
	#(boxes, masks) = generate_boxes_and_masks(detect_fn, image_np, cache_location=CACHE_FOLDER + id, max_highlights=5)
#
	#if len(masks) < 1:
	#	return jsonify({
	#		"detections": 0,
	#	})
	image = Image.open(STATIC_FOLDER + filename)
	#image_np = np.array(image.convert('RGB'))

	boxes = request.args.get('boxes')
	clientWidth = request.args.get('width')
	boxes = json.loads(boxes)
	print('compose')
	source, background, composition, frames = compose_focus_effect(image, boxes, clientWidth)
	# composition.save(STATIC_FOLDER + id + '.jpg', 'JPEG', optimize=True, quality=80, progressive=True)
	print('saving')
	img_io = BytesIO()
	composition.save(img_io, 'PNG')
	img_io.seek(0)
	print('done')

	return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)