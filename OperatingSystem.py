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


if __name__ == '__main__':
    print(get_platform())
