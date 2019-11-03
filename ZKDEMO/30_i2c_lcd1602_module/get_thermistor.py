#!/usr/bin/env python
import PCF8591 as ADC
import math

def get_temperature():
    ADC.setup(0x48)
    analogVal = ADC.read(0)
    Vr = 5 * float(analogVal) / 255
    Rt = 10000 * Vr / (5 - Vr)
    temp = 1 / (((math.log(Rt / 10000)) / 3950) + (1 / (273.15 + 25)))
    temp = temp - 273.15
    print('temperature = %s C'%temp)
    return '%.2f'%temp

if __name__ == '__main__':
    get_temperature()