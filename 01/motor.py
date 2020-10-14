# coding=utf-8
import RPi.GPIO as GPIO
import sys
import time

STERRING_PIN = 19
pin = 19

# if __name__ == '__main__':
#     GPIO.setmode(GPIO.BCM)
#     GPIO.setwarnings(False)
#     GPIO.setup(pin, GPIO.OUT)
#     pwm = GPIO.PWM(pin, 100)
#     pwm.start(0)
#
#     for i in range(-10, 170, 1):
#         try:
#             duty = (1./18.)*int(i) + 2.5
#             pwm.ChangeDutyCycle(duty)
#             print(duty)
#             time.sleep(0.5)
#         except:
#             pass



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

