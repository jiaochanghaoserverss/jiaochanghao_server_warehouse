# coding=gbk
import redis


class Rediscon():
    def __init__(self):
        self.conn = redis.Redis(host='localhost', port=6379)

    # 字符串 存
    def set_str(self, key, value, time=0):
        if time == 0:
            self.conn.set(key, value)
        else:
            self.conn.setex(key, value, time)

    # 字符串取
    def get_str(self, key):
        value = self.conn.get(key)
        if value:
            value = str(value, encoding='utf8')
        else:
            return None
        return value

    # 字符串删除
    def del_str(self, key):
        return self.conn.delete(key)


    # 存
    def insert_set(self, key, value):
        for i in value:
            self.conn.sadd(key, i)

    # 取
    def find_set(self, key):
        value = self.conn.smembers(key)
        if value:
            list = []
            for i in value:
                list.append(str(i, encoding='utf8'))
            return list
        else:
            return None

    # hash 存
    def insert_hash(self, key, params, value):
        self.conn.hset(key, params, value)

    # hash 取一个属性
    def get_value(self, key, params):
        return self.conn.hget(key, params)

    # hash 获取多个
    def get_all_value(self, key):
        return self.conn.hgetall(key)

    # hash 删除
    def del_hash(self, key, params):
        self.conn.hdel(key, params)


r = Rediscon()
# rset.insert_set('name1',['/index','/login','/asdasd','/asdasdfw233r'])
# res = rset.find_set('name1')
# print(res)







