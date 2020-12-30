import alarm
import board
import digitalio
import displayio
import wifi
import socketpool
import ssl
import adafruit_requests
import adafruit_imageload.bmp
import time

from alarm.time import TimeAlarm
from io import BytesIO

from config import config

print('booted')

neopixel_disable = digitalio.DigitalInOut(board.NEOPIXEL_POWER)
neopixel_disable.direction = digitalio.Direction.OUTPUT
neopixel_disable.value = True

speaker_enable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
speaker_enable.direction = digitalio.Direction.OUTPUT
speaker_enable.value = False

wifi.radio.connect(config['wifi_ssid'], config['wifi_key'])
pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())

print('connected to wifi')

response = requests.get(config['endpoint'])

print('downloaded bunny')

bunny_bytes = response.content
bunny_io = BytesIO(bunny_bytes)

group = displayio.Group()
bitmap, _ = adafruit_imageload.bmp.load(bunny_io, bitmap=displayio.Bitmap)
palette = displayio.Palette(4)
for i in range(4):
	palette[i] = 0x555555 * i
tile = displayio.TileGrid(bitmap, pixel_shader=palette, x=0, y=0)
group.append(tile)

board.DISPLAY.show(group)
board.DISPLAY.refresh()
print('displayed')

# if you go into deep sleep right after calling refresh(),
# the board might power off before the refresh is complete
time.sleep(5)

print('going to sleep')
time_alarm = TimeAlarm(monotonic_time=time.monotonic() + 30 * 60)
alarm.exit_and_deep_sleep_until_alarms(time_alarm)
