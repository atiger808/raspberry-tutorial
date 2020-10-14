import time
import sys

def run_time(func):
    def wrapper(*args, **kwargs):
        t1= time.time()
        print('Start time: %s'%time.strftime('%x', time.localtime(t1)))
        back = func(*args, **kwargs)
        print('End time: %s'%(time.strftime('%x', time.localtime(time.time()))))
        print('Waste time: %s s'%(time.time()-t1))
        return back
    return wrapper


@run_time
def cal(n):
    s = 0
    for i in range(int(n)):
        i = 1

if __name__ == '__main__':
    cal(sys.argv[1])

