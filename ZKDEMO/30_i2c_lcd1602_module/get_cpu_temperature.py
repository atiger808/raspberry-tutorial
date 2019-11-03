# _*_ coding: utf-8 _*_
# @Time     : 2019/10/8 3:07
# @Author   : Ole211
# @Site     : 
# @File     : get_cpu_temperature.py    
# @Software : PyCharm

import psutil
import os
def get_cpu_temperature():
    cpu_temp = psutil.sensors_temperatures().values()[0][0][1]
    return '%.2f'%cpu_temp

def get_cpu_temperature2():
    res = os.popen('vcgencmd measure_temp').readline()
    return res.replace("temp=", "").replace("'C\n", "")


if __name__ == '__main__':
    print(get_cpu_temperature())
