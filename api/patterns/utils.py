import json

import requests
from rest_framework.exceptions import APIException

from backend.settings import STABLE_DIFF_API_KEY


def generate_img(prompt: str) -> str:

    url = 'https://modelslab.com/api/v6/realtime/text2img'

    payload = json.dumps({
        'key': STABLE_DIFF_API_KEY,
        'prompt': f'Sewing pattern with these parameters: {prompt}',
        'negative_prompt': 'bad quality',
        'width': '512',
        'height': '512',
        'safety_checker': False,
        'seed': None,
        'samples': 1,
        'base64': False,
        'webhook': None,
        'track_id': None
    })

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, data=payload)

    try:
        return response.json()['output']
    except KeyError:
        raise APIException({'stableDiffusion_api_key_err': response.json()['message']}, 500)
