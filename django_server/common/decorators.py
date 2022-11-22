

def get_or_none(func):
    """数据对象查询， 如果未查到给None"""
    def inner(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except:
            return None
    return inner
