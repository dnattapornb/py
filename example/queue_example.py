import logging
from multiprocessing import Queue

logging.basicConfig(format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s', level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')

colors = ['red', 'green', 'blue', 'black']
cnt = 1
# instantiating a queue object
queue = Queue()
# print('pushing items to queue:')
logging.info('pushing items to queue:')
for color in colors:
    # print('item no: ', cnt, ' ', color)
    logging.info('item no: %d %s' % (cnt, color))
    queue.put(color)
    cnt += 1

# print('\npopping items from queue:')
logging.info('popping items from queue:')
cnt = 0
while not queue.empty():
    # print('item no: ', cnt, ' ', queue.get())
    logging.info('item no: %d %s' % (cnt, queue.get()))
    cnt += 1
