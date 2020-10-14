# _*_ coding: utf-8 _*_
# @Time     : 2019/9/26 4:57
# @Author   : Ole211
# @Site     : 
# @File     : count_down.py    
# @Software : PyCharm
import time
from datetime import datetime
import sys

now = time.time()
future = now + 100
print(type(now))
print(time.localtime())
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

while 1:
    if now > future:
        break

    sys.stdout.write('%.2f' % (future - now) + '\r')
    sys.stdout.flush()
    now = time.time()
