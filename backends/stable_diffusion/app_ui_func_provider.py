"""
The backend is closely integrated with the electron frontend and some functionalities are implemented on the ui side as well.
The Rest API is going to need eto 'mock' the UI's functionalities to be able to bring parity.
"""
import os
from types import SimpleNamespace

from diffusionbee_backend import tdict_dirs

_SD_STYLE_MAP = {
    "cinematic": SimpleNamespace(apply=lambda
        prompt: f"cinematic film still {prompt} , shallow depth of field, vignette, highly detailed, high budget, bokeh, cinemascope, moody, epic, gorgeous, film grain, grainy")
}


class UiFuncProvider:
    def __init__(self, payload):
        self.payload = {**payload}

    def set_tdict_path(self):
        def get_tdict_path(filename: str):
            for tdict_dir in tdict_dirs:
                if filename in os.listdir(tdict_dir):
                    return os.path.join(tdict_dir, filename)
            raise FileNotFoundError(f"tdict {filename=} not found")

        self.payload["model_tdict_path"] = get_tdict_path(self.payload["model_tdict_filename"])

    def apply_sd_style(self):
        st_transformer = _SD_STYLE_MAP.get(self.payload.get("selected_sd_style"))
        if st_transformer:
            self.payload["prompt"] = st_transformer.apply(self.payload["prompt"])

    def get_enriched_payload(self) -> dict:
        self.set_tdict_path()
        self.apply_sd_style()
        return self.payload
