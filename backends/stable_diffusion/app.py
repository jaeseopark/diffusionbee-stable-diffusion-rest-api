import io
import os

from PIL import Image
from flask import Flask, request, jsonify, send_file

from diffusionbee_backend import process_opt as _process_opt, get_generator, tdict_collection_path

# Initialize Flask app
app = Flask(__name__)
generator = get_generator()

def process_opt(req: dict, *args, **kwargs):
    req["model_tdict_path"] = os.path.join(tdict_collection_path, req["model_tdict_filename"])
    return _process_opt(req, *args, **kwargs)


@app.route("/generate/single", methods=["POST"])
def generate_image():
    if request.json.get("num_imgs", 1) > 1:
        return jsonify({"error": "Only single image allowed for this endpoint"}), 400

    outs = process_opt(request.json, generator=generator, should_save_locally=False)

    image = Image.fromarray(outs['img'][0])

    img_byte_array = io.BytesIO()
    image.save(img_byte_array, format='png')
    img_byte_array.seek(0) # Rewind the byte array to the start

    return send_file(img_byte_array, mimetype="image/png")

@app.route("/generate", methods=["POST"])
def generate_images():
    raise NotImplementedError
    outs = process_opt(request.json, generator=generator, should_save_locally=False)
    imgs = outs['img']

    # Convert to byte array
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format="PNG")
    img_byte_arr = img_byte_arr.getvalue()

    return img_byte_arr, 200, {'Content-Type': 'image/png'}

@app.get("/tdicts")
def get_tdict_filenames():
    return dict(filenames=os.listdir(tdict_collection_path)), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
