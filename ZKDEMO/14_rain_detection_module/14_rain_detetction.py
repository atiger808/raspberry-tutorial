# coding=utf-8
'''
LM393模块 配合PCF8591模块 做 雨水检测
接口分别为：A0, D0, VCC, GND
A0 对应  PCF8591模块的AIN0
D0 对应  GPIO接口
VCC 接 5v
GND 接 地线
'''

import PCF8591 as ADC
import RPi.GPIO as GPIO
import time
import math

DO = 5

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    ADC.setup(0x48)
    GPIO.setup(DO, GPIO.IN)

def Print(x):
    if x == 1:
        print('')
        print('####################')
        print('#    Not raining   #')
        print('####################')
        print('')
    if x == 0:
        print('')
        print('####################')
        print('#      Raining     #')
        print('')

def loop():
    status = 1
    while True:
        print(ADC.read(0))
        tmp = GPIO.input(DO)
        if tmp != status:
            Print(tmp)
            status = tmp
        time.sleep(0.2)

if __name__ == '__main__':
    try:
        setup()
        loop()
    except KeyboardInterrupt:
        pass
