import os
import sys
import cv2
import numpy as np
from ppadb.client import Client as AdbClient

ROOT_DIR = sys.path[1]
img_name = 'screen'
img_path = ROOT_DIR + '/assets/image/screenshot/' + img_name + '.png'

# Default is "127.0.0.1" and 5037
client = AdbClient(host="127.0.0.1", port=5037)
print('Client version : %d' % client.version())
devices = client.devices()
print('Count devices : %d' % len(devices))

for device in devices:
    print('Device %s' % device.serial)
    print('CPU : %d' % (device.cpu_count()))
    emu_size = device.wm_size()
    print(emu_size)
    print('Width : %d' % emu_size.width)
    print('Height : %d' % emu_size.height)
    print("\n")

device = client.device("emulator-5554")

while True:
    result = device.screencap()
    with open(img_path, 'wb') as fp:
        fp.write(result)

    img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    cv2.imshow(f"HoughLines", img)
    cv2.waitKey(1)
