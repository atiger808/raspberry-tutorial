import json, os
import cv2
import threading
from imutils.video import VideoStream
import imutils
import numpy as np

import RPi.GPIO as GPIO
from time import sleep
import time
import datetime
import random

import qrcode
from PIL import Image
from pyzbar import pyzbar

WIDTH = 640
HEIGHT = 480
FRAME_WIDTH = 1080
angle = 90
step = 45
l_step = 15
top_angle = 90
bottom_angle = 90
centerX, centerY = 0, 0
msg = ""
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cascade_dir = os.path.join(base_dir, 'static')


face_cascade = cv2.CascadeClassifier(os.path.join(cascade_dir, 'haarcascade_frontalface_default.xml'))
eye_cascade = cv2.CascadeClassifier(os.path.join(cascade_dir,'haarcascade_eye.xml'))
smile_cascade = cv2.CascadeClassifier(os.path.join(cascade_dir,'haarcascade_smile.xml'))
full_cascade = cv2.CascadeClassifier(os.path.join(cascade_dir,'haarcascade_upperbody.xml'))
lock = threading.Lock()
outputFrame = None
# cap = cv2.VideoCapture(0)
url = "http://admin:admin@192.168.43.1:8081/"
rtsp_url = "rtsp://admin:admin@192.168.43.1:8554/live"
cap = cv2.VideoCapture(0)

vs = ''
# vs = VideoStream(usePiCamera=2).start()  # 使用一个RPi相机模块
# vs = VideoStream(src=0).start()  # 如果您正在使用一个USB网络摄像头


if not os.path.exists('/home/pi/Videos/'):
    os.mkdir('/home/pi/Videos/')
fps = 24
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('/home/pi/Videos/out.mp4', fourcc, fps, (WIDTH, HEIGHT))


class SingleMotionDetector:
    def __init__(self, accumWeight=0.5):
        self.accumWeight = accumWeight
        self.bg = None

    def update(self, image):
        if self.bg is None:
            self.bg = image.copy().astype('float')
            return
        cv2.accumulateWeighted(image, self.bg, self.accumWeight)

    def detect(self, image, tVal=25):
        delta = cv2.absdiff(self.bg.astype('uint8'), image)
        thresh = cv2.threshold(delta, tVal, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.erode(thresh, None, iterations=2)
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        (minX, minY) = (np.inf, np.inf)
        (maxX, maxY) = (-np.inf, -np.inf)
        if len(cnts) == 0:
            return None
        for c in cnts:
            x, y, w, h = cv2.boundingRect(c)
            minX, minY = min(minX, x), min(minY, y)
            maxX, maxY = max(maxX, x + w), max(maxY, y + h)
        return thresh, (minX, minY, maxX, maxY)


class Car(object):
    def __init__(self):
        self.IN1 = 16
        self.IN2 = 13
        self.IN3 = 12
        self.IN4 = 6
        self.TRIG = 25
        self.ECHO = 26
        self.R_pin = 22
        self.G_pin = 23
        self.B_pin = 24
        self.Active_buzzer = 17
        self.Passive_buzzer = 5
        self.Left_TrackPin = 18
        self.Right_TrackPin = 27
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.IN3, GPIO.OUT)
        GPIO.setup(self.IN4, GPIO.OUT)
        GPIO.setup(self.TRIG, GPIO.OUT)
        GPIO.setup(self.ECHO, GPIO.IN)
        GPIO.setup(self.R_pin, GPIO.OUT)
        GPIO.setup(self.G_pin, GPIO.OUT)
        GPIO.setup(self.B_pin, GPIO.OUT)
        GPIO.setup(self.Active_buzzer, GPIO.HIGH)
        # GPIO.setup(self.Passive_buzzer, GPIO.OUT)
        GPIO.setup(self.Left_TrackPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.Right_TrackPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    ######## 方向操控 #######
    ######## 方向操控 #######
    def back(self):
        print('moror back...')
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)

    def forward(self):
        print('motor forward...')
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)

    def stop(self):
        print('motor stop...')
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)

    def turn_right(self):
        print('motor right...')
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)

    def turn_left(self):
        print('motor left')
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)

    def auto_pilot(self):
        if GPIO.input(self.Left_TrackPin) == GPIO.LOW and GPIO.input(self.Right_TrackPin) == GPIO.LOW:
            print('Both side line is White----Forward')
            self.forward()
        elif GPIO.input(self.Left_TrackPin) == GPIO.LOW and GPIO.input(self.Right_TrackPin) == GPIO.HIGH:
            print('Left line is White and Right is Black----Turn Right')
            self.turn_right()
            time.sleep(1.5)
        elif GPIO.input(self.Left_TrackPin) == GPIO.HIGH and GPIO.input(self.Right_TrackPin) == GPIO.LOW:
            print('Left line is Black and Right is White----Turn Left')
            self.turn_left()
            time.sleep(1.5)
        else:
            print('Both side line is Black----Forward')
            self.stop()

    ####### 超声波距离检测 ########
    def checkdist(self):
        GPIO.output(self.TRIG, 0)
        time.sleep(0.000002)

        GPIO.output(self.TRIG, 1)
        time.sleep(0.000015)
        GPIO.output(self.TRIG, 0)
        while GPIO.input(self.ECHO) == 0:
            pass
        t1 = time.time()
        while GPIO.input(self.ECHO) == 1:
            pass
        t2 = time.time()
        return (t2 - t1) * 340 / 2

    def rgb(self, red=False, green=False, blue=False, delay=0.1):
        GPIO.output(self.R_pin, red)
        GPIO.output(self.G_pin, green)
        GPIO.output(self.B_pin, blue)
        time.sleep(delay)

    def bright(self):
        self.rgb(red=True)
        self.rgb(green=True)
        self.rgb(blue=True)

    def buzzer_on(self):
        GPIO.output(self.Active_buzzer, GPIO.LOW)

    def buzzer_off(self):
        GPIO.output(self.Active_buzzer, GPIO.HIGH)

    def beep(self, x=0.2):
        GPIO.setup(self.Active_buzzer, GPIO.OUT)
        GPIO.output(self.Active_buzzer, GPIO.HIGH)
        self.buzzer_on()
        time.sleep(x)
        self.buzzer_off()
        time.sleep(x)

    def servo_motor(self, flag):
        global top_angle, bottom_angle, step
        if flag == "front":
            top_angle = top_angle + step
            if top_angle > 180:
                top_angle = 180
            os.system("python3 /home/pi/right_motor.py {} {}".format("top", top_angle))

        if flag == "rear":
            top_angle = top_angle - step
            if top_angle < 0:
                top_angle = 0
            os.system("python3 /home/pi/right_motor.py {} {}".format("top", top_angle))

        if flag == "leftfront":
            bottom_angle = bottom_angle + step
            if bottom_angle > 180:
                bottom_angle = 180
            os.system("python3 /home/pi/right_motor.py {} {}".format("bottom", bottom_angle))

        if flag == "rightfront":
            bottom_angle = bottom_angle - step
            if bottom_angle < 0:
                bottom_angle = 0
            os.system("python3 /home/pi/right_motor.py {} {}".format("bottom", bottom_angle))

        if flag == "stop":
            global minX, minY, maxX, maxY
            pass

        if flag == "stop":
            for angle in range(0, 181, step):
                bottom_angle = angle
                top_angle = random.randint(0, 190)

                os.system("python3 /home/pi/right_motor.py {} {}".format("bottom", bottom_angle))
                # os.system("python3 /home/pi/right_motor.py {} {}".format("top", top_angle))
                sleep(0.1)

    def setServoAngle(self, angleX, flag='bottom'):
        os.system("python3 /home/pi/right_motor.py {} {}".format(flag, angleX))

    def steer(self, flag):
        global angle, step
        angle = angle + step
        if angle == 180:
            step = -30
        if angle == 0:
            step = 30
        os.system("python3 /home/pi/right_motor.py {} {}".format(flag, angle))

    def destroy(self):
        GPIO.cleanup()


def detect_motion(frameCount):
    global vs, outputFrame, lock, out
    global centerX, centerY, bottom_angle, top_angle
    # tasks.setServoAngle.delay("bottom", bottom_angle)
    md = SingleMotionDetector(accumWeight=0.1)
    total = 0
    while True:
        frame = vs.read()
        frame = imutils.resize(frame, width=FRAME_WIDTH)
        height, width = frame.shape[:2]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)
        
        if total > frameCount:
            motion = md.detect(gray)
            if motion is not None:
                thresh, (minX, minY, maxX, maxY) = motion
                centerX, centerY = (minX + maxX) // 2, (minY + maxY) // 2
                if total % 16 == 0:
                    if (width // 3 * 2) > centerX > (width // 3):
                        pass
                    if centerX < (width // 3):
                        bottom_angle = bottom_angle + l_step
                        if bottom_angle > 180:
                            bottom_angle = 180
                    if centerX > (width // 3 * 2):
                        bottom_angle = bottom_angle - l_step
                        if bottom_angle < 0:
                            bottom_angle = 0
                    # tasks.setServoAngle.delay("bottom", bottom_angle)
                    os.system('python3 /home/pi/right_motor.py {} {}'.format('bottom', bottom_angle))
                print(centerX, bottom_angle)
                cv2.rectangle(frame, (minX, minY), (maxX, maxY), (0, 255, 0), 1)
        timestamp = datetime.datetime.now()
        cv2.putText(frame, timestamp.strftime('%A %d %B %Y %I:%M:%S%p'), (10, frame.shape[0] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 255), 1)
        frame = decodeDisplay(frame)
        md.update(gray)
        total = total + 1
        with lock:
            # out.write(frame)
            outputFrame = frame.copy()


def detect_color(frameCount):
    global outputFrame, lock
    global centerX, centerY, bottom_angle, top_angle
    total = 0
    while (cap.isOpened()):
        # 获取每一帧
        ret, frame = cap.read()
        frame = cv2.resize(frame, (WIDTH, HEIGHT))
        # 转换到hsv
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # 设置蓝色阈值
        lower_blue = np.array([100, 50, 50])
        upper_blue = np.array([130, 255, 255])
        # 红色阈值
        lower_red = np.array([156, 43, 46])
        upper_red = np.array([180, 255, 255])
        # 根据阈值构建掩膜
        lower_hsv = np.array([156, 43, 46])
        upper_hsv = np.array([180, 255, 255])
        mask = cv2.inRange(hsv, lowerb=lower_hsv, upperb=upper_hsv)
        mask = cv2.erode(mask, kernel=np.ones((5, 5), np.uint8), iterations=2)
        mask = cv2.dilate(mask, kernel=np.ones((5, 5), np.uint8), iterations=2)
        # 对原图和掩膜进行运算
        res = cv2.bitwise_and(frame, frame, mask=mask)
        _, conts, hier = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # 找出边界
        cnts = sorted(conts, key=cv2.contourArea, reverse=True)
        if len(cnts) > 0:
            dst = cnts[0]
            # 矩形框
            x, y, w, h = cv2.boundingRect(dst)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 3)
            centerX, centerY = x + w // 2, y + h // 2
            if total % 16 == 0:
                if (WIDTH // 3 * 2) > centerX > (WIDTH // 3):
                    pass
                if centerX < (WIDTH // 3):
                    bottom_angle = bottom_angle + l_step
                    # tasks.setServoAngle.delay("bottom", bottom_angle)
                    os.system('python3 /home/pi/right_motor.py {} {}'.format('bottom', bottom_angle))
                    if bottom_angle > 180:
                        bottom_angle = 180
                if centerX > (WIDTH // 3 * 2):
                    bottom_angle = bottom_angle - l_step
                    # tasks.setServoAngle.delay("bottom", bottom_angle)
                    os.system('python3 /home/pi/right_motor.py {} {}'.format('bottom', bottom_angle))
                    if bottom_angle < 0:
                        bottom_angle = 0
        print("%s, %s°" % (centerX, bottom_angle))
        frame = decodeDisplay(frame)
        timestamp = datetime.datetime.now()
        cv2.putText(frame, timestamp.strftime('%A %d %B %Y %I:%M:%S%p') + "    X %s Y %s" % (bottom_angle, top_angle),
                    (10, frame.shape[0] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.35, (255, 255, 255), 1)
        frame = decodeDisplay(frame)
        total = total + 1
        with lock:
            outputFrame = frame.copy()


def detect_face(frameCount):
    global outputFrame, lock
    global centerX, centerY, bottom_angle, top_angle
    total = 0
    while (cap.isOpened()):
        ret, frame = cap.read()
        frame = cv2.resize(frame, (WIDTH, HEIGHT))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # 检测人脸
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        if len(faces) > 0:
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 4)
                roi_gray = gray[y:y + h, x:x + w]
                roi_color = frame[y:y + h, x:x + w]
                # 用文字标记出来
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame, 'face-detect', (x, y), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
                centerX, centerY = x + w // 2, y + h // 2
                print("%s, %s°" % (centerX, bottom_angle))
                if total % 16 == 0:
                    if (WIDTH // 3 * 2) > centerX > (WIDTH // 3):
                        pass
                    if centerX < (WIDTH // 3):
                        bottom_angle = bottom_angle + l_step
                        if bottom_angle > 180:
                            bottom_angle = 180
                    if centerX > (WIDTH // 3 * 2):
                        bottom_angle = bottom_angle - l_step
                        if bottom_angle < 0:
                            bottom_angle = 0
                    # tasks.setServoAngle.delay("bottom", bottom_angle)
                    os.system('python3 /home/pi/right_motor.py {} {}'.format('bottom', bottom_angle))

                # 检测眼睛
                # eyes = eye_cascade.detectMultiScale(roi_gray)
                # for (ex, ey, ew, eh) in eyes:
                #     # 绘制矩形
                #     cv.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 1)
                #     # 绘制圆
                #     # cv.circle(roi_color, (ex+ew//2, ey+eh//2), int(np.sqrt((ew//2)**2 + (eh//2)**2)), (0, 255, 0), -1)
                #     # 用文字标记出来
                #     font = cv.FONT_HERSHEY_SIMPLEX
                #     cv.putText(roi_color, 'eye', (ex, ey), font, 1, (255, 255, 255), 1, cv.LINE_AA)
        # print('X:{} angle:{}'.format(centerX, bottom_angle))
        timestamp = datetime.datetime.now()
        cv2.putText(frame, timestamp.strftime('%A %d %B %Y %I:%M:%S%p') + "    X %s Y %s" % (bottom_angle, top_angle),
                    (10, frame.shape[0] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.35, (255, 255, 255), 1)
        frame = decodeDisplay(frame)
        total = total + 1
        with lock:
            outputFrame = frame.copy()


def servo_motion():
    global centerX, centerY, bottom_angle, top_angle
    print(x, y, bottom_angle)
    tasks.setServoAngle.delay("bottom", bottom_angle)
    if 220 > centerX > 180:
        pass
    if centerX < 180:
        bottom_angle = bottom_angle + 10
        if bottom_angle > 180:
            bottom_angle = 180
    if centerX > 220:
        bottom_angle = bottom_angle - 10
        if bottom_angle < 0:
            bottom_angle = 0
    tasks.setServoAngle.delay("bottom", bottom_angle)


def generate():
    global outputFrame, lock
    while True:
        with lock:
            # ret, outputFrame = cap.read()
            # outputFrame = cv2.rotate(outputFrame, 0)
            # cv2.imshow("o", outputFrame)
            if outputFrame is None:
                continue
            flag, encodeImage = cv2.imencode(".jpg", outputFrame)
            if not flag:
                continue
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodeImage) + b'\r\n')

def slide_libs(status):
    global bottom_angle
    bottom_angle = status
    print(bottom_angle)
    angleX = 180 - int(status)
    
    car = Car()
    # car.beep()
    car.setServoAngle(angleX)
    

def servo_libs(status):
    car = Car()
    car.servo_motor(status)

def motor_libs(status):
    car = Car()
    if status == 'front':
        dist = car.checkdist()
        print("距离: %0.3f m" % dist)
        if dist < 0.3:
            car.rgb(red=True)
            car.back()
            time.sleep(1)
            car.turn_right()
            time.sleep(1)
        else:
            # car.rgb(green=True)
            car.bright()
            car.beep()
            car.forward()
    elif status == 'leftfront':
        car.turn_left()
    elif status == 'rightfront':
        car.turn_right()
    elif status == 'rear':
        car.back()
    elif status == 'stop':
        car.stop()
    elif status == "shoot":
        if not os.path.isdir(base_dir + "/static/image"):
            os.makedirs(base_dir + "/static/image")
        cv2.imwrite(base_dir + "/static/image/out.jpg", outputFrame)
        print(base_dir)
        os.system("python3 {}/send_qq_img_email.py {}".format(base_dir, base_dir + "/static/image"))
    elif status == "steer_top":
        global angle, step
        car.steer("top")
    elif status == "steer_bottom":
        global angle, step
        car.steer("bottom")
    elif status == "auto":
        while True:
            if status == "auto":
                car.auto_pilot()
                time.sleep(0.2)
            else:
                break


def create_qrcode_libs(data, code_img_path):
    qr = qrcode.QRCode(
        version=2,
        error_correction = qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=1
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image()
    img.save(code_img_path)
    result = decode_qrcode_libs(code_img_path)
    if len(result):
        content = result[0].data.decode("utf-8")
        print("结果: %s" % content)
    else:
        content = ""
        print("Can not recognize!")
    return content


def decode_qrcode_libs(code_img_path):
    if not os.path.exists(code_img_path):
        raise FileExistsError(code_img_path)
    # Here, set only recognize QR Code and ignore other type of code 
    return pyzbar.decode(Image.open(code_img_path), symbols=[pyzbar.ZBarSymbol.QRCODE])
    

def decodeDisplay(frame):
    global flag
    car = Car()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    barcodes = pyzbar.decode(gray)
    for barcode in barcodes:
        x, y, w, h = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
        text = "{} {}".format(barcodeData, barcodeType)
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 255), 2)
        print("[INFO] Found, {} barcode: {}".format(barcodeType, barcodeData))
    flag = False
    car.rgb(red=True)
    if len(barcodes):
        flag = True
        car.rgb(green=True)
        car.beep()
        cv2.imwrite(os.path.join(base_dir, 'static/image/'+'qr.png'), frame)
    return frame


def get_world_map():
    import requests
    import time
    import json
    import pandas as pd
    timestamp = int(time.time() * 1000)
    real_url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_foreign&callback=&_=%d' % timestamp
    res = requests.get(real_url)
    data = res.json()
    dic_data = json.loads(data['data'])
    return dic_data