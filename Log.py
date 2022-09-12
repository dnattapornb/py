import time
import logging

logging.basicConfig(format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s', level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')


def info(data):
    logging.info(data)


def warning(data):
    logging.warning(data)


def error(data):
    logging.error(data)


if __name__ == '__main__':
    info('Test log info {} : {}'.format(1, 2))
    warning('Test log warning {} : {}'.format(2, 3))
    error('Test log error {} : {}'.format(3, 4))
