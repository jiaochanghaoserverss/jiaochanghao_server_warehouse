# -*- coding: utf-8 -*-


def bytes_to_show(val):
    """ 字节转为更高级别的单位 """
    try:
        val = int(val)
    except:
        return val
    units = ['KB', 'MB', 'GB']
    ret = ''
    v = val
    for u in units:
        v = v / 1000.0
        if v < 1000:
            ret = '%.2f%s' % (v, u)
            break
    return ret

def show_num_unit(num, default=0):
    """ 数字转化为中文单位 """
    try:
        num = int(num)
    except:
        return default
    if num >= 10000:
        return '%d万' % (num // 10000)
    elif num >= 1000:
        return '%d千' % (num // 1000)
    return num


def show_percent(numerator, denominator):
    if denominator == 0:
        return '-'
    if not numerator or not denominator:
        return '0.00%'
    return '%.2f%%' % (numerator * 100.0 / denominator)


def show_permillage(p):
    return '%.1f%%' % (p / 10.0)


def index2abcd(index):
    """ 根据索引给出ABCD选项 """
    return chr(ord('A')+index)


def num_to_chinese(value):
    """ 数字转化为中文数字 """
    m = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十']
    if value <= 10:
        return m[value]
    if value < 20:
        return '十'+m[value % 10]
    if value < 99:
        s = m[value/10]+'十'
        if value % 10:
            s += m[value % 10]
        return s
    return ''


def yuan2fen(f):
    """ 元转化为分 """
    return int(round(f*100))

def show_price(amount):
    """ 显示金额, (分)转化为(元) """
    if not amount:
        return '0'
    p = amount * 1.0 / 100
    fen = abs(amount) % 100
    if fen > 0:
        if fen % 10 > 0:
            return '%.2f' % p
        return '%.1f' % p
    return '%d' % p


def show_discount(amount):
    """ 显示折扣 """
    if amount % 10 > 0:
        return '%.1f' % (amount/10.0)
    return amount/10


def show_sign_price(amount):
    """ 显示金额(显示正负), (分)转化为(元) """
    if not amount:
        return '0'
    sign = '+' if amount >= 0 else ''
    yuan = int(amount / 100)
    fen = amount % 100
    if fen > 0:
        if fen % 10 > 0:
            return '%s%d.%02d' % (sign, yuan, fen)
        return '%s%d.%d' % (sign, yuan, int(fen/10))
    return '%s%d' % (sign, yuan)


def show_sign_number(num, show_zero='+'):
    """ 显示有符号的数字 """
    assert isinstance(num, (int, float))
    if num == 0:
        if show_zero == '+':
            return '+0'
        return '-0'
    if num > 0:
        return '+%s' % num
    return '%s' % num
