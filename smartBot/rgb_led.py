# _*_ coding: utf-8 _*_
# @Time     : 2019/10/16 6:54
# @Author   : Ole211
# @Site     : 
# @File     : rgb_led.py    
# @Software : PyCharm

import RPi.GPIO as GPIO
import time

R = 22
G = 23
B = 24


def setup(R, G, B):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(R, GPIO.OUT)
    GPIO.setup(G, GPIO.OUT)
    GPIO.setup(B, GPIO.OUT)


def rgb(red=False, green=False, blue=False, delay=0.1):
    GPIO.output(R, red)
    GPIO.output(G, green)
    GPIO.output(B, blue)
    time.sleep(delay)


def bright():
    rgb(red=True)
    rgb(green=True)
    rgb(blue=True)

def destroy():
    GPIO.cleanup()


if __name__ == '__main__':
    try:
        setup(R, G, B)
        while True:
            bright()
    except KeyboardInterrupt:
        pass
    finally:
        destroy()
