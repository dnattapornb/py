import cv2
import pytesseract
from urllib.request import urlopen
import numpy as np


def detect_characters(cf=''):
    img_path = 'assets/image/test/normal-type.jpg'
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # print(pytesseract.image_to_string(img))
    # print(pytesseract.image_to_boxes(img))

    hImg, wImg, _ = img.shape
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


def detect_words(cf=''):
    img_path = 'assets/image/test/normal-type.jpg'
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # print(pytesseract.image_to_string(img))
    # print(pytesseract.image_to_boxes(img))
    hImg, wImg, _ = img.shape
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


def solve_captcha(cf=''):
    # url = 'https://demos.telerik.com/aspnet-ajax/Telerik.Web.UI.WebResource.axd?type=rca&isc=true&guid=97c82a00-ebd7-4ccf-94f3-ef064b2daa34'
    # resp = urlopen(url)
    # img_original = np.asarray(bytearray(resp.read()), dtype="uint8")
    # img_original = cv2.imdecode(img_original, cv2.IMREAD_UNCHANGED)
    # print('Original Dimensions : ', img_original.shape)

    img_path = 'assets/image/test/captcha/58PXX.jpg'
    img_original = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    # img_original = cv2.cvtColor(img_original, cv2.COLOR_BGR2HSV)
    print('Original Dimensions : ', img_original.shape)

    scale_percent = 300  # percent of original size
    width = int(img_original.shape[1] * scale_percent / 100)
    height = int(img_original.shape[0] * scale_percent / 100)
    dim = (width, height)
    img_resized = cv2.resize(img_original, dim, interpolation=cv2.INTER_AREA)
    print('Resized Dimensions : ', img_resized.shape)

    img_gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
    # print('Gray Dimensions : ', img_gray.shape)

    (thresh, img_black_white) = cv2.threshold(img_gray, 150, 255, cv2.THRESH_BINARY)
    # (thresh, img_black_white) = cv2.threshold(img_gray, 190, 255, cv2.THRESH_TOZERO)
    # print('Black white Dimensions : ', img_black_white.shape)

    # cv2.imshow('Original image', img_original)
    # cv2.imshow('Gray image', img_gray)
    # cv2.imshow('Black white image', img_black_white)

    ans = ''
    hImg, wImg = img_black_white.shape
    boxes = pytesseract.image_to_boxes(img_black_white, config=cf, lang='eng')
    for b in boxes.splitlines():
        # print(b)
        b = b.split(' ')
        # print(b)
        if b[0] not in ['.', ':', '\'']:
            ans += b[0]
        x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])

        cv2.rectangle(img_resized, (x, hImg - y), (w, hImg - h), (0, 0, 255), 2)
        cv2.putText(img_resized, b[0], (x, hImg - y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 50, 255), 2)

        cv2.rectangle(img_gray, (x, hImg - y), (w, hImg - h), (0, 0, 255), 2)

        cv2.rectangle(img_black_white, (x, hImg - y), (w, hImg - h), (0, 0, 255), 2)

    print('Captcha is : {}'.format(ans))
    cv2.imshow('Original image', img_resized)
    cv2.imshow('Gray image', img_gray)
    cv2.imshow('Black white image', img_black_white)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    print('tesseract version : {}'.format(pytesseract.get_tesseract_version()))
    print('tesseract support languages : {}'.format(pytesseract.get_languages()))

    conf = r'--oem 3 --psm 10'
    # conf = r'--oem 3 --psm 6 outputbase digits'
    # detect_characters(conf)
    # detect_words(conf)
    solve_captcha(conf)
