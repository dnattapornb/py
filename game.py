import os
import sys
import cv2
from ppadb.client import Client as AdbClient

ROOT_DIR = sys.path[1]
img_name = 'screen'
img_path = ROOT_DIR + '/assets/image/screenshot/' + img_name + '.png'

# Default is "127.0.0.1" and 5037
client = AdbClient(host="127.0.0.1", port=5037)
devices = client.devices()
for device in devices:
    print(device.serial)

print(client.version())

device = client.device("emulator-5554")
result = device.screencap()
with open(img_path, 'wb') as fp:
    fp.write(result)
