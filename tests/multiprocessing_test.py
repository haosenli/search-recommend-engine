import multiprocessing
from multiprocessing import Pool
from time import sleep

def work(x):
    sleep(2)
    print(x)
    return x

def tasks():
    for i in range(10):
        yield i
    
if __name__ == '__main__':
    # freeze_support()
    with Pool(processes=8) as pool:
        results = pool.imap(work, tasks())
        for result in results:
            print(result)