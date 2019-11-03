import RPi.GPIO as GPIO
import time

PIpin = 6
Rpin = 12
Gpin = 13

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(Rpin, GPIO.OUT)
    GPIO.setup(Gpin, GPIO.OUT)
    
    # set default  Rpin=1, Gpin=0, led is not blocked
    GPIO.output(Rpin, GPIO.HIGH)
    GPIO.output(Gpin, GPIO.LOW)


    # set BtnPin's mode is input, and pull up to hight level (3.3v)
    GPIO.setup(PIpin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(PIpin, GPIO.BOTH, callback=detect, bouncetime=200)

def led(x):
    # led is not blocked
    if x == 0:
        GPIO.output(Rpin, 1)
        GPIO.output(Gpin, 0)
    # led is blocked on
    if x == 1:
        GPIO.output(Rpin, 0)
        GPIO.output(Gpin, 1)

def Print(x):
    if x == 1:
        print('\n')
        print('    #####################')
        print('    # Light was blocked #')
        print('    #####################')


def detect(chn):
    led(GPIO.input(PIpin))
    Print(GPIO.input(PIpin))

def loop():
    while True:
        pass

def destroy():
    GPIO.output(Rpin, GPIO.HIGH)
    GPIO.output(Gpin, GPIO.HIGH)
    GPIO.cleanup()

if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()



