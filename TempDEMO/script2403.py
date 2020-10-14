'''
24.4检测GPIO输入
轮询
配置检测输入的硬件
在这个项目中， 我们将模拟一个房间和两个门铃：一个是前门
一个是后门。当有人按其中一个门铃时， 项目将告诉你是哪一个门铃响，
然后会根据这些信息做一些很酷的事情
这段代码配置的GPIO18作为输出。然后使用GPIO24和GPIO25作为输入（分别代表前后门门铃）
然后进入一个循环， 在每次迭代中轮询GPIO24和GPIO25引脚状态。如果GPIO24引脚是滴电平， 代码会打印一条信息说后门铃响了并且点亮LED。如果GPIO25引脚是低电平， 则代码会打印一条信息说前门铃响了并且点亮LED。

'''

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT) # GPIO 18 用来输出
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP) # GPIO 24 用来输入 代表前门门铃
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP) # GPIO 25 用来输入 代表后门门铃
GPIO.output(18, GPIO.LOW)

try:
    while True:
        if (GPIO.input(24) == GPIO.LOW):
            print('Back door')
            GPIO.output(18, GPIO.HIGH)
        elif (GPIO.input(25) == GPIO.LOW):
            print('Front door')
            GPIO>output(18, GPIO>HIGH)
        else:
            GPIO.output(18, GPIO.LOW)
        time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()
print('End of Test')

