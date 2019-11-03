# _*_ coding: utf-8 _*_
# @Time     : 2019/10/15 2:56
# @Author   : Ole211
# @Site     : 
# @File     : sync.py    
# @Software : PyCharm

''' 程序实现异步的方法'''

from threading import Thread
from time import sleep

def asyn(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper

@asyn
def task():
    global dist
    print('执行任务')
    for i in range(5):
        dist = i
        sleep(0.2)


def A():
    global dist
    print('----开始----')
    task()
    print(dist)
    print("函数A睡了十秒钟。。。。。。")
    print("-----结束----")

def B():
    n  = 0
    while n<10:
        A()
        n = n+1
        sleep(1)
B()



'''异步函数实现'''
# import time
# import asyncio
#
# # 定义异步函数
# async def hello():
#     # asyncio.sleep(1)
#     print('Hello World:%s' % time.time())
#
# def run():
#     for i in range(5):
#         loop.run_until_complete(hello())
#
# loop = asyncio.get_event_loop()
# if __name__ =='__main__':
#     run()