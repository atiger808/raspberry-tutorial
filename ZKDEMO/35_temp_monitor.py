#coding=utf-8
import RPi.GPIO as GPIO
import importlib
import time
import sys

LedR = 22
LedG = 23
LedB = 24
Buzzer_active = 17
Buzzer_passive = 5
TRIG = 25
ECHO = 26

# 有源蜂鸣
beep_active = importlib.import_module('10_active_buzzer')
# 无源蜂鸣
beep_passive = importlib.import_module('10_passive_buzzer')
# rgb LED 灯
rgb = importlib.import_module('02_rgb_led')
# 超声雷达测距
dst = importlib.import_module('25_ultrasonic_ranging')

beep_active.setup(Buzzer_active)
beep_passive.setup(Buzzer_passive)
rgb.setup(LedR, LedG, LedB)
dst.setup(TRIG, ECHO)


color = {'Red':0x00FFFF, 'Green':0xFF00FF, 'Blue':0xFF0000}

def loop():
    while True:
        dist = dst.distance()
        print('Distance: %.3f m' %(dist))
        if dist < 0.45:
            rgb.setColor(color['Red'])
            for i in range(0, 2):
                beep_active.beep(0.25)
        else:
            rgb.setColor(color['Blue'])
        time.sleep(0.1)

def destroy():
    # beep_passive.destroy()
    beep_active.destroy()
    rgb.destroy()
    dst.destroy()
    GPIO.cleanup()

if __name__ == '__main__':
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
