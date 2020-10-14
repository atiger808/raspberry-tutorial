'''
花式LED闪光灯
这段代码在GPIO 18 上开始发送PWM信号， 以1Hz的频率发送， 然后他开始
有个循环并且什么都不做， 在try代码中设置这个循环， 以便可以捕获Ctrl+C键以便停止

'''
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
blink = GPIO.PWM(18, 1)
try:
    blink.start(50)
    while True:
        pass
except KeyboardInterrupt:
    blink.stop()
GPIO.cleanup()

