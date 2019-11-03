#####################################################
#
#	DO NOT WATCH THE LASER DERECTELY IN THE EYE!
#
#####################################################
import RPi.GPIO as GPIO
import time

LedPin = 19

def setup(LedPin):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LedPin, GPIO.OUT)
    GPIO.output(LedPin, GPIO.HIGH)

def loop():
    while True:
        print('...Laser on')
        GPIO.output(LedPin, GPIO.LOW)
        time.sleep(0.5)
        GPIO.output(LedPin, GPIO.HIGH)
        time.sleep(0.5)

def destroy():
    GPIO.output(LedPin, GPIO.HIGH)
    GPIO.cleanup()

if __name__ == '__main__':
    setup(LedPin)
    try:
        loop()
    except KeyboardInterrupt:
        destroy()

