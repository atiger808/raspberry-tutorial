from django.shortcuts import render, redirect, reverse
from django.shortcuts import get_object_or_404
from django.http import StreamingHttpResponse
from django.http import HttpResponse
from django.views.generic import View
import threading
import json, re
import os

from .libs import Car, detect_face, detect_color, generate, motor_libs, servo_libs, slide_libs, create_qrcode_libs, vs, \
    WIDTH
# 分布式异步celery使用
from webpage import tasks
from django_site.settings import BASE_DIR


def index(request):
    data = {
        "front": "front",
        "leftfront": "leftfront",
        "rightfront": "rightfront",
        "rear": "rear",
        "stop": "stop",
        "auto": "auto",
        "shoot": "shoot",
        "steer_top": "steer_top",
        "steer_bottom": "steer_bottom",
        "width": WIDTH
    }
    context = {
        "cmd": data
    }
    return render(request, 'webpage/index.html', context=context)


def servo(request):
    status = request.POST.get("status")
    data = {"status": 0}
    print(status)
    if status:
        servo_libs(status)
        data["status"] = 1
    return HttpResponse(json.dumps(data))


def motor(request):
    status = request.POST.get("status")
    print(status)
    data = {"status": 0}
    if status:
        motor_libs(status)
        data["status"] = 1
    return HttpResponse(json.dumps(data))


def slide(request):
    status = request.POST.get('slide')
    data = {"status": 0}
    print(status)
    if status:
        slide_libs(status)
        data['status'] = 1
    return HttpResponse(json.dumps(data))


def scan_qr_result(request):
    code = request.GET.get('code')
    code = re.findall(r'[0-9a-zA-Z]{32}', code)
    print(code)
    if code and len(code[0]) == 32:
        qrcode = code[0]
        print('ok')
        return render(request, 'webpage/result.html', locals())
    return HttpResponse('None')


def getImgChaptchaDTO(request):
    pass


def qr_index(request):
    return render(request, "webpage/qr_index.html")


def create_qrcode(request):
    from segno import helpers
    import qrcode
    data = {"status": 0}
    if request.method == "POST":
        content = request.POST.get("content")
        savepath = os.path.join(BASE_DIR, "static/image/qr.png")

        '''
        # 生成验证码
        # 方法一: from segno import helpers
        qr = helpers.make_mecard(content, "ok")
        qr.save(savepath, scale=10)
        '''

        # 方法二: import qrcode
        img = create_qrcode_libs(content, savepath)

        data["status"] = 1
        return HttpResponse(json.dumps(data))


def video_feed(request):
    # global vs
    t = threading.Thread(target=detect_face, args=(32,))
    t.daemon = True
    t.start()
    # vs.stop
    return StreamingHttpResponse(generate(), content_type='multipart/x-mixed-replace; boundary=frame')


def maps(request):
    return render(request, 'theWorldDisease.html')
