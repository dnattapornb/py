import os
import cv2
import time
import pytesseract
import numpy as np
from urllib.request import urlopen
from matplotlib import pyplot as plt


def detect_characters():
    img_path = '../assets/image/normal-type.jpg'
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # print(pytesseract.image_to_string(img))
    # print(pytesseract.image_to_boxes(img))

    hImg, wImg, _ = img.shape
    # conf = r'--oem 3 --psm 6 outputbase digits'
    cf = r'--oem 3 --psm 8'
    boxes = pytesseract.image_to_boxes(img, config=cf)
    for b in boxes.splitlines():
        print(b)
        b = b.split(' ')
        print(b)
        x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
        cv2.rectangle(img, (x, hImg - y), (w, hImg - h), (0, 0, 255), 2)
        cv2.putText(img, b[0], (x, hImg - y - 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 50, 255), 2)

    cv2.imshow('Test', img)
    cv2.waitKey()


def detect_words():
    img_path = '../assets/image/normal-type.jpg'
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # print(pytesseract.image_to_string(img))
    # print(pytesseract.image_to_boxes(img))

    hImg, wImg, _ = img.shape
    # conf = r'--oem 3 --psm 6 outputbase digits'
    cf = r'--oem 3 --psm 8'
    boxes = pytesseract.image_to_data(img, config=cf)
    print(boxes)
    for x, b in enumerate(boxes.splitlines()):
        # index 0 is column name 'level	page_num	block_num	par_num	line_num	word_num	left	top	width	height	conf	text'
        if x != 0:
            b = b.split()
            print(b)
            if len(b) == 12:
                x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
                cv2.rectangle(img, (x, y), (w + x, h + y), (0, 0, 255), 2)
                cv2.putText(img, b[11], (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 50, 255), 2)

    cv2.imshow('Test', img)
    cv2.waitKey()


def solve_captcha():
    img_path = '../assets/image/captcha/4FYLF.jpg'
    img_original = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)

    # gray scale
    # img_gray = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)

    # percent of original size
    scale_percent = 400
    width = int(img_original.shape[1] * scale_percent / 100)
    height = int(img_original.shape[0] * scale_percent / 100)
    dim = (width, height)
    img_original = cv2.resize(img_original, dim, interpolation=cv2.INTER_AREA)

    # reduce noise
    img_original_noiseless = cv2.fastNlMeansDenoisingColored(img_original, None, 22, 20, 15, 21)

    # threshold
    img_original_black_white = cv2.threshold(img_original_noiseless, 153, 255, cv2.THRESH_BINARY)[1]

    predict_captcha = ''
    hImg, wImg, _ = img_original.shape
    cf = r'-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ --oem 3 --psm 10'
    boxes = pytesseract.image_to_boxes(img_original_black_white, config=cf, lang='eng')
    for box in boxes.splitlines():
        box = box.split(' ')
        predict_captcha += box[0]

        x, y, w, h = int(box[1]), int(box[2]), int(box[3]), int(box[4])
        # cv2.rectangle(img_original, (x, hImg - y), (w, hImg - h), (0, 0, 255), 2)
        # cv2.putText(img_original, box[0], (x, hImg - y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 50, 255), 2)
        cv2.rectangle(img_original_black_white, (x, hImg - y), (w, hImg - h), (0, 0, 255), 2)

    print('Captcha is : [{}]'.format(predict_captcha))

    cv2.imshow('Original', img_original)
    cv2.imshow('Original noiseless', img_original_noiseless)
    cv2.imshow('Original to black white', img_original_black_white)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    print('tesseract version : {}'.format(pytesseract.get_tesseract_version()))
    print('tesseract support languages : {}'.format(pytesseract.get_languages()))

    # detect_characters()
    # detect_words()
    solve_captcha()
