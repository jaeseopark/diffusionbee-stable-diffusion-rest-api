import io
import os

from PIL import Image
from flask import Flask, request, send_file

from diffusionbee_backend import process_opt as _process_opt, get_generator, tdict_dirs

# Initialize Flask app
app = Flask(__name__)
generator = get_generator()

def process_opt(req: dict, *args, **kwargs):
    filename = req["model_tdict_filename"]
    for tdict_dir in tdict_dirs:
        if filename in os.listdir(tdict_dir):
            req["model_tdict_path"] = os.path.join(tdict_dir, filename)
            return _process_opt(req, *args, **kwargs)
    raise FileNotFoundError(f"tdict {filename=} not found")


@app.route("/generate/single", methods=["POST"])
def generate_image():
    if request.json.get("num_imgs", 1) > 1:
        return dict(error="Only single image allowed for this endpoint"), 400

    try:
        outs = process_opt(request.json, generator=generator, should_save_locally=False)
    except FileNotFoundError as e:
        return dict(error=str(e)), 400

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
    image.save(img_byte_arr, format="jpeg", quality=70, optimize=True, progressive=True)
    img_byte_arr = img_byte_arr.getvalue()

    return img_byte_arr, 200, {'Content-Type': 'image/jpeg'}

@app.get("/tdicts")
def get_tdict_filenames():
    filenames = [filename for dirname in tdict_dirs for filename in os.listdir(dirname)]
    return dict(filenames=filenames), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5825)
