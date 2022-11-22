import datetime


def cal_status(start, end):
    now = datetime.datetime.now()
    if start > now:
        return dict(value=0, display="未开始")
    if start <= now <= end:
        return dict(value=1, display="进行中")
    else:
        return dict(value=2, display="已结束")
