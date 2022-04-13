# Code to execute in an independent thread
import time


def countdown(n, pool_sema):
    pool_sema.acquire()
    # 加锁，limited threads
    while n > 0:
        print('T-minus', n)
        n -= 1
        time.sleep(3)
    pool_sema.release()
    #解锁，


if __name__ == '__main__':
    from threading import Thread, BoundedSemaphore

    max_connections = 20
    pool_sema = BoundedSemaphore(max_connections)
    start = time.time()
    t = Thread(target=countdown, args=(10,pool_sema))
    t.start()
    end = time.time()
    print('spend time is {0}'.format(end - start))
