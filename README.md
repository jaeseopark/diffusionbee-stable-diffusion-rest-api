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
# Rest API
cd backends/stable_diffusion
source venv/bin/activate
python3 app.py
```

```shell
# Electron
cd electron_app
npm install
npm run electron:serve
```

### Tdicts 

```shell
curl -s http://localhost:5000/tdicts
```

The response, when only 1 model is installed:

```json
{ "filenames": [ "Default_SDB_0.1_SDB_0.1.tdict" ] }
```

### Payload

See [`sd_run.py`](backends/stable_diffusion/stable_diffusion/sd_run.py) for the full list of arguments. Most args are optional and will get assigned default values.

Mandatory:
* `model_tdict_filename`: Grab from the response from the `/tdicts` endpoint. Ex. `Default_SDB_0.1_SDB_0.1.tdict`
* `prompt`: a string value

### Single image

```shell
curl -X POST http://localhost:5000/generate/single \
  -H "Content-Type: application/json" \
  -d @payload.json \
  -o generated_image.jpeg
```
