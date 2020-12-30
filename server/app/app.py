import functools
import logging
import os

import requests

from dotenv import load_dotenv
from flask import Flask, request, app

from app.bunnies import get_bunny_url
from app.image_processing import convert_image

load_dotenv()
app = Flask(__name__)
app.logger.setLevel(logging.INFO)

USER_AGENT = 'bunny-bot/1.0 (aleksejs@popovs.lv)'
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET')

def device_auth(view):
	@functools.wraps(view)
	def wrapped_view(**kwargs):
		if CLIENT_SECRET is None:
			return ('no secret configured', 500)

		secret = request.args.get('secret', request.headers.get('x-device-secret'))
		if secret != CLIENT_SECRET:
			return ('wrong secret', 401)

		return view(**kwargs)

	return wrapped_view

def report_battery_voltage(view):
	@functools.wraps(view)
	def wrapped_view(**kwargs):
		battery_voltage_s = request.headers.get('x-battery-voltage')
		if battery_voltage_s is not None:
			battery_voltage = float(battery_voltage_s)
			app.logger.info('battery: %.2fV', battery_voltage)

		return view(**kwargs)

	return wrapped_view

def download_url(url: str) -> bytes:
	result = requests.get(url, headers={'User-Agent': USER_AGENT})
	result.raise_for_status()
	return result.content

@app.route('/')
def hello_world():
	return 'Hello, World!'

@app.route('/bunny')
@device_auth
@report_battery_voltage
def bunny():
	bunny_url = get_bunny_url(TWITTER_API_KEY, TWITTER_API_SECRET)
	bunny_bytes = download_url(bunny_url)
	bunny_bmp = convert_image(bunny_bytes)

	return (
		bunny_bmp,
		200,
		{'Content-Type': 'image/bmp'},
	)
