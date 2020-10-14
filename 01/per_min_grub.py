import cv2
import time
import os

if not os.path.exists('./image_record'):
    os.mkdir('./image_record')

cap = cv2.VideoCapture(0)
n =1245
images = os.listdir('image_record')
while cap.isOpened():
    ret, frame = cap.read()
    print('第 %d 张'%n)
    filename = './image_record/' +  time.strftime('%Y-%m-%d %H_%M_%S', time.localtime())+'--'+str(n)+'.jpg'
    cv2.imwrite(filename, frame)
    n = n+1
    time.sleep(60)
    if n>1420:
        break
    '''
    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break
    '''
cap.release()
cv2.destroyAllWindows()
    
