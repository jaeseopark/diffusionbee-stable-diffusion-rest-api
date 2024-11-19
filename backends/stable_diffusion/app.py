import io
import os
import threading
import zipfile

from PIL import Image
from flask import Flask, request, send_file

from app_ui_func_provider import UiFuncProvider
from diffusionbee_backend import process_opt as _process_opt, get_generator, tdict_dirs

# Initialize Flask app
app = Flask(__name__)
generator = get_generator()
lock = threading.Lock()

def process_opt(req: dict, *args, **kwargs):
    lock.acquire()
    try:
        return _process_opt(UiFuncProvider(req).get_enriched_payload(), *args, **kwargs)
    finally:
        lock.release()


@app.route("/generate/single", methods=["POST"])
def generate_image():
    if request.json.get("num_imgs", 1) > 1:
        return dict(error="Only single image allowed for this endpoint"), 400

    try:
        imgs = process_opt(request.json, generator=generator, should_save_locally=False)
    except FileNotFoundError as e:
        return dict(error=str(e)), 400

    image = Image.fromarray(imgs[0])

    img_byte_array = io.BytesIO()
    image.save(img_byte_array, format='png')
    img_byte_array.seek(0) # Rewind the byte array to the start

    return send_file(img_byte_array, mimetype="image/png")

@app.route("/generate", methods=["POST"])
def generate_images():
    try:
        imgs = process_opt(request.json, generator=generator, should_save_locally=False)
    except FileNotFoundError as e:
        return dict(error=str(e)), 400

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zf:
        for i, diffused_img in enumerate(imgs):
            img_file_buffer = io.BytesIO()
            pillow_image = Image.fromarray(diffused_img)
            pillow_image.save(img_file_buffer, format="jpeg", quality=70, optimize=True, progressive=True)
            zf.writestr(f"diffused-{i}.jpeg", img_file_buffer.getvalue())
    zip_buffer.seek(0)

    return zip_buffer, 200, {'Content-Type': 'application/zip'}

@app.get("/tdicts")
def get_tdict_filenames():
    filenames = [filename for dirname in tdict_dirs for filename in os.listdir(dirname)]
    return dict(filenames=filenames), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5825)
