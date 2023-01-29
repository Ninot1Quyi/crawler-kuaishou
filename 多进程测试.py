import time
from multiprocessing.pool import Pool

def numsCheng(i):
    return i * 2

if __name__ == '__main__':
    time1 = time.time()
    nums_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    pool = Pool(processes=5)
    result = pool.map(numsCheng, nums_list)
    pool.close()        # 关闭进程池，不再接受新的进程
    pool.join()         # 主进程阻塞等待子进程的退出

    print(result)
    time2 = time.time()
    print("计算用时：", time2-time1)
