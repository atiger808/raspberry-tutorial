# coding=utf-8
import RPi.GPIO as GPIO
import time
import sys

# BCM     BOARD
IN1 = 16
IN2 = 13
IN3 = 12
IN4 = 6

ECHO = 25
TRIG = 26

def init():
    global pwma, pwmb
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(IN1, GPIO.OUT)
    GPIO.setup(IN2, GPIO.OUT)
    GPIO.setup(IN3, GPIO.OUT)
    GPIO.setup(IN4, GPIO.OUT)

    GPIO.setup(ENA, GPIO.OUT)
    GPIO.setup(ENB, GPIO.OUT)
    
    pwma = GPIO.PWM(ENA, 80)
    pwmb = GPIO.PWM(ENB, 80)
    pwma.start(90)
    pwmb.start(90)

    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)


######## 方向操控 #######
def forward():
    print('moror forward...')
    # pwma.ChangeFrequency(800)
    # pwmb.ChangeFrequency(800)
    GPIO.output(ENA, GPIO.HIGH)
    GPIO.output(ENB, GPIO.HIGH)
    pwma.ChangeDutyCycle(100)
    pwmb.ChangeDutyCycle(100)

    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

def back():
    print('motor back...')
    GPIO.output(ENA, GPIO.HIGH)
    GPIO.output(ENB, GPIO.HIGH)

    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)

def stop():
    print('motor stop...')
    GPIO.output(ENA, GPIO.LOW)
    GPIO.output(ENB, GPIO.LOW)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)

def turn_left():
    print('motor left...')
    GPIO.output(ENB, GPIO.HIGH)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

def turn_right():
    print('motor right')
    GPIO.output(ENA, GPIO.HIGH)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)

####### 超声波距离检测 ########
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

    during = t2 -t1
    return during * 340 /2

def checkdist():
    GPIO.output(TRIG, 0)
    time.sleep(0.000002)

    GPIO.output(TRIG, 1)
    time.sleep(0.00001)
    GPIO.output(TRIG, 0)

    while GPIO.input(ECHO) == 0:
        a = 0
    t1 = time.time()
    while GPIO.input(ECHO) == 1:
        a = 1
    t2 = time.time()
    dist = (t2-t1)*340/2
    return dist

def loop():
    forward()
    time.sleep(5)
    stop()
    time.sleep(3)
    turn_left()
    time.sleep(5)
    stop()
    time.sleep(3)
    turn_right()
    time.sleep(5)
    stop()
    time.sleep(3)
    back()
    time.sleep(5)
    destroy()

def destroy():
    pwma.stop()
    pwmb.stop()
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
    init()
    main(sys.argv[1])
    destroy()
    '''
    try:
        while True:
            dist = distance()
            print('距离：%0.3f m' % dist)
            if dist > 0.35:
                forward()
            else:
                turn_left()
            time.sleep(0.3)
    except KeyboardInterrupt:
        destroy()
    '''
