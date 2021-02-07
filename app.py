from io import BytesIO
from flask import Flask, jsonify, send_file, request
from PIL import Image
import numpy as np
import json
from image import compose_focus_effect
import hashlib
import os
from urllib.parse import urlsplit, parse_qs

app = Flask(__name__)
# detect_fn = load_model()

CACHE_FOLDER = './cache/'
STATIC_FOLDER = 'static/uploads/'
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

@app.errorhandler(Exception)
def handle_error(e):
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

@app.route("/")
def index():
    return app.send_static_file('index.html')

@app.route("/upload", methods=["POST"])
def post_file():
	"""Upload a file."""

	image = Image.open(BytesIO(request.data))
	id = hashlib.md5(image.tobytes()).hexdigest()

	filename = id + '.png'

	image.save(STATIC_FOLDER + filename, 'PNG')

	width, height = image.size

	if (width > height):
		ratio = width / 640
		image.resize((640, int(height / ratio))).save(STATIC_FOLDER + 'preview_' + filename, 'PNG')
	else:
		ratio = height / 640
		image.resize((int(width / ratio), 640)).save(STATIC_FOLDER + 'preview_' + filename, 'PNG')

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
	query = urlsplit(request.url).query
	params = {k: v[0] for k, v in parse_qs(query).items()}
	settings = {
		"speeds": [1],
		"steps": 5,
		"distances": [5],
		"showBorders": False,
		"width": None,
		"boxes": [],
	}
	settings.update(params)
	settings["boxes"] = json.loads(settings["boxes"])
	settings["speeds"] = json.loads(settings["speeds"])
	settings["distances"] = json.loads(settings["distances"])
	source, background, composition, frames = compose_focus_effect(image, settings)
	# composition.save(STATIC_FOLDER + id + '.jpg', 'JPEG', optimize=True, quality=80, progressive=True)
	img_io = BytesIO()
	composition.save(img_io, 'PNG')
	img_io.seek(0)

	return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)