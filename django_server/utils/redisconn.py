# coding=gbk
import redis


class Rediscon():
    def __init__(self):
        self.conn = redis.Redis(host='localhost', port=6379)

    # �ַ��� ��
    def set_str(self, key, value, time=0):
        if time == 0:
            self.conn.set(key, value)
        else:
            self.conn.setex(key, value, time)

    # �ַ���ȡ
    def get_str(self, key):
        value = self.conn.get(key)
        if value:
            value = str(value, encoding='utf8')
        else:
            return None
        return value

    # �ַ���ɾ��
    def del_str(self, key):
        return self.conn.delete(key)


    # ��
    def insert_set(self, key, value):
        for i in value:
            self.conn.sadd(key, i)

    # ȡ
    def find_set(self, key):
        value = self.conn.smembers(key)
        if value:
            list = []
            for i in value:
                list.append(str(i, encoding='utf8'))
            return list
        else:
            return None

    # hash ��
    def insert_hash(self, key, params, value):
        self.conn.hset(key, params, value)

    # hash ȡһ������
    def get_value(self, key, params):
        return self.conn.hget(key, params)

    # hash ��ȡ���
    def get_all_value(self, key):
        return self.conn.hgetall(key)

    # hash ɾ��
    def del_hash(self, key, params):
        self.conn.hdel(key, params)


r = Rediscon()
# rset.insert_set('name1',['/index','/login','/asdasd','/asdasdfw233r'])
# res = rset.find_set('name1')
# print(res)







