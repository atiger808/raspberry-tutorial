import RPi.GPIO as GPIO
import time, sys

# BCM
IN1 = 16 
IN2 = 13
IN3 = 12
IN4 = 6


TRIG = 25#   超声波发射
ECHO = 26#   超声波接受

R_pin = 22
G_pin = 23
B_pin = 24

def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(IN1, GPIO.OUT)
    GPIO.setup(IN2, GPIO.OUT)
    GPIO.setup(IN3, GPIO.OUT)
    GPIO.setup(IN4, GPIO.OUT)

    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

    GPIO.setup(R_pin, GPIO.OUT)
    GPIO.setup(G_pin, GPIO.OUT)
    GPIO.setup(B_pin, GPIO.OUT)

######## 方向操控 #######
def back():
    print('moror forward...')
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

def forward():
    print('motor back...')
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)

def stop():
    print('motor stop...')
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)

def turn_left():
    print('motor left...')
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

def turn_right():
    print('motor right')
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)

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

def rgb(red=False, green=False, blue=False, delay=0.1):
    GPIO.output(R_pin, red)
    GPIO.output(G_pin, green)
    GPIO.output(B_pin, blue)
    time.sleep(delay)

def bright():
    rgb(red=True)
    rgb(green=True)
    rgb(blue=True)


def main(status, x):
    if status == 'front':
        forward()
        time.sleep(x)
    elif status == 'back':
        back()
        time.sleep(x)
    elif status == 'left':
        turn_left()
        time.sleep(x)
    elif status == 'right':
        turn_right()
        time.sleep(x)
    elif status == 'stop':
        stop()

def destroy():
    GPIO.cleanup()

if __name__ == '__main__':
    time.sleep(4)
    init()
    forward()
    try:
        while True:
            dist = distance()
            print('距离：%0.3f m' % dist)
            if dist < 0.5:
                rgb(red=True)
                back()
                time.sleep(1)
                turn_left()
                time.sleep(1)
            else:
                rgb(green=True)
                forward()
            time.sleep(0.3)
    except KeyboardInterrupt:
        print('Ctrl Pressed')
        stop()
        destroy()
    finally:
        stop()
        destroy()
