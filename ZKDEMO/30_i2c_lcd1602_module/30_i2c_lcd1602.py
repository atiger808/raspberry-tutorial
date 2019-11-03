# _*_ coding: utf-8 _*_
# @Time     : 2019/10/8 1:03
# @Author   : Ole211
# @Site     : 
# @File     : pcf8574_lcd.py.py    
# @Software : PyCharm

import smbus
from time import sleep
import time
from get_cpu_temperature import get_cpu_temperature
from get_thermistor import get_temperature

def delay(time):
    sleep(time / 1000.0)


def delayMicroseconds(time):
    sleep(time / 1000000.0)


class Screen():
    enable_mask = 1 << 2
    rw_mask = 1 << 1
    rs_mask = 1 << 0
    backlight_mask = 1 << 3

    data_mask = 0x00

    def __init__(self, cols=20, rows=1, addr=0x27, bus=1):
        self.cols = cols
        self.rows = rows
        self.bus_num = bus
        self.bus = smbus.SMBus(self.bus_num)
        self.addr = addr
        self.display_init()

    def enable_backlight(self):
        self.data_mask = self.data_mask | self.backlight_mask

    def disable_backlight(self):
        self.data_mask = self.data_mask & ~self.backlight_mask

    def display_data(self, *args):
        self.clear()
        for line, arg in enumerate(args):
            self.cursorTo(line, 0)
            self.println(arg[:self.cols].ljust(self.cols))

    def cursorTo(self, row, col):
        offsets = [0x00, 0x40, 0x14, 0x54]
        self.command(0x80 | (offsets[row] + col))

    def clear(self):
        self.command(0x10)

    def println(self, line):
        for char in line:
            self.print_char(char)

    def print_char(self, char):
        char_code = ord(char)
        self.send(char_code, self.rs_mask)

    def display_init(self):
        delay(1.0)
        self.write4bits(0x30)
        delay(4.5)
        self.write4bits(0x30)
        delay(4.5)
        self.write4bits(0x30)
        delay(0.15)
        self.write4bits(0x20)
        self.command(0x20 | 0x08)
        self.command(0x04 | 0x08, delay=80.0)
        self.clear()
        self.command(0x04 | 0x02)
        delay(3)

    def command(self, value, delay=50.0):
        self.send(value, 0)
        delayMicroseconds(delay)

    def send(self, data, mode):
        self.write4bits((data & 0xF0) | mode)
        self.write4bits((data << 4) | mode)

    def write4bits(self, value):
        value = value & ~self.enable_mask
        self.expanderWrite(value)
        self.expanderWrite(value | self.enable_mask)
        self.expanderWrite(value)

    def expanderWrite(self, data):
        self.bus.write_byte_data(self.addr, 0, data | self.data_mask)


if __name__ == "__main__":
    screen = Screen(bus=1, addr=0x27, cols=16, rows=1)
    screen.enable_backlight()
    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print(now)
    line1 = 'Welcome to China!'
    screen.display_data(line1, '')
    sleep(5)
    while True:
        line2 = time.strftime('%m-%d %H:%M:%S', time.localtime(time.time()))
        line3 = 'CPU: ' + str(get_cpu_temperature()) +"'C"
        line4 = 'Temp: ' + str(get_temperature()) +"'C"
        screen.display_data(line2, line4)
        sleep(1)
        # screen.display_data(now[::-1], now)
        # sleep(1)
