import os
import sys
import time
import Log
import OperatingSystem
from Captcha import Captcha
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

TIMEOUT = 10
ROOT_DIR = sys.path[1]
platform = OperatingSystem.get_platform()
web_driver = OperatingSystem.get_web_driver()
driver_path = ROOT_DIR + '\\assets\\web\\' + platform + '\\' + web_driver
driver = webdriver.Chrome(driver_path)


def document_initialised(driver):
    return driver.execute_script("return initialised")


if __name__ == '__main__':
    # driver.set_window_size(900, 960)
    driver.set_window_position(0, 0)
    driver.get('https://demos.telerik.com/aspnet-ajax/captcha/examples/overview/defaultcs.aspx')
    print(driver.current_url)

    i = 0
    j = 0
    while True:
        present_element = EC.presence_of_element_located((By.ID, 'example'))
        WebDriverWait(driver, TIMEOUT).until(present_element)

        # Page submitted successfully!
        if i > 0:
            is_success = driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceholder1_lblCorrectCode"]').is_displayed()
            if is_success:
                j += 1
            Log.info('Prediction is : {}'.format(is_success))
            Log.info('Prediction percentage : {}%'.format((j/i)*100))

        img_captcha = driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceholder1_RadCaptcha1_CaptchaImage"]')
        img_url = img_captcha.get_attribute('src')
        Log.info('Image url : {}'.format(img_url))

        captcha = Captcha()
        captcha.url(img_url)
        img_original = captcha.get_img()
        img_resize = captcha.resize(img_original, 400)
        img_noise = captcha.noisereduce(img_resize)
        img_noise_threshold = captcha.thresholding(img_noise)
        prediction = captcha.solve(img_noise_threshold, 10)
        Log.info('Captcha is : {}'.format(prediction))

        input_captcha = driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceholder1_RadCaptcha1_CaptchaTextBox"]')
        input_captcha.send_keys(prediction)

        btn_captcha = driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceholder1_btnVerify"]')
        btn_captcha.send_keys(Keys.ENTER)

        i += 1

