# -*- coding: utf-8 -*-
import re
import time
from datetime import date, datetime, timedelta
from datetime import time as dt_time
import calendar
from six import integer_types

###############################################################################
# Define
###############################################################################
WEEK_PER_YEAR = 52
WEEK_PER_MONTH = 4

TIME_AGO = {
    'years': ['年'],
    'months': ['月'],
    'weeks': ['周'],
    'days': ['天', '日'],
    'hours': ['时', '小时'],
    'minutes': ['分'],
    'seconds': ['秒'],
}

__ptn_time_ago = r'(?P<time>\d+)\s*(?:个)?(?:%s)'
__time_re = {
    k: re.compile(__ptn_time_ago % '|'.join(v))
    for k, v in list(TIME_AGO.items())
}


###############################################################################

def get_timestamp_by_format_timeago(data, format_time):
    """
    从 '1天前' '1天 2小时前' 提取出当时的时间戳
    @format_time('(?P<days>\d+)\s小时前'):  正则表达式 参考TIME_AGO
    """
    ret = data
    try:
        _re = re.compile(format_time, flags=re.I)
    except Exception as err:
        print(err)
    m_time = _re.search(data)
    if not m_time:
        return ret
    time_dict = m_time.groupdict().copy()
    timedelta_dict = {
        'weeks': 0,
        'days': 0,
        'hours': 0,
        'seconds': 0,
    }
    if 'years' in time_dict:
        years = int(time_dict.pop('years'))
        timedelta_dict['weeks'] += WEEK_PER_YEAR * years
    if 'months' in time_dict:
        months = int(time_dict.pop('months'))
        timedelta_dict['weeks'] += WEEK_PER_MONTH * months
    for key in list(timedelta_dict.keys()):
        add = int(time_dict.get(key, 0))
        timedelta_dict[key] += add
    if not all(timedelta_dict):
        return ret
    ret = datetime.now() - timedelta(**timedelta_dict)
    ret = int(time.mktime(ret.timetuple()))
    return ret


def get_timestamp_from_timeago(data):
    if data.find('刚刚'):
        return int(time.time())
    global __time_re, TIME_AGO, WEEK_PER_YEAR, WEEK_PER_MONTH
    timedelta_dict = dict.fromkeys(list(TIME_AGO.keys()), 0)
    for k, v in __time_re.items():
        m = v.search(data)
        if not m:
            continue
        timedelta_dict[k] += int(m.group('time'))
    if not all(timedelta_dict):
        return 0
    years = timedelta_dict.pop('years')
    if years:
        timedelta_dict['weeks'] += WEEK_PER_YEAR * years
    months = timedelta_dict.pop('months')
    if months:
        timedelta_dict['weeks'] += WEEK_PER_MONTH * months
    ret = datetime.now() - timedelta(**timedelta_dict)
    ret = int(time.mktime(ret.timetuple()))
    return ret


def date2str(dt):
    return dt.strftime('%Y-%m-%d')


def str2date(dt):
    t = dt.split('-')
    return date(int(t[0]), int(t[1]), int(t[2]))


def prev_date(dt):
    return dt + timedelta(days=-1)


def get_today_str():
    return date2str(date.today())


def get_yesterday_str():
    yesterday = date.today() + timedelta(days=-1)
    return date2str(yesterday)


def get_date_month_date_range(dt):
    _, monthRange = calendar.monthrange(dt.year, dt.month)
    firstDate = date(year=dt.year, month=dt.month, day=1)
    lastDate = date(year=dt.year, month=dt.month, day=monthRange)
    return (firstDate, lastDate)


def get_date_month_date_range_str(dt):
    (firstDate, lastDate) = get_date_month_date_range(dt)
    return (date2str(firstDate), date2str(lastDate))


def get_date_month_date_open_range(dt):
    (firstDate, lastDate) = get_date_month_date_range(dt)
    lastDate += timedelta(days=1)
    return (firstDate, lastDate)


def get_this_month_date_range_str():
    dt = date.today()
    return get_date_month_date_range_str(dt)


def get_last_month_date_range_str():
    dt = date.today()
    dt = dt + timedelta(days=-(dt.day + 1))
    return get_date_month_date_range_str(dt)


def get_date_week_date_range(dt):
    firstDate = dt + timedelta(days=-dt.weekday())
    lastDate = dt + timedelta(days=(6 - dt.weekday()))
    return (firstDate, lastDate)


def get_date_week_date_range_str(dt):
    (firstDate, lastDate) = get_date_week_date_range(dt)
    return (date2str(firstDate), date2str(lastDate))


def get_date_week_date_open_range(dt):
    (firstDate, lastDate) = get_date_week_date_range(dt)
    lastDate += timedelta(days=1)
    return (firstDate, lastDate)


def get_this_week_date_range_str():
    dt = date.today()
    return get_date_week_date_range_str(dt)


def get_last_week_date_range_str():
    dt = date.today()
    dt = dt + timedelta(days=-(dt.weekday() + 1))
    return get_date_week_date_range_str(dt)


def get_last_month_today(dt=None):
    if not dt:
        dt = date.today()
    dt2 = dt + timedelta(days=-dt.day)  # 上月最后一天
    day = min(dt.day, dt2.day)
    return date(dt2.year, dt2.month, day)


def get_last_month_tomorrow():
    dt = get_last_month_today() + timedelta(days=1)
    return dt


def get_next_month_today(dt=None):
    if not dt:
        dt = date.today()
    year = dt.year
    month = dt.month + 2
    if month > 12:
        month = (dt.month + 2) % 12
        year += 1
    dt2 = date(year, month, 1) + timedelta(days=-1)  # 下月的最后一天
    day = min(dt.day, dt2.day)
    return date(dt2.year, dt2.month, day)


def get_next_month_first_day(dt=None):
    if not dt:
        dt = date.today()
    year = dt.year
    month = dt.month + 1
    if month > 12:
        month = 1
        year += 1
    return date(year, month, 1)


def get_date_range(dt):
    assert isinstance(dt, (datetime, date))
    combine = datetime.combine
    return (combine(dt, dt_time.min), combine(dt, dt_time.max))


def get_today_range():
    return get_date_range(date.today())


def get_day_cname(day):
    """ 给定日期, 获取距离今天的中文显示 """
    assert isinstance(day, date)
    names = ['{delta}天前', '前天', '昨天', '今天', '明天', '后天', '{delta}天后']
    today_index = 3
    today = date.today()
    delta = (day - today).days
    index = min(len(names), max(0, delta + today_index))
    return names[index].format(delta=abs(delta) - 1)


def time_ago(value):
    """ 给定时间, 获取已经过去的时间显示 """
    if isinstance(value, date):
        timestamp = time.mktime(value.timetuple())
    elif isinstance(value, integer_types):
        timestamp = value
    else:
        return value
    now = time.time()
    diff = now - timestamp
    if diff < 5:
        return '刚刚'
    if diff < 60:
        return '%d秒前' % (diff)
    if diff < 3600:
        return '%d分钟前' % (diff / 60)
    if diff < 86400:
        return '%d小时前' % (diff / 3600)
    if diff < 86400 * 31:
        return '%d天前' % (diff / 86400)
    nd = datetime.now()
    if diff < 86400 * 365:
        return '%d个月前' % ((nd.month + 11 - value.month) % 12 + 1)
    return '%d年前' % (nd.year - value.year)


def seconds_to_clock(val):
    """ 给定秒数, 获取换算后的小时,分钟,秒数 """
    try:
        val = int(val)
    except:
        return val
    hour = val / 3600
    tmp = val % 3600
    minute = tmp / 60
    second = tmp % 60
    return int(hour), int(minute), int(second)


def seconds_to_number_clock(val):
    return '%02d:%02d:%02d' % seconds_to_clock(val)


def seconds_to_show(val):
    hour, minute, second = seconds_to_clock(val)
    ret = ''
    if hour:
        ret += '%s小时' % hour
    if minute:
        ret += '%s分钟' % minute
    if second:
        ret += '%s秒' % second
    return ret


def date_week_day(day):
    """ 星期的中文表示 """
    assert isinstance(day, (date, datetime))
    enum = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    idx = day.weekday()
    return enum[idx]


def days_to_now(dt):
    """ 某天距离现在有几天 """
    if isinstance(dt, datetime):
        delta = datetime.now() - dt
    elif isinstance(dt, datetime.date):
        delta = date.today() - dt
    else:
        return 0
    return delta.days


def birthday2age(dt):
    """ 生日转化为年龄 """
    if not isinstance(dt, datetime) and isinstance(dt, date):
        dt = datetime(dt.year, dt.month, dt.day)
    delta = datetime.today() - dt
    return delta.days / 365


if __name__ == '__main__':
    d = '1天前'
    print(get_timestamp_from_timeago(d))
    d = '1年3个月11天12秒前'
    print(get_timestamp_from_timeago(d))
