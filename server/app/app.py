import os

import requests

from dotenv import load_dotenv
from flask import Flask, request, app

from bunnies import get_bunny_url
from image_processing import convert_image

load_dotenv()
app = Flask(__name__)

USER_AGENT = 'bunny-bot/1.0 (aleksejs@popovs.lv)'
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET')

def download_url(url: str) -> bytes:
	result = requests.get(url, headers={'User-Agent': USER_AGENT})
	result.raise_for_status()
	return result.content

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/bunny')
def bunny():
	secret = request.args.get('secret')
	if secret != CLIENT_SECRET:
		return ('wrong secret', 401)

	bunny_url = get_bunny_url(TWITTER_API_KEY, TWITTER_API_SECRET)
	bunny_bytes = download_url(bunny_url)
	bunny_bmp = convert_image(bunny_bytes)

	return (
		bunny_bmp,
		200,
		{'Content-Type': 'image/bmp'},
	)
