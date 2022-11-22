#!/usr/bin/python
# -*- coding: utf-8 -*-

import traceback, logging

def check_first_image(image_data, min_width=300, min_height=300):
    try:
        import io
        from PIL import Image
        tmpIm = io.StringIO(image_data)
        im = Image.open(tmpIm)
        (width, height) = im.size
        if width < min_width or height < min_height:
            return False
        return True
    except:
        logging.error(traceback.format_exc())
    return False

def check_first_image_by_url(image_url, min_width=300, min_height=300):
    import urllib.request, urllib.error, urllib.parse
    try:
        file = urllib.request.urlopen(image_url)
        return check_first_image(file.read(), min_width, min_height)
    except:
        logging.error(traceback.format_exc())
    return False

def auto_check_first_image(image_url, image_data=None):
    size = 200
    if image_url.startswith('http://mmbiz.qpic.cn'): #来自微信的图片特殊
        size = 260
    if image_data:
        return check_first_image(image_data, size, size)
    return check_first_image_by_url(image_url, size, size)


def text2qrcode_image(text, version, border=4, fill_color='black'):
    import qrcode
    qr = qrcode.QRCode(
        version=version,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=border,
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color)
    return img

def text2qrcode(text, version, border=4):
    img = text2qrcode_image(text, version, border)
    import io
    sio = io.BytesIO()
    img.save(sio)
    return sio.getvalue()

'''
打开一个图片，参数可以是本地路径也可以是url
'''
def open_image(uri):
    try:
        from PIL import Image
        if uri.find('://') < 0:
            img = Image.open(uri)
            return img
        import io, urllib.request, urllib.error, urllib.parse
        file = urllib.request.urlopen(uri)
        sio = io.BytesIO(file.read())
        img = Image.open(sio)
        return img
    except:
        logging.error(traceback.format_exc())
    return None

'''
将一个图片image粘贴找另外一张背景图上，实现图片的合并
'''
def paste_image(bg_image, image, box):
    try:
        region = image.resize((box[2] - box[0], box[3] - box[1]))
        bg_image.paste(region, box)
        return bg_image
    except:
        logging.error(traceback.format_exc())
    return None


