'''
24.5
2. 异步事件
   你一定必须停止整个程序然后等待一个事件发生. 相反, 可以使用异步事件.使用异步事件可以
   定义多个事件让程序来监听.每一个指向代码中的一个方法, 这个方法将在事件发生时触发
   可以使用 add_event_delete() 方法来定义这个事件和要触发的方法， 如下所示;
   GPIO.add_event_delete(channel, event, callback=method)
提示：减少开关弹跳
    你可能注意到， 在检测输入项的时， 有时候按钮开关会比较灵敏（例如按一次按钮会触发两次不同的接触）
    通常这个叫做弹跳，可以输入开关添加一个电容器来减少开关弹跳的次数， 也可以使用软件控制开关弹跳
    add_event_detect() 方法有一个bouncetime参数， 可以添加一个超时时间帮助解决这个问题

小结：
    本章探讨了树莓派上的GPIO接口。 我们完成了一个项目， 输出一个数字信号到GPIO引脚上， 并且还完成了
    一个项目以输出可以控制发动机 PWM 信号。 我们还完成了一个GPIO引脚上读取输入值的项目， 他允许检测按钮按下事件。
    可以使用这些概念来控制任何类型的电路， 从读取温度到运行机器人
'''

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.output(18, GPIO.LOW)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def backdoor(channel):
    GPIO.output(18, GPIO.HIGH)
    print('Back door')
    time.sleep(0.1)
    GPIO.output(18, GPIO.LOW)

def frontdoor(channel):
    GPIO.output(18, GPIO.HIGH)
    print('Front door')
    time.sleep(0.1)
    GPIO.output(18, GPIO.LOW)

GPIO.add_event_detect(24, GPIO.FALLING, callback=backdoor)

GPIO.add_event_detect(25, GPIO.FALLING, callback=frontdoor)

try:
    while True:
        pass
except KeyboardInterrupt:
    GPIO.cleanup()
print('End of program')

