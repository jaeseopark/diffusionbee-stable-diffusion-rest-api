# Diffusion Bee Rest API

A Rest API wrapper around the Diffusion Bee application.

More info about the underlying app at https://diffusionbee.com/

## Development

```shell
git clone https://github.com/jaeseopark/diffusionbee-stable-diffusion-ui

cd diffusionbee-stable-diffusion-ui/backends/stable_diffusion

brew install pyenv
pyenv install $(cat .python-version)

python3 -m venv venv
source venv/bin/activate
pip install pip --upgrade
pip install -r requirements.txt
```

```shell
cd backends/stable_diffusion
source venv/bin/activate
python3 app.py
```

### Tdicts 

```shell
curl -s http://localhost:5825/tdicts
```

The response, when only 1 model is installed:

```json
{ "filenames": [ "Default_SDB_0.1_SDB_0.1.tdict" ] }
```

### Payload

See [`sd_run.py`](backends/stable_diffusion/stable_diffusion/sd_run.py) for the full list of arguments. Most args are optional and will get assigned default values.

| Parameter            | Type/Description                                           | Is Required | Notes                                               |
|----------------------|------------------------------------------------------------|-------------|-----------------------------------------------------|
| model_tdict_filename | Filename of the model. Ex. `Default_SDB_0.1_SDB_0.1.tdict` | Yes         | Grab from the response from the `/tdicts` endpoint. |
| prompt               | Prompt for the generation                                  | Yes         | Up to 77 words                                      |

### Single image

```shell
curl -X POST http://localhost:5825/generate/single \
  -H "Content-Type: application/json" \
  -d @payload.json \
  -o generated_image.jpeg
```

### Multiple images

```shell
curl -X POST http://localhost:5825/generate \
  -H "Content-Type: application/json" \
  -d @payload.json \
  -o generated_images.zip
```
