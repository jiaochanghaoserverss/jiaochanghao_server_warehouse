# -*- coding: utf-8 -*-

import logging
import urllib.parse


class UrlEditor(object):
    """
    编辑链接GET参数
    """

    def __init__(self, url):
        (self.scheme, self.netloc, self.path,
         self.query, self.frag) = urllib.parse.urlsplit(url)
        self.query_list = urllib.parse.parse_qsl(self.query)

    def get_qs(self, key, default=None):
        """
        获取某个GET参数
        :param key: 参数名
        :param default: 默认值
        """
        for (k, val) in self.query_list:
            if k == key:
                return val
        return default

    def unset_qs(self, key):
        """
        取消某个GET参数
        :param key: 参数名
        """
        pos = -1
        for i, (k, _) in enumerate(self.query_list):
            if k == key:
                pos = i
                break
        else:
            return
        try:
            del self.query_list[pos]
        except Exception as err:
            logging.error(err)

    def set_qs(self, key, val, append=False):
        """
        设置GET参数
        :param key: 参数名
        :param val: 具体值
        :param append: 是否添加在所有参数最后
        """
        pos = -1
        qs = (key, val)
        for i, (k, _) in enumerate(self.query_list):
            if k == key:
                pos = i
                break
        else:
            self.query_list.append(qs)
            return
        if append:
            try:
                del self.query_list[pos]
                self.query_list.append(qs)
            except Exception as err:
                logging.error(err)
        else:
            self.query_list[pos] = qs

    def get_url(self):
        """
        获取修改后的链接
        :return url
        """
        query = '&'.join(['%s=%s' % (k, v) for (k, v) in self.query_list])
        data = (self.scheme, self.netloc, self.path, query, self.frag)
        return urllib.parse.urlunsplit(data)
