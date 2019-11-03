# _*_ coding: utf-8 _*_
# @Time     : 2019/10/7 8:21
# @Author   : Ole211
# @Site     : 
# @File     : 29_ir_obstable.py    
# @Software : PyCharm

import RPi.GPIO as GPIO
ObstaclePin = 23

def setup(ObstaclePin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ObstaclePin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def loop():
    while True:
        if (0==GPIO.input(ObstaclePin)):
            print('Detected Barrier!')

def destroy():
    GPIO.cleanup()

if __name__ == '__main__':
    setup(ObstaclePin)
    try:
        loop()
    except KeyboardInterrupt:
        destroy()

        