import time
from celery import task
import os

@task
def func_test():
    print('hello ...')
    time.sleep(5)
    print('world ...')
    

@task    
def setServoAngle(flag, angleX):
    os.system("python3 /home/pi/right_motor.py {} {}".format(flag, angleX))
    
