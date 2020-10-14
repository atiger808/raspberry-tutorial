# _*_ coding: utf-8 _*_
# @Time     : 2019/10/13 2:30
# @Author   : Ole211
# @Site     : 
# @File     : motor2.py    
# @Software : PyCharm

import RPi.GPIO as GPIO
import time

pin = 25

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pin, GPIO.OUT)
pwm = GPIO.PWM(pin, 50)
pwm.start(0)


angle = 0
while angle < 180:
    duty = 2.5 + 15.*angle/180.
    pwm.ChangeDutyCycle(duty)
    print(duty)
    time.sleep(0.04)
    angle = angle + 15

pwm.ChangeDutyCycle(2.5)
time.sleep(1)
GPIO.cleanup()