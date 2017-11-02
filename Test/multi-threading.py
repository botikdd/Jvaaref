from threading import Thread, current_thread
from multiprocessing import Process
import time

def f(n):
    i = n
    while i > 0:
        print(i)
        time.sleep(i)
        i = i - 1

if __name__ == '__main__':
    t1 = Thread(target=f, args=(20,))
    t2 = Thread(target=f, args=(5,))
    t1.start()
    t2.start()

    t2.join()
    t1.join()