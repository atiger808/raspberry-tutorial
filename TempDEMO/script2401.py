'''
闪烁LED灯
'''
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.output(18, GPIO.LOW)
blinks = 0
print('Start of blinking')
while(blinks <10):
    GPIO.output(18, GPIO.HIGH)
    time.sleep(1.0)
    GPIO.output(18, GPIO.LOW)
    time.sleep(1.0)
    blinks = blinks+1
GPIO.output(18, GPIO.LOW)
GPIO.cleanup()
print('End of blinking')
