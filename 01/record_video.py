import cv2
import os
def record_video():
    if not os.path.exists('./video/'):
        os.mkdir('./video/')
    cap = cv2.VideoCapture(0)
    fps = 24
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('./video/out.mp4', fourcc, fps, (640, 480))

    while (cap.isOpened()):
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        out.write(frame)
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

record_video()
