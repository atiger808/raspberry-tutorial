import time
from run_time import run_time as run
import sys
@run
def delay_time(n):
    t1 = time.time()
    for i in range(int(n)):
        x = 1
    print(time.time()-t1)

if __name__ == '__main__':
    delay_time(sys.argv[1])
