import RPi.GPIO as GPIO
import time

color = [0xff00, 0x00ff, 0x0ff0, 0xf00f]
Rpin = 12
Gpin = 13

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(Rpin, GPIO.OUT)
    GPIO.setup(Gpin, GPIO.OUT)
    
    GPIO.output(Rpin,GPIO.LOW)
    GPIO.output(Gpin, GPIO.LOW)

    global p_R, p_G
    p_R = GPIO.PWM(Rpin, 2000)
    p_G = GPIO.PWM(Gpin, 2000)

    p_R.start(0)
    p_G.start(0)

def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min)*(out_max - out_min)/(in_max - in_min) + out_min

def setColor(col):
    R_val = col >> 8
    G_val = col & 0x00ff

    R_val = map(R_val, 0, 255, 0, 100)
    G_val = map(G_val, 0, 255, 0, 100)

    p_R.ChangeDutyCycle(R_val)
    p_G.ChangeDutyCycle(G_val)
    
def bright(x):
    GPIO.output(Rpin, 1)
    GPIO.output(Gpin, 1)
    p_R.ChangeDutyCycle(100)
    p_G.ChangeDutyCycle(100)
    time.sleep(x)
    GPIO.output(Rpin, GPIO.LOW)
    GPIO.output(Gpin, GPIO.LOW)
    time.sleep(x)

def loop():
    while True:
        for col in color:
            setColor(col)
            time.sleep(0.5)

def destroy():
    p_R.stop()
    p_G.stop()
    GPIO.output(Rpin, GPIO.LOW)
    GPIO.cleanup()

if __name__ == '__main__':
    setup()
    time.sleep(5)
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
