# coding=utf-8
'''
HC-SR04 超声波测距模块
1. 采用IO 口TRIG 触发测距，
   给最少10us 高电平信号
   即发射高电平时间最小: 0.00001s。
2  测试距离=(高电平时间*声速(340M/S))/2
3. 工作电压DC 5V 工作电流15mA 
   工作频率40kHz 最远射程4m 
   最近射程2cm 测量角度15度
4. 被测物体的面积不少于0.5平方米
   且平面尽量要求平整，否则影响测量的结果
   建议测量周期为60ms以上
   即周期最小: 0.06s

'''

import RPi.GPIO as GPIO
import time

TRIG = 19
ECHO = 20

def setup(TRIG_pin, ECHO_pin):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG_pin, GPIO.OUT)
    GPIO.setup(ECHO_pin, GPIO.IN)

def distance():
    GPIO.output(TRIG, 0)
    time.sleep(0.000002)

    GPIO.output(TRIG, 1)
    time.sleep(0.000015)
    GPIO.output(TRIG, 0)

    while GPIO.input(ECHO) == 0:
        pass
    t1 = time.time()
    while GPIO.input(ECHO) == 1:
        pass
    t2 = time.time()

    during = t2 -t1
    return during * 340 /2

def distance2():
    GPIO.output(TRIG, 1)
    x = 1
    x = 1
    x = 1
    GPIO.output(TRIG, 0)
    while GPIO.input(ECHO) == 0:
        continue
    t0 = time.time()
    while GPIO.input(ECHO) == 1:
        continue
    t1 = time.time()
    during = t1 - t0
    return during*340/2
    

def loop():
    while True:
        dist = distance()
        print('dist: %.3f m' % dist)
        time.sleep(0.1)

def destroy():
    GPIO.cleanup()

if __name__ == '__main__':
    setup(TRIG, ECHO)
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
