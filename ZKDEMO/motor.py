# coding=utf-8
import RPi.GPIO as GPIO
import sys
import time

STERRING_PIN = 17
top_pin = 4
bottom_pin = 17
# timeout=float(sys.argv[1])
import cv2

cap = cv2.VideoWriter(0)
_, frame = cap.read()
cv2.imwrite('shot,jpg', frame)
def setup_top():
    GPIO.setmode(GPIO.BCM)
    global pwm_top
    GPIO.setup(top_pin, GPIO.OUT, initial=False)
    pwm_top = GPIO.PWM(top_pin, 50)
    pwm_top.start(10./180*90+2)
    pwm_top.ChangeDutyCycle(0)

def setup_bottom():
    GPIO.setmode(GPIO.BCM)
    global pwm_bottom
    GPIO.setup(bottom_pin, GPIO.OUT, initial=False)
    pwm_bottom = GPIO.PWM(bottom_pin, 50)
    pwm_bottom.start(10./180*90 +2)
    pwm_bottom.ChangeDutyCycle(0)

def setDirection(channel, direction):
    duty = 10./180.*direction + 2
    print(duty)
    if channel == 'bottom':
        setup_bottom()
        pwm_bottom.ChangeDutyCycle(duty)
        time.sleep(0.2)
        pwm_bottom.ChangeDutyCycle(0)
        pwm_bottom.stop()
        GPIO.cleanup()
    elif channel == 'top':
        setup_top()
        pwm_top.ChangeDutyCycle(duty)
        time.sleep(0.4)
        pwm_top.ChangeDutyCycle(0)
        pwm_top.stop()
        GPIO.cleanup()

if __name__ == '__main__':
    print('starting')
    setDirection(sys.argv[1], int(sys.argv[2]))
    print('Done')



'''
GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)
GPIO.setup(pin, GPIO.OUT, initial=False)
pwm = GPIO.PWM(pin, 50)
pwm.start(0)
time.sleep(2)


def loop():
    while True:
        print('....正转')
        for i in range(0, 181, 10):
            pwm.ChangeDutyCycle(2.5 + 1./18.*i)
            time.sleep(0.02)
            pwm.ChangeDutyCycle(0)
            time.sleep(0.2)
        print('....反转')
        for i in range(181, 0, -10):
            pwm.ChangeDutyCycle(2.5 + 1./18.*i)
            time.sleep(0.02)
            pwm.ChangeDutyCycle(0)
            time.sleep(0.2)
def destroy():
    pwm.ChangeDutyCycle(0)
    pwm.stop()
    GPIO.output(pin, False)
    GPIO.cleanup()

if __name__ == '__main__':
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
    GPIO.cleanup()
'''
