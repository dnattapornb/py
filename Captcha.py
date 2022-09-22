import os
import cv2
import pytesseract
import numpy as np
from urllib.request import urlopen
from matplotlib import pyplot as plt


class Captcha:

    def __init__(self):
        self.img_url = None
        self.img_path = None
        self.img_original = None

    def path(self, path):
        self.img_path = path
        self.img_original = cv2.imread(self.img_path, cv2.IMREAD_UNCHANGED)

    def url(self, url):
        self.img_url = url
        resp = urlopen(url)
        self.img_original = np.asarray(bytearray(resp.read()), dtype="uint8")
        self.img_original = cv2.imdecode(self.img_original, cv2.IMREAD_UNCHANGED)

    def get_img(self):
        return self.img_original

    @staticmethod
    def resize(image, scale_percent=400):
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        dim = (width, height)
        return cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

    @staticmethod
    def blur(image):
        return cv2.medianBlur(image, 5)

    @staticmethod
    def noisereduce(image, h=22.5):
        return cv2.fastNlMeansDenoisingColored(image, None, h, 20, 15, 21)

    @staticmethod
    def thresholding(image, threshold=153):
        return cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)[1]

    @staticmethod
    def show(image, title='image'):
        cv2.imshow(title, image)

    @staticmethod
    def solve(image, psm=10):
        cf = r'-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ --oem 3 --psm {}'.format(psm)
        prediction = pytesseract.image_to_string(image, config=cf, lang='eng')
        prediction = "".join(prediction.split())

        return prediction

    def __solve__(self, image, psm=10):
        cf = r'-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ --oem 3 --psm {}'.format(psm)
        prediction = ''
        hImg, wImg, _ = image.shape
        boxes = pytesseract.image_to_boxes(image, config=cf, lang='eng')
        for box in boxes.splitlines():
            box = box.split(' ')
            prediction += box[0]

            x, y, w, h = int(box[1]), int(box[2]), int(box[3]), int(box[4])
            cv2.rectangle(image, (x, hImg - y), (w, hImg - h), (0, 0, 255), 2)
            cv2.putText(image, box[0], (x, hImg - y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 50, 255), 2)

        self.show(self.img_original, 'Original')
        self.show(image, 'Solve')

        return prediction


def test():
    captcha = Captcha()
    captcha.path('assets/image/captcha/1A3RQ.jpg')
    img_original = captcha.resize(captcha.img_original, 400)
    img_blur = captcha.blur(img_original)
    img_noise = captcha.noisereduce(img_original)
    img_original_threshold = captcha.thresholding(img_original)
    img_blur_threshold = captcha.thresholding(img_blur)
    img_noise_threshold = captcha.thresholding(img_noise)

    numpy_horizontal = np.hstack((img_original, img_original_threshold))
    numpy_horizontal_concat = np.concatenate((img_original, img_original_threshold), axis=1)

    captcha.show(img_original, 'original')
    captcha.show(img_blur, 'blur')
    captcha.show(img_noise, 'noise')
    captcha.show(img_original_threshold, 'original to threshold')
    captcha.show(img_blur_threshold, 'blur to threshold')
    captcha.show(img_noise_threshold, 'noise to threshold')

    # call imshow() using plt object
    plt.imshow(numpy_horizontal_concat)

    # display that image
    plt.show()

    prediction = captcha.__solve__(img_noise_threshold, 10)
    print(prediction)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    test()
    exit()

    images = []
    path = "assets/image/captcha"  # Get the list of all files and directories
    dir_list = os.listdir(path)
    for file in dir_list:
        images.append([file[0:-4], path + '/' + file])

    i = 0
    for image in images:
        captcha = Captcha()
        captcha.path(image[1])
        img_original = captcha.get_img()
        img_resize = captcha.resize(img_original, 400)
        img_noise = captcha.noisereduce(img_resize)
        img_noise_threshold = captcha.thresholding(img_noise)
        prediction = captcha.solve(img_noise_threshold, 10)

        if len(prediction) != 5:
            img_noise = captcha.noisereduce(img_resize, 23.5)
            img_noise_threshold = captcha.thresholding(img_noise)
            prediction = captcha.solve(img_noise_threshold, 8)

        file_name = image[0].upper().replace('0', 'O')
        prediction = prediction.upper().replace('0', 'O')
        success = (file_name == prediction)
        if success:
            i += 1
        print('Captcha is : [{}] , Prediction is [{}] , {}'.format(file_name, prediction, success))

    print('{}/{}'.format(i, len(images)))
