import RPi.GPIO as GPIO
import time

RelayPin = 17

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(RelayPin, GPIO.OUT)
    GPIO.output(RelayPin, GPIO.HIGH)

def loop():
    while True:
        print('Relay on ...')
        GPIO.output(RelayPin, GPIO.LOW)
        time.sleep(0.5)
        print('Relay off...')
        GPIO.output(RelayPin, GPIO.HIGH)
        time.sleep(0.5)

def destroy():
    GPIO.output(RelayPin, GPIO.HIGH)
    GPIO.cleanup()

if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
