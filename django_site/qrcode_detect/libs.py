import cv2
import os
import json
import qrcode
import numpy as np
from PIL import Image
from pyzbar import pyzbar


def make_qr_code(content, save_path=None):
    qr_code_maker = qrcode.QRCode(
        version=5,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=8,
        border=4,
    )
    qr_code_maker.add_data(data=content)
    qr_code_maker.make(fit=True)
    img = qr_code_maker.make_image()
    if save_path:
        img.save(save_path)
    else:
        print("save error")


def make_qr_code_with_icon(content, icon_path, save_path=None):
    if not os.path.exists(icon_path):
        raise FileExistsError(icon_path)

    # 1，生成二维码图片
    qr_code_maker = qrcode.QRCode(
        version=5,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=8,
        border=4,
    )
    qr_code_maker.add_data(data=content)
    qr_code_maker.make(fit=True)
    qr_code_img = qr_code_maker.make_image().convert("RGBA")

    # 2，导入图标， 并修改尺寸
    icon_img = Image.open(icon_path)
    code_with, code_height = qr_code_img.size
    icon_img = icon_img.resize((code_with // 4, code_height // 4), Image.ANTIALIAS)
    # 3, 添加图标到二维码
    qr_code_img.paste(icon_img, (code_with * 3 // 8, code_height * 3 // 8))

    if save_path:
        qr_code_img.save(save_path)
        qr_code_img.show()
    else:
        print('save error')


def decode_qr_code(code_img_path):
    if not os.path.exists(code_img_path):
        raise FileExistsError(code_img_path)
    return pyzbar.decode(Image.open(code_img_path), symbols=[pyzbar.ZBarSymbol.QRCODE])


def decodeDisplay(frame):
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
    if len(barcodes):
        cv2.imwrite('qr.png', frame)
    return frame
