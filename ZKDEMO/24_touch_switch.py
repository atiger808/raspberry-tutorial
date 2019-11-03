import RPi.GPIO as GPIO

TouchPin = 18
Rpin = 12
Gpin = 13
tmp = 0

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(Rpin, GPIO.OUT)
    GPIO.setup(Gpin, GPIO.OUT)
    # Set btn's mode is input , and pull up to high level(3.3v)
    GPIO.setup(TouchPin, GPIO.IN,pull_up_down=GPIO.PUD_UP)

def Led(x):
    if x == 0:
        GPIO.output(Rpin, 1)
        GPIO.output(Gpin, 0)
    if x == 1:
        GPIO.output(Rpin, 0)
        GPIO.output(Gpin, 1)

def Print(x):
    global tmp
    if x != tmp:
        if x == 0:
            print('###########')
            print('#   on    #')
            print('###########')
        if x == 1:
            print('###########')
            print('#  off    #')
            print('###########')
        tmp = x

def loop():
    while True:
        Led(GPIO.input(TouchPin))
        Print(GPIO.input(TouchPin))

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
