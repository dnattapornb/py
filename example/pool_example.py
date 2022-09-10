import time
import logging
from multiprocessing import Pool

logging.basicConfig(format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s', level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')

work = (["A", 5], ["B", 2], ["C", 1], ["D", 3], ["E", 10], ["F", 10])


def work_log(work_data):
    # print("Process %s waiting %s seconds" % (work_data[0], work_data[1]))
    # time.sleep(int(work_data[1]))
    # print("Process %s Finished." % work_data[0])
    logging.info('Process %s waiting %s seconds' % (work_data[0], work_data[1]))
    time.sleep(int(work_data[1]))
    logging.info('Process %s Finished.' % work_data[0])


def pool_handler():
    p = Pool(10)
    p.map(work_log, work)


if __name__ == '__main__':
    # pool_handler()
    main()
