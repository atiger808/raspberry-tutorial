# coding=utf-8
'''
有源蜂鸣器
1. 采用S8550三极管驱动
2. 工作电压3.3v-5v
3. VCC外接3.3v-5v电压
   GND外接GND
   I/O外接IO
4. 低电平触发
'''

import RPi.GPIO as GPIO
import time

BuzzerPin = 17

def setup(BuzzerPin):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BuzzerPin, GPIO.OUT)
    GPIO.output(BuzzerPin, GPIO.HIGH)

def on():
    GPIO.output(BuzzerPin, GPIO.LOW)

def off():
    GPIO.output(BuzzerPin, GPIO.HIGH)

def beep(x):
    on()
    time.sleep(x)
    off()
    time.sleep(x)

def loop():
    while True:
        beep(0.5)

def destroy():
    GPIO.output(BuzzerPin, GPIO.HIGH)
    GPIO.cleanup()

if __name__ == '__main__':
    setup(BuzzerPin)
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
