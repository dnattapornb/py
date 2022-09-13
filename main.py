import time
import Log
import queue  # imported for using queue.Empty exception
from multiprocessing import Pool, Lock, Process, Queue, current_process, cpu_count
from Web import Web

# url = 'http://127.0.0.1/channel-manager/admin'
# url = 'https://www3.lotto.ktbnetbank.com/#/login'
url = 'https://www3.lotto.ktbnetbank.com'

# element_id = 'loginForm'
element_id = 'headTitleWeb'

# worker
work = []
for i in range(2):
    tmp = ['WEB-%02d' % (i + 1), i * 300]
    work.append(tmp)
work_done = []

# task
task_done = []

'''
# --------------- [ start : worker + pool ] ---------------
def work_factory(work_data):
    logging.info('Process %s' % (work_data[0]))
    web = Web(url, work_data[1], work_data[0])
    web.run(element_id)
    work_done.append(web)
    logging.info('Process %s Finished.' % (work_data[0]))
    # time.sleep(300)


def pool_handler():
    p = Pool(10)
    p.map(work_factory, work)
'''


# --------------- [ start : multiprocessing ] ---------------
def do_job(tasks_to_accomplish, tasks_that_are_done):
    while True:
        try:
            task = tasks_to_accomplish.get_nowait()
        except queue.Empty:
            break
        else:
            Log.info('Task : %s' % (task[0]))
            web = Web(url, task[1], task[0])
            web.run(element_id)
            task_done.append(web)
            Log.info('Task : %s is don by %s.' % (task[0], current_process().name))
            tasks_that_are_done.put(task[0] + ' is done by ' + current_process().name)
            time.sleep(.5)
    return True


def task_handler():
    number_of_task = 2
    number_of_processes = 10
    tasks_to_accomplish = Queue()
    tasks_that_are_done = Queue()
    processes = []

    for x in range(number_of_task):
        tasks_to_accomplish.put(['WEB-%02d' % (x + 1), x * 300])

    # creating processes
    for w in range(number_of_processes):
        p = Process(target=do_job, args=(tasks_to_accomplish, tasks_that_are_done))
        processes.append(p)
        p.start()

    # completing process
    for p in processes:
        p.join()

    # print the output
    while not tasks_that_are_done.empty():
        print(tasks_that_are_done.get())

    return True


if __name__ == '__main__':
    task_handler()
    # pool_handler()
    # create_gui()
