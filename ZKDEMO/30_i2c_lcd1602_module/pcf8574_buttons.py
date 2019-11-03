# _*_ coding: utf-8 _*_
# @Time     : 2019/10/8 1:08
# @Author   : Ole211
# @Site     : 
# @File     : pcf8574_buttons.py    
# @Software : PyCharm

import smbus
from time import sleep

class ButtonPanel():
    previous_data = 0; #Storage variable so that we can compare current and previous states

    def __init__(self, addr = 0x27, bus = 1, int_pin = None):
        self.bus_num = bus
        self.bus = smbus.SMBus(self.bus_num)
        self.addr = addr
        self.int_pin = int_pin

    def start(self):
        self.bus.write_byte(self.addr, 0xff)
        if self.int_pin is None:
            self.loop_polling()
        else:
            self.loop_interrupts()

    def loop_interrupts(self):
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
        GPIO.setup(self.int_pin, GPIO.IN)
        try:
            while True:
                while GPIO.input(self.int_pin) == False: #Monitoring just the GPIO pin, it's pulled down when one of the buttons is pressed
                    data = (~self.bus.read_byte(self.addr)&0xFF)
                    self.process_data(data)
                    self.previous_data = data
                sleep(0.1)
        except:
            raise
        finally:
            GPIO.cleanup()

    def loop_polling(self):
        while True:
            data = (~self.bus.read_byte(self.addr)&0xFF) #Bothering the IC each 100 milliseconds
            if data != self.previous_data:
                self.process_data(data)
                self.previous_data = data
            sleep(0.1)

    def process_data(self, data):
        data_difference = data ^ self.previous_data #XORing data
        #Now data_difference is a byte in which buttons that changed state are marked with 1 and buttons which didn't are marked with 0
        changed_buttons = []
        for i in range(8): #Going through bits of data_difference and getting the positions of buttons which changed state
            if data_difference & 1<<i:
                changed_buttons.append(i)
        for button_number in changed_buttons:
            if data & 1<<button_number: #Button pressed
                print("Button {} pressed".format(button_number))
            else: #Button released
                print("Button {} released".format(button_number))


if __name__ == "__main__":
    buttons = ButtonPanel(addr = 0x27, int_pin = 4)
    buttons.start()
