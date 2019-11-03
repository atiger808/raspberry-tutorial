# _*_ coding: utf-8 _*_
# @Time     : 2019/10/16 1:03
# @Author   : Ole211
# @Site     : 
# @File     : 36_human_infrared.py    
# @Software : PyCharm
'''人体红外传感器
 HC-SR501 感应模块简介
     对照前面的参数以及电路图，找到下面的左右针脚正负极，中间的PIN为感应输出，感应到人体时，输出3.3V高电平，检测不到信号时输出0。同时还要求工作电压在4.5V-20V之间。恰好树莓派的P1编号中第2，4号PIN都是5V的电压，满足要求，所以这次我们要接5V的电压。

    参数调节旋钮是用来扭动控制一些参数的。比如探测的延时时间，灵敏度等等。具体可以参看 HC -SR501的说明书。这里我们都使用默认值。

    但是有一个关键的L H模式调节阀门要介绍一下，右上角有三个针脚，按照我实物照片，假定从上到下为123 。还有一个黄色的套接头，图中套接头接通了2 3号，代表了H模式，这个套接头是可以拔下来的，然后插到上面来，接通1 2号，代表了L模式。
    L模式是不可重复触发，当探测到一次人体时，输出一次高电平，保持一段时间恢复低电平，在此期间如果还是检测到了人体也不再延长这个高电平的时间。等到低电平的封锁时间（前面默认是2.5S）过了以后才又开始检测。
    H模式是可以重复触发，如果一直感应到人体时，会一直输出高电平，直到探测不到人体后保持小段时间然后恢复低电平。
2.人体红外传感器工作原理
菲涅尔透镜利用透镜的特殊光学原理，在探测器前方产生一个交替变化的“盲区”和“高灵敏区”，以提高它的探测接收灵敏度。当有人从透镜前走过时，人体发出的红外线就不断地交替从“盲区”进入“高灵敏区”，这样就使接收到的红外信号以忽强忽弱的脉冲形式输入，从而强其能量幅度。

3.功能特点：
1.全自动感应：当有人进入其感应范围则输入高电平，人离开感应范围则自动延时关闭高电平。输出低电平。
2.光敏控制（可选）：模块预留有位置，可设置光敏控制，白天或光线强时不感应。光敏控制为可选功能，出厂时未安装光敏电阻。如果需要，请另行购买光敏电阻自己安装。
3.两种触发方式：L不可重复，H可重复。可跳线选择，默认为H。
A.不可重复触发方式：即感应输出高电平后，延时时间一结束，输出将自动从高电平变为低电平。
B.可重复触发方式：即感应输出高电平后，在延时时间段内，如果有人体在其感应范围内活动，其输出将一直保持高电平，直到人离开后才延时将高电平变为低电干（感应模块检测到人体的每一次活动后会自动顺延一个延时时间段，并且以最后一次活动的时间为延时时间的起始点）。具有感应封锁时间（默认设置：2.5S封锁时间）：感应模块在每一次感应输出后（高电平变成低电平）可以紧跟着设置一个封锁时间段，在此时间段内感应器不接受任何感应信号。此功能可以实现“感应输出时间“和一封锁时间“两者的间隔工作，可应用于间隔探测产品；同时此功能可有效抑制负载切换过程中产生的各种干扰。（此时间可设置在零点几秒一几十秒钟）。
4.工作电压范围宽：默认工作电压DC4.5V-20V。
5.微功耗：静态电流<50微安，特别适合干电池供电的自动控制产品。
6.输出高电平信号：可方便与各类电路实现对接。
————————————————
版权声明：本文为CSDN博主「zhq_blog」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/zhq_blog/article/details/88671175
'''
import RPi.GPIO as GPIO
import time

Infrared_pin = 20
time_out = 0.2
R_pin = 22
G_pin = 23
B_pin = 24


def setup(Infrared_pin, R_pin, G_pin, B_pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(Infrared_pin, GPIO.IN)

    GPIO.setup(R_pin, GPIO.OUT)
    GPIO.setup(G_pin, GPIO.OUT)
    GPIO.setup(B_pin, GPIO.OUT)


def rgb(red=False, green=False, blue=False, delay=0.1):
    GPIO.output(R_pin, red)
    GPIO.output(G_pin, green)
    GPIO.output(B_pin, blue)
    time.sleep(delay)


def beep():
    while GPIO.input(Infrared_pin):
        GPIO.output(Buzzer_pin, GPIO.LOW)
        time.sleep(0.3)
        GPIO.output(Buzzer_pin, GPIO.HIGH)
        time.sleep(0.3)


def detect():
    while True:
        if GPIO.input(Infrared_pin) == True:
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + '-------Someone is here!!!')
            rgb(green=True)
        else:
            print('---------Infrared is Detecting-----------')
            rgb(green=False)
            time.sleep(time_out)


def destroy():
    GPIO.cleanup()


if __name__ == '__main__':
    setup(Infrared_pin, R_pin, G_pin, B_pin)
    try:
        detect()
    except KeyboardInterrupt:
        destroy()
