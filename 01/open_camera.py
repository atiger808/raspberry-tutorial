import cv2

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame=cap.read()
    cv2.imshow('frame', frame)
    k = cv2.waitKey(1) & 0xff
    if k==27:
        break
cap.release()
cv2.destroyAllWindows()
