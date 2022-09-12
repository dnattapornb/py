import time
from multiprocessing import Pool

worker = 2
work = (["A", 5], ["B", 2], ["C", 1], ["D", 3], ["E", 10], ["F", 10])


def work_process(work_data):
    print('Worker get work %s to processing waiting %s seconds' % (work_data[0], work_data[1]))
    time.sleep(int(work_data[1]))
    print('Worker get work %s is finished.' % work_data[0])


def pool_handler():
    p = Pool(worker)
    p.map(work_process, work)


if __name__ == '__main__':
    pool_handler()
