import time
import random
import pathlib
import Log
import OperatingSystem
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Credentials import Credentials


class Web:
    ROOT_DIR = str(pathlib.Path().resolve())
    TIMEOUT = 5

    def __init__(self, site_url, offset_x=0, name='TEST-00'):
        self.name = name
        self.site_url = site_url
        self.window_position_x = 0 + offset_x
        self.window_position_y = 0
        self.window_size_width = 480
        self.window_size_height = 635

        self.driver = None
        self.handle = None
        self.present_element = None
        self.present_element_id = None
        self.password_element = None
        self.username_element = None

        credentials = Credentials()
        self.username = credentials.get_username()
        self.password = credentials.get_password()

        self.driver_path = ''
        self.log_path = ''
        self.init_path()

        self.random_number = random.randint(10, 20)

        self.create()

    def init_path(self):
        platform = OperatingSystem.get_platform()
        web_driver = 'chromedriver'
        if platform == 'mac':
            web_driver = 'chromedriver'
        elif platform == 'win':
            web_driver = 'chromedriver.exe'
        self.driver_path = Web.ROOT_DIR + '/assets/web/' + platform + '/' + web_driver
        self.log_path = Web.ROOT_DIR + '/assets/log/'

    def create(self):
        self.driver = webdriver.Chrome(self.driver_path)
        self.driver.set_window_size(self.window_size_width, self.window_size_height)
        self.driver.set_window_position(self.window_position_x, self.window_position_y)
        self.driver.get(self.site_url)
        self.handle = self.driver.window_handles[0]
        Log.info('{} Open web : {}'.format(self.name, self.handle))

    def get_handle(self):
        return self.handle

    def save_page_source(self):
        file_name = '%s_%s.txt' % (self.name, datetime.now().strftime("%Y-%m-%dT%H.%M.%S"))
        with open(self.log_path + file_name, 'w', encoding='utf-8') as f:
            try:
                f.write(self.driver.page_source)
            except Exception as e:
                print(e)
            finally:
                f.close()

    def login(self):
        self.save_page_source()
        Log.info(
            '{} Login\'s insert : username=\'{}\' password=\'{}\''.format(self.name, self.username, self.password))
        # self.username_element = self.driver.find_element(By.ID, 'inputEmail')
        # self.username_element.send_keys(self.username)
        # self.password_element = self.driver.find_element(By.ID, 'inputPassword')
        # self.password_element.send_keys(self.password)

    def run(self, present_element_id, test_mode=False):
        i = 0
        while True:
            i += 1

            if test_mode:
                if i == 1:
                    Log.info('{} Test web : {} times'.format(self.name, self.random_number))
                if i == self.random_number:
                    self.driver.get('https://www.lotto.ktbnetbank.com/KTBLotto/#/login')

            try:
                self.present_element = EC.presence_of_element_located((By.ID, present_element_id))
                WebDriverWait(self.driver, Web.TIMEOUT).until(self.present_element)
                url = self.driver.current_url

                # login
                # KTBLotto
                if 'login' in url:
                    pass
                    Log.info('{} Login\'s state : {}, {}'.format(self.name, self.handle, url))
                    self.login()
                    break
                else:
                    Log.info('{} Refresh\'s state : {}, {}'.format(self.name, self.handle, url))
                    time.sleep(1)
                    self.driver.refresh()
            except Exception as e:
                Log.error('{} Exception\'s state : {}'.format(self.name, type(e).__name__))
                self.driver.refresh()


if __name__ == '__main__':
    web = Web('https://www3.lotto.ktbnetbank.com')
    web.run('headTitleWeb', True)
