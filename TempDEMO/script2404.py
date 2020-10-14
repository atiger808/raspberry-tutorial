'''
24.4 输入事件
1. 同步事件
   wait_for_edge()方法会将程序停止， 直到它在输入信号上检测到一个上升和下降信号
   如果想要程序暂停等待这个事件， 应该使用这个方法
这个脚本监听GPIO 24 信号。 程序会在第7行暂停不做任何事， 直到检测到有个下降的输入值
（记住：给输入通道接入高电平， 因此当你按下按钮时， 信号从高电平变成低电平）。当事件
发生时， 程序继续执行。
这个方法的缺点是一次只能等待一个事件。 如果某人在等待后门铃响时按下了前门铃，则将会错过
这个事件。下一个方法会解决这个问题
'''

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.wait_for_edge(24, GPIO.FALLING)
print('The button was pressed')
GPIO.cleanup()

