import requests
from rest_framework.exceptions import APIException

from backend.settings import STABLE_DIFF_API_KEY


def generate_img(prompt: str) -> str:

    # url = 'https://modelslab.com/api/v6/realtime/text2img'

    # payload = json.dumps({
    #     'key': STABLE_DIFF_API_KEY,
    #     'prompt': f'Sewing pattern with these parameters: {prompt}',
    #     'negative_prompt': 'bad quality',
    #     'width': '512',
    #     'height': '512',
    #     'safety_checker': False,
    #     'seed': None,
    #     'samples': 1,
    #     'base64': False,
    #     'webhook': None,
    #     'track_id': None
    # })

    # headers = {
    #     'Content-Type': 'application/json'
    # }

    # response = requests.post(url, headers=headers, data=payload)
    headers = {'Authorization': f'Bearer {STABLE_DIFF_API_KEY}'}

    url = 'https://api.edenai.run/v2/image/generation'
    payload = {
        'providers': 'replicate',
        'resolution': '1024x1024',
        'text': f'Sewing pattern with these parameters: {prompt}',
        'fallback_providers': '',
        'response_as_dict': True,
        'attributes_as_list': False,
        'show_original_response': False,
        'settings': {},
        'num_images': 1
    }

    response = requests.post(url, json=payload, headers=headers)

    try:
        return response.json()['replicate']['items'][0]['image_resource_url']
    except KeyError:
        raise APIException({'api_generation_err': response.json()['error']['type']}, 500)
