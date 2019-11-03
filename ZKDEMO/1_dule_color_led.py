import RPi.GPIO as GPIO
import time

R_pin = 22
G_pin = 23


def setup(R_pin, G_pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(R_pin, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(G_pin, GPIO.OUT, initial=GPIO.HIGH)


def flight_red():
    n = 10
    while n>0:
        GPIO.output(R_pin, GPIO.LOW)
        GPIO.output(G_pin, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(R_pin, GPIO.HIGH)
        GPIO.output(G_pin, GPIO.HIGH)
        time.sleep(0.1)
        n = n-1
    GPIO.cleanup()

def destroy():
    GPIO.output(R_pin, GPIO.HIGH)
    GPIO.output(G_pin, GPIO.HIGH)
    GPIO.cleanup()

if __name__ == '__main__':
    try:
        setup(R_pin, G_pin)
        flight_red()
    except KeyboardInterrupt:
        destroy()

