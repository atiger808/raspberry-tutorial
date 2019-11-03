# _*_ coding: utf-8 _*_
# @Time     : 2019/10/7 19:36
# @Author   : Ole211
# @Site     : 
# @File     : 34_tracking.py    
# @Software : PyCharm

import RPi.GPIO as GPIO
import importlib
import time

Left_TrackPin = 18
Right_TrackPin = 27

def setup(Left_TrackPin, Right_TrackPin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(Left_TrackPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(Right_TrackPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

def loop():
    GPIO.setmode(GPIO.BCM)
    while True:
        if GPIO.input(Left_TrackPin) == GPIO.LOW and GPIO.input(Right_TrackPin) == GPIO.LOW:
            print('Both side line is White----Forward')
        elif GPIO.input(Left_TrackPin) == GPIO.LOW and GPIO.input(Right_TrackPin) == GPIO.HIGH:
            print('Left line is White and Right is Black----Turn Right')
        elif GPIO.input(Left_TrackPin) == GPIO.HIGH and GPIO.input(Right_TrackPin) == GPIO.LOW:
            print('Left line is Black and Right is White----Turn Left')
        else:
            print('Both side line is Black----Forward----Stop')
        time.sleep(0.02)
def destroy():
    GPIO.cleanup()

if __name__ == '__main__':
    try:
        setup(Left_TrackPin, Right_TrackPin)
        loop()
    except KeyboardInterrupt:
        destroy()


