from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from PIL import Image
import numpy as np
import os, json

from .libs import make_qr_code, make_qr_code_with_icon, decodeDisplay, decode_qr_code
from django_site.settings import BASE_DIR, MEDIA_DIR


def qr_index(request):
    if request.method == 'GET':
        return render(request, "qrcode_detect/qr_index.html")


def qrcode_no_icon(request):
    data = {'status': 0}
    if request.method == 'POST':
        save_img = os.path.join(BASE_DIR, 'static/image/qrcode.png')
        content = request.POST.get('content')
        make_qr_code(content, save_img)
        data['status'] = 1
        result = decode_qr_code(save_img)
        if len(result):
            print(result[0].data.decode('utf-8'))
        else:
            print('cant not recognise')
    return HttpResponse(json.dumps(data))


def qrcode_with_icon(request):
    data = {'status': 0}
    if request.method == 'POST':
        icon_img = os.path.join(BASE_DIR, 'static/image/icon.jpg')
        save_img = os.path.join(BASE_DIR, 'static/image/icon_qrcode.png')
        content = request.POST.get('content')
        make_qr_code_with_icon(content, icon_img, save_img)
        data['status'] = 1
        result = decode_qr_code(save_img)
        if len(result):
            print(result[0].data.decode('utf-8'))
        else:
            print('cant not recognise')
    return HttpResponse(json.dumps(data))


def upload_file(request):
    print(MEDIA_DIR)
    data = {'status': 0}
    if request.is_ajax():
        files = request.FILES.getlist('files')
        print("result: %s" % files)
        print(files[0].name)
        if files:
            data['status'] = 1
            for i in files:
                file_name = str(i)
                file_img = os.path.join(BASE_DIR, "media/" + file_name)
                icon_img = os.path.join(BASE_DIR, 'static/image/icon.jpg')
                with open(icon_img, "wb") as f:
                    for chunk in i.chunks(chunk_size=2014):
                        f.write(chunk)
                print(i)
        return HttpResponse(json.dumps(data))


def pic_show(request):
    pic_list = os.listdir(os.path.join(BASE_DIR, "static/image"))
    print(pic_list)
    return render(request, "qrcode_detect/pic.html", locals())


def download_file(request):
    pass
