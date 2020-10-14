import RPi.GPIO as GPIO
import time

# BCM     BOARD
IN1 = 19 # 11
IN2 = 16 # 12
IN3 = 21 # 16
IN4 = 26 # 18
ENA = 13
ENB = 20

TRIG = 12 # 4  超声波发射
ECHO = 4  # 7  超声波接受


GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)

pwma = GPIO.PWM(ENA, 100)
pwmb = GPIO.PWM(ENB, 100)
pwma.start(0)
pwmb.start(0)
GPIO.output(IN1, GPIO.HIGH)
GPIO.output(IN2, GPIO.LOW)
GPIO.output(IN3, GPIO.LOW)
GPIO.output(IN4, GPIO.LOW)

try:
    while 1:
        pwma.ChangeDutyCycle(90)
        pwmb.ChangeDutyCycle(90)
        time.sleep(5)
        pwma.ChangeDutyCycle(10)
        pwmb.ChangeDutyCycle(10)
        time.sleep(3)
except KeyboardInterrupt:
    GPIO.cleanup()


