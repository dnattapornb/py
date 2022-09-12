import platform


def get_platform():
    name = 'unknown'
    __Platform = platform.platform()
    if 'mac' in __Platform.lower():
        name = 'mac'
    elif 'darwin' in __Platform.lower():
        name = 'mac'
    elif 'win' in __Platform.lower():
        name = 'win'

    return name


def get_web_driver():
    web_driver = 'chromedriver'
    if platform == 'mac':
        web_driver = 'chromedriver'
    elif platform == 'win':
        web_driver = 'chromedriver.exe'

    return web_driver


if __name__ == '__main__':
    print(get_platform())
