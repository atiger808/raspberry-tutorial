import RPi.GPIO as GPIO
import time

colors = [0xff0000, 0x00ff00, 0x0000ff, 0xffff00, 0x00ffff]
R = 11
G = 12
B = 13

def setup(Rpin, Gpin, Bpin):
    global pins
    global p_R, p_G, p_B
    pins = {'pin_R': Rpin, 'pin_G': Gpin, 'pin_B': Bpin}
    GPIO.setmode(GPIO.BOARD)
    for i in pins:
        GPIO.setup(pins[i], GPIO.OUT)
        GPIO.output(pins[i], GPIO.HIGH)
    
    p_R = GPIO.PWM(pins['pin_R'], 2000)
    p_G = GPIO.PWM(pins['pin_G'], 2000)
    p_B = GPIO.PWM(pins['pin_B'], 5000)
    
    p_R.start(100)
    p_G.start(100)
    p_B.start(100)
    
def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def off():
    for i in pins:
        GPIO.output(pins[i], GPIO.HIGH)
        
def setColor(col):
    R_val = (col & 0xff0000) >> 16
    G_val = (col & 0x00ff00) >> 8
    B_val = (col & 0x0000ff) >> 0
    
    R_val = map(R_val, 0, 255, 0, 100)
    G_val = map(G_val, 0, 255, 0, 100)
    B_val = map(B_val, 0, 255, 0, 100)
    
    p_R.ChangeDutyCycle(100 - R_val)
    p_G.ChangeDutyCycle(100 - G_val)
    p_B.ChangeDutyCycle(100 - B_val)
    
def loop():
    while True:
        for col in colors:
            setColor(col)
            time.sleep(1)
            
def destroy():
    p_R.stop()
    p_G.stop()
    p_B.stop()
    off()
    
if __name__ == '__main__':
    try:
        setup(R, G, B)
        loop()
    except KeyboardInterrupt:
        destroy()
