import time
import logging
import queue  # imported for using queue.Empty exception
from multiprocessing import Pool, Lock, Process, Queue, current_process, cpu_count
from tkinter import *
from Web import Web

logging.basicConfig(format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s', level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')

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


# --------------- [ end : worker + pool ] ---------------
'''


# --------------- [ start : multiprocessing ] ---------------
def do_job(tasks_to_accomplish, tasks_that_are_done):
    while True:
        try:
            task = tasks_to_accomplish.get_nowait()
        except queue.Empty:
            break
        else:
            logging.info('Task : %s' % (task[0]))
            web = Web(url, task[1], task[0])
            web.run(element_id)
            task_done.append(web)
            logging.info('Task : %s is don by %s.' % (task[0], current_process().name))
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


# --------------- [ start : multiprocessing ] ---------------


def create_gui():
    app = Tk()

    # 1440 x 900
    # 2560 x 1080
    sw = app.winfo_screenwidth()
    sh = app.winfo_screenheight()

    app.title('My GUI')
    app.geometry('500x400+0+0')
    Button(app, text='Start', command=task_handler).pack()
    app.mainloop()
    print('{} x {}'.format(sw, sh))


if __name__ == '__main__':
    task_handler()
    # pool_handler()
    # create_gui()
