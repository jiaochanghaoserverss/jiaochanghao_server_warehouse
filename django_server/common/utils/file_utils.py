# -*- coding: utf-8 -*-

import re

def is_image(filename):
    ret = False
    if filename:
        m = re.search(r'\.(png|jpg|jpeg|gif|bmp)$', filename, re.I)
        ret = bool(m)
    return ret


def is_video(filename):
    ret = False
    if filename:
        m = re.search(
            r'\.(avi|wmv|mpeg|mp4|mov|mkv|flv|f4v|m4v|rmvb|rm|3gp|dat|ts|mts|vob)$', filename, re.I)
        ret = bool(m)
    return ret
