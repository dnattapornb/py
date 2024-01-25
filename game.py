import os
import sys
import cv2
import numpy as np
from ppadb.client import Client as AdbClient

ROOT_DIR = sys.path[1]
img_name = 'screen'
# img_path = ROOT_DIR + '/assets/image/screenshot/' + img_name + '.png'
img_path = 'C:\\Users\\ABOY\\Documents\\py\\assets\\image\\screenshot\\' + img_name + '.png'

# Default is "127.0.0.1" and 5037
client = AdbClient(host="127.0.0.1", port=5037)
print('Client version : %d' % client.version())
devices = client.devices()
print('Count devices : %d' % len(devices))

if len(devices) == 0:
    print('Invalid device attached')
    quit()

for device in devices:
    print('Device %s' % device.serial)
    print('CPU : %d' % (device.cpu_count()))
    emu_size = device.wm_size()
    print(emu_size)
    print('Width : %d' % emu_size.width)
    print('Height : %d' % emu_size.height)
    print("\n")

device = client.device("emulator-5564")

while True:
    result = device.screencap()
    with open(img_path, 'wb') as fp:
        fp.write(result)

    img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)

    # percent by which the image is resized
    scale_percent = 50

    # calculate the 50 percent of original dimensions
    width = int(emu_size.width * scale_percent / 100)
    height = int(emu_size.height * scale_percent / 100)

    # dsize
    dsize = (width, height)

    # resize image
    output = cv2.resize(img, dsize)


    cv2.imshow(f"@BOY", output)
    cv2.waitKey(1)
