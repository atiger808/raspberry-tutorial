import cv2
import pyzbar.pyzbar as pyzbar
from libs import make_qr_code_with_icon, decode_qr_code, decodeDisplay


def detect():
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        im = decodeDisplay(frame)
        cv2.waitKey(5)
        cv2.imshow('o', im)
        if cv2.waitKey(10)& 0xff == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    detect()




