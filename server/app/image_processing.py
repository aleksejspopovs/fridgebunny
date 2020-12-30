import subprocess
import tempfile

from io import BytesIO

from PIL import Image

TARGET_WIDTH = 296
TARGET_HEIGHT = 128
BACKGROUND_COLOR = (255, 255, 255)

def resize_image(im: Image) -> Image:
	orig_width, orig_height = im.size

	if orig_width < orig_height:
		# image is portrait, rotate it first
		return resize_image(im.transpose(Image.ROTATE_90))

	scaled_width = TARGET_WIDTH
	scaled_height = round(orig_height * (scaled_width / orig_width))
	if scaled_height > TARGET_HEIGHT:
		scaled_height = TARGET_HEIGHT
		scaled_width = round(orig_width * (scaled_height / orig_height))

	scaled = im.resize((scaled_width, scaled_height))

	result = Image.new('RGB', (TARGET_WIDTH, TARGET_HEIGHT), BACKGROUND_COLOR)
	result.paste(scaled, (
		(TARGET_WIDTH - scaled_width) // 2,
		(TARGET_HEIGHT - scaled_height) // 2
	))

	return result

def einkize_image(im: Image) -> bytes:
	with tempfile.NamedTemporaryFile(suffix='.png') as im_file:
		im.save(im_file.name)

		with tempfile.NamedTemporaryFile(suffix='.bmp') as out_file:
			# I hate to do this, but it seems that PIL cannot do dithering
			# with more than 2 colors in the output
			subprocess.run(
				[
					'convert',
					im_file.name,
					'-dither',
					'FloydSteinberg',
					'-define',
					'dither:diffusion-amount=85%',
					'-remap',
					'./app/eink-4level-palette.png',
					f'BMP3:{out_file.name}',
				],
				check=True,
			)

			return out_file.read()

def convert_image(im_bytes: bytes) -> bytes:
	im_io = BytesIO(im_bytes)
	im = Image.open(im_io)
	return einkize_image(resize_image(im))
