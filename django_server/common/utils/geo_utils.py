# -*- coding: utf-8 -*-
from math import radians, atan, tan, sin, cos, acos, atan2, sqrt


def calc_distance(lat_a, lng_a, lat_b, lng_b):
    '''
    :param lat_a: 纬度a
    :param lng_a: 经度a
    :param lat_b: 纬度b
    :param lng_b: 经度b
    :return distance: 距离(km)
    '''
    if lat_a == lat_b and lng_a == lng_b:
        return 0
    ra = 6378.140  # 赤道半径 (km)
    rb = 6356.755  # 极半径 (km)
    flatten = (ra - rb) / ra  # 地球扁率
    rad_lat_a = radians(lat_a)
    rad_lng_a = radians(lng_a)
    rad_lat_b = radians(lat_b)
    rad_lng_b = radians(lng_b)
    pa = atan(rb / ra * tan(rad_lat_a))
    pb = atan(rb / ra * tan(rad_lat_b))
    xx = acos(sin(pa) * sin(pb) + cos(pa) *
              cos(pb) * cos(rad_lng_a - rad_lng_b))
    c1 = (sin(xx) - xx) * (sin(pa) + sin(pb)) ** 2 / cos(xx / 2) ** 2
    c2 = (sin(xx) + xx) * (sin(pa) - sin(pb)) ** 2 / sin(xx / 2) ** 2
    dr = flatten / 8 * (c1 - c2)
    distance = ra * (xx + dr)
    return distance


def simpleDistance(lat_a, lng_a, lat_b, lng_b):
    R = 6373.0
    rad_lat_a = radians(lat_a)
    rad_lng_a = radians(lng_a)
    rad_lat_b = radians(lat_b)
    rad_lng_b = radians(lng_b)

    dlon = rad_lng_a - rad_lng_b
    dlat = rad_lat_a - rad_lat_b

    a = sin(dlat / 2)**2 + cos(rad_lat_a) * cos(rad_lat_b) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance
