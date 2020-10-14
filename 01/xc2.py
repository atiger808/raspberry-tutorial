# coding=utf-8
import RPi.GPIO as GPIO
import time
import sys

IN1 = 16
IN2 = 13
IN3 = 12
IN4 = 6

ECHO = 25
TRIG = 26


def init():
    global ENA_pwm, ENB_pwm
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # 使能ENA, ENB 初始化
    GPIO.setup(ENA, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(ENB, GPIO.OUT, initial=GPIO.LOW)

    # GPIO接口初始化
    GPIO.setup(IN1, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(IN2, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(IN3, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(IN4, GPIO.OUT, initial=GPIO.LOW)

    ENA_pwm = GPIO.PWM(ENA, 100)
    ENB_pwm = GPIO.PWM(ENB, 100)
    ENA_pwm.start(0)
    ENB_pwm.start(0)
    # 脉冲占空比
    ENA_pwm.ChangeDutyCycle(100)
    ENB_pwm.ChangeDutyCycle(100)

    # 超声波初始化
    GPIO.setup(TRIG, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(ECHO, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def distance():
    GPIO.output(TRIG, 0)
    time.sleep(0.000002)

    GPIO.output(TRIG, 1)
    time.sleep(0.00001)
    GPIO.output(TRIG, 0)

    while GPIO.input(ECHO) == 0:
        pass
    t1 = time.time()
    while GPIO.input(ECHO) == 1:
        pass
    t2 = time.time()

    during = t2 - t1
    return during * 340 / 2


def checkdist():
    GPIO.output(TRIG, GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(TRIG, GPIO.LOW)
    while not GPIO.input(ECHO):
        pass
    t1 = time.time()
    while GPIO.input(ECHO):
        pass
    t2 = time.time()
    return (t2 - t1) * 340 / 2


def forward():
    print('forward...')
    GPIO.output(ENA, True)
    GPIO.output(ENB, True)

    GPIO.output(IN1, False)
    GPIO.output(IN2, True)
    GPIO.output(IN3, True)
    GPIO.output(IN4, False)


def backward():
    print('backward...')
    GPIO.output(ENA, True)
    GPIO.output(ENB, True)

    GPIO.output(IN1, True)
    GPIO.output(IN2, False)
    GPIO.output(IN3, False)
    GPIO.output(IN4, True)


def turn_left():
    print('turn_left...')
    GPIO.output(ENA, False)
    GPIO.output(ENB, True)

    GPIO.output(IN1, False)
    GPIO.output(IN2, False)
    GPIO.output(IN3, True)
    GPIO.output(IN4, False)


def turn_right():
    print('turn_right...')
    GPIO.output(ENA, True)
    GPIO.output(ENB, False)

    GPIO.output(IN1, False)
    GPIO.output(IN2, True)
    GPIO.output(IN3, False)
    GPIO.output(IN4, False)


def stop():
    print('stop...')
    GPIO.output(ENA, False)
    GPIO.output(ENB, False)

    GPIO.output(IN1, False)
    GPIO.output(IN2, False)
    GPIO.output(IN3, False)
    GPIO.output(IN4, False)

def destroy():
    ENA_pwm.stop()
    ENB_pwm.stop()
    GPIO.cleanup()

def main(status):
    if status == 'front':
        forward()
        time.sleep(10)
    elif status == 'back':
        back()
        time.sleep(10)
    elif status == 'left':
        turn_left()
        time.sleep(10)
    elif status == 'right':
        turn_right()
        time.sleep(10)
    elif status == 'stop':
        stop()

if __name__ == '__main__':
    time.sleep(2)
    init()
    try:
        while True:
            dst = distance()
            print('distance: %.3f m' % dst)
            main(sys.argv[1])
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()
