# _*_ coding: utf-8 _*_
# @Time     : 2019/10/16 3:02
# @Author   : Ole211
# @Site     : 
# @File     : 36_2_human_infrared.py    
# @Software : PyCharm

import RPi.GPIO as GPIO
import time

Infrared_pin = 20
Buzzer_pin = 17
time_out = 0.2

GPIO.setmode(GPIO.BCM)
# Set pin as input
GPIO.setup(Infrared_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Echo
# GPIO.setup(Buzzer_pin, GPIO.OUT)  # Buzzer
# GPIO.output(Buzzer_pin, GPIO.HIGH)

Current_State = 0
Previous_State = 0


def beep():
    while GPIO.input(Infrared_pin):
        GPIO.output(Buzzer_pin, GPIO.LOW)
        time.sleep(0.3)
        GPIO.output(Buzzer_pin, GPIO.HIGH)
        time.sleep(0.3)

try:

    print("Waiting for PIR to settle ...")

    # Loop until PIR output is 0
    while GPIO.input(Infrared_pin) == 1:
        Current_State = 0

    print("  等待准备中..")

    # Loop until users quits with CTRL-C
    while True:

        # Read PIR state
        Current_State = GPIO.input(Infrared_pin)

        if Current_State == 1 and Previous_State == 0:
            # PIR is triggered
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + 'Someone is here!')
            # beep()
            # Record previous state
            Previous_State = 1
        elif Current_State == 0 and Previous_State == 1:
            # PIR has returned to ready state
            print("  等待准备中.. ")
            # GPIO.output(Buzzer_pin, GPIO.HIGH)
            Previous_State = 0

        # Wait for 10 milliseconds
        time.sleep(0.01)

except KeyboardInterrupt:
    print"  Quit"
    # Reset GPIO settings
    GPIO.cleanup()