# _*_ coding: utf-8 _*_
# @Time     : 2019/10/13 2:01
# @Author   : Ole211
# @Site     : 
# @File     : angleServoCtrl.py    
# @Software : PyCharm

from time import sleep
import RPi.GPIO as GPIO
import sys

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


def setServoAngle(servo, angle):
    # assert angle >=30 and angle <= 150
    GPIO.output(servo, True)
    pwm = GPIO.PWM(servo, 50)
    pwm.start(0)
    dutyCycle = angle / 18. + 3.
    pwm.ChangeDutyCycle(dutyCycle)
    sleep(0.3)
    pwm.stop()
    sleep(3)


if __name__ == '__main__':
    servo = int(sys.argv[1])
    GPIO.setup(servo, GPIO.OUT, initial=False)
    print('...on')
    setServoAngle(servo, int(sys.argv[2]))
    print('...off')
    GPIO.output(servo, False)
    GPIO.cleanup()
