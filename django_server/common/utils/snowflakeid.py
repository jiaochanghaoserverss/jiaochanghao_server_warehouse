# -*- coding: utf-8 -*-

'''
|                      64bit                        |
| 1bit  |   41bit   |   4bit  |   6bit    |  12bit |
| Empty  | Timestamp | Worker  | ProcessID | Number |
| 空位   | 时间戳(秒)  |  机器位  | 进程位     | 序号位  |


ProcessID: 多数Linux操作系统默认进程数位0x7fff
'''

import os
import time
import threading
import random

lock = threading.Lock()

__all__ = ('ProcessSnowflakeID', 'get_worker_id_from_cache')


class SingletonMeta(type):
    """
    python Singleton, use as:
    class MyClass(metaclass=SingletonMeta):
        pass
    http://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

    def get_instance(cls):
        return cls._instances.get(cls, None)


class ProcessSnowflakeID(metaclass=SingletonMeta):
    twepoch = 1514736000  # 2018-01-01

    # int64_bits = 64

    worker_id_bits = 4
    process_id_bits = 6
    sequence_bits = 12

    max_worker_id = -1 ^ (-1 << worker_id_bits)
    max_process_id = -1 ^ (-1 << process_id_bits)
    # max_sequence_id = -1 ^ (-1 << sequence_bits)

    process_id_shift = sequence_bits
    worker_id_shift = sequence_bits + process_id_bits
    timestamp_left_shift = sequence_bits + process_id_bits + worker_id_bits
    sequence_mask = -1 ^ (-1 << sequence_bits)

    def __init__(self, worker_id: int):
        if worker_id < 0 or worker_id > self.max_worker_id:
            raise ValueError('invalid work id: %s' % worker_id)

        self.worker_id = worker_id
        self.process_id = os.getpid() & self.max_process_id
        self.last_timestamp = -1
        self.sequence = 0

    def _next(self) -> int:
        timestamp = self._get_timestamp()
        if timestamp < self.last_timestamp:
            raise Exception('clock is moving backwards')
        if self.last_timestamp == timestamp:
            sequence = (self.sequence + 1) & self.sequence_mask
            if sequence == 0:
                timestamp = self.til_next_second()
        else:
            sequence = random.randint(0, 9)

        self.sequence = sequence
        self.last_timestamp = timestamp

        _ts = (timestamp - self.twepoch) << self.timestamp_left_shift
        _worker = self.worker_id << self.worker_id_shift
        _process = self.process_id << self.process_id_shift

        return _ts | _worker | _process | sequence

    def next(self) -> int:
        """
        获取下一个ID
        """
        with lock:
            return self._next()

    def _get_timestamp(self) -> int:
        return int(time.time())

    def til_next_second(self):
        ts = self._get_timestamp()
        while ts <= self.last_timestamp:
            ts = self._get_timestamp()
        return ts

    @classmethod
    def parse(self, snowflakeid: int):
        pass


def get_mac_address():
    """
    获取Mac地址
    """
    import uuid
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e + 2] for e in range(0, 11, 2)])


def get_worker_id_from_cache(client, cache_key):
    from .service_registry import RedisServiceRegistry
    mac = get_mac_address()
    r = RedisServiceRegistry(client)
    worker_id = r.register(cache_key, mac)
    try:
        return int(worker_id)
    except:
        return None
