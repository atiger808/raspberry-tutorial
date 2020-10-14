import cv2
import time
import os

############# 照片转换为延时摄影视频 ################
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('delay.mp4', fourcc, 24.0, (640, 480))

file_path = './image_record/'
if os.path.isdir(file_path):
    imgs = [os.path.join(file_path, i) for i in os.listdir(file_path)]
    imgs = sorted(imgs, key=lambda x: int(x.split('--')[-1].strip('.jpg')))

print(imgs[-1])
for i in range(len(imgs)):
    frame = cv2.imread(imgs[i])
    # cv2.imshow('frame', frame)
    out.write(frame)
    k = cv2.waitKey(2) & 0xff
    if k == 27:
        break
print('ok!')
cv2.destroyAllWindows()



'''
######### 延时摄影效果 ###########
cap = cv2.VideoCapture(r'D:\video\record_1567590397.mp4')
fourcc = cap.get(cv2.CAP_PROP_FPS)
n = 0
while cap.isOpened():
    ret, frame = cap.read()
    k = cv2.waitKey(1) & 0xff
    if n % (fourcc*3) == 0:
        cv2.imshow('frame', frame)
    if k == 27:
        break
    n = n+1

cap.release()
cv2.destroyAllWindows()
'''
