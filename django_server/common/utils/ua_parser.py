# -*- coding: utf-8 -*-

import logging
import traceback
import re
from common.lru_cache import LruCache


SPIDER_LIST = {
    r'(?P<baidu>Baiduspider)',
    r'(?P<google>Googlebot|Mediapartners-Google)',
    r'(?P<soso>Soso.*spider)',
    r'(?P<sogou>Sogou.*?spider)',
    r'(?P<msn>msnbot)',
    r'(?P<yahoo>Yahoo.*?Slurp)',
    r'(?P<youdao>youdao.*?spider)',
    r'(?P<bing>bingbot)',
    r'(?P<haosou>360Spider)',
    r'(?P<easou>EasouSpider)',
    r'(?P<jike>JikeSpider)',
    r'(?P<alexa>crawler.*alexa)',
    r'(?P<dnspod>DNSPod)',
    # new
    r'(?P<yunyun>YYSpider)',
    r'(?P<yandex>YandexBot)',
    r'(?P<ahrefs>AhrefsBot)',
    r'(?P<linkdex>linkdexbot)',
    r'(?P<yisou>YisouSpider)',
    r'(?P<qq_url_manager>QQ-URL-Manager)',

}
SPIDER_PATTERN = re.compile(r'(%s)' % '|'.join(SPIDER_LIST), re.I)

SE_REF_LIST = [
    r'.*?\.(?P<baidu>baidu)\.com',
    r'www\.(?P<google>google)\.',
    r'.*?\.(?P<shenma>sm)\.cn',
    r'.*?\.(?P<haosou>haosou)\.com',
    r'.*?\.(?P<sogou>sogou)\.com',
]
SE_REF_PATTERN = re.compile(r'^https?://(%s)' % '|'.join(SE_REF_LIST))


def get_re_result(re_ptn, re_str, default=''):
    re_obj = re_ptn.search(re_str)
    if not re_obj:
        return default
    for key, val in re_obj.groupdict().items():
        if val:
            return key
    return default


def is_spider_referer(referer):
    if not referer:
        return False
    if get_re_result(SE_REF_PATTERN, referer, None):
        return True
    return False


reg_mobile_b = re.compile(r"(android|bb\\d+|meego).+mobile|avantgo|bada\\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od|ad)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino", re.I | re.M)
reg_mobile_v = re.compile(r"1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\\-(n|u)|c55\\/|capi|ccwa|cdm\\-|cell|chtm|cldc|cmd\\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\\-s|devi|dica|dmob|do(c|p)o|ds(12|\\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\\-|_)|g1 u|g560|gene|gf\\-5|g\\-mo|go(\\.w|od)|gr(ad|un)|haie|hcit|hd\\-(m|p|t)|hei\\-|hi(pt|ta)|hp( i|ip)|hs\\-c|ht(c(\\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\\-(20|go|ma)|i230|iac( |\\-|\\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\\/)|klon|kpt |kwc\\-|kyo(c|k)|le(no|xi)|lg( g|\\/(k|l|u)|50|54|\\-[a-w])|libw|lynx|m1\\-w|m3ga|m50\\/|ma(te|ui|xo)|mc(01|21|ca)|m\\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\\-2|po(ck|rt|se)|prox|psio|pt\\-g|qa\\-a|qc(07|12|21|32|60|\\-[2-7]|i\\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\\-|oo|p\\-)|sdk\\/|se(c(\\-|0|1)|47|mc|nd|ri)|sgh\\-|shar|sie(\\-|m)|sk\\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\\-|v\\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\\-|tdg\\-|tel(i|m)|tim\\-|t\\-mo|to(pl|sh)|ts(70|m\\-|m3|m5)|tx\\-9|up(\\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\\-|your|zeto|zte\\-", re.I | re.M)


def is_mobile_browser(user_agent):
    if not user_agent:
        return False
    if reg_mobile_b.search(user_agent):
        return True
    if reg_mobile_v.search(user_agent[0:4]):
        return True
    return False

###############################################################################
# UAParser
###############################################################################


class UAParser(object):
    """
    UserAgent解析器

    参数解释
        is_mobile_browser           是否是移动端
        is_weixin_browser           是否是微信浏览器
        platform                    客户端平台(android/ios/pc)
        is_android_platform
        is_ios_platform
        is_pc_platform
        is_spider                   是否是爬虫
        spider_name

        # 需要继承后自定义
        is_app                      是否是自开发的客户端
        is_ios_app
        is_android_app
        app_device_id               客户端设备id
        app_version                 客户端版本(字符串)
        app_version_id              客户端打包版本号(数字)
        app_version_num             客户端版本号
    """
    result_cache = LruCache(10000)

    def __init__(self, agent):
        self.agent = agent or ''
        self.result = {}
        try:
            self.parse()
        except:
            logging.error(traceback.format_exc())

    def __getattr__(self, key, default=None):
        try:
            return self.result[key]
        except (TypeError, AttributeError, KeyError):
            return default

    def __getitem__(self, key, default=None):
        try:
            return self.result[key]
        except (TypeError, AttributeError, KeyError):
            return default

    def parse(self):
        result = self.result_cache.get(self.agent)
        if result:
            self.result = result
            return
        result = self.result
        result.update(self.parse_platform_info())
        result.update(self.parse_weixin_browser_info())
        result.update(self.parse_spider_info())
        # result.update(self.parse_app_info())
        result.update(self.parse_mobile_browser_info())
        self.result_cache.put(self.agent, result)

    def ua_find(self, string):
        return (self.agent.find(string) > -1)

    def parse_weixin_browser_info(self):
        """
        is_weixin_browser
        """
        '''
            Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/6.5.18 NetType/WIFI Language/zh_CN
            Mozilla/5.0 (Linux; Android 6.0; HUAWEI GRA-UL00 Build/HUAWEIGRA-UL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043602 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/4G Language/zh_CN"
        '''
        ret = {}
        if self.ua_find('MicroMessenger'):
            ret['is_weixin_browser'] = True

            try:
                p = 'MicroMessenger/'
                start = self.agent.find(p)
                end = self.agent.find(' ', start)
                version = self.agent[start+len(p):end]
                ret['weixin_version'] = version
                ret['weixin_version_id'] = [int(i) for i in version.split('.')]
            except:
                pass
        return ret

    def parse_platform_info(self):
        """
        platform
        is_android_platform
        is_ios_platform
        is_pc_platform
        """
        ret = {}
        if self.ua_find('Android'):
            platform = 'android'
        elif self.ua_find('Mac OS') and not self.ua_find('Macintosh'):
            platform = 'ios'
        else:
            platform = 'pc'
        ret['platform'] = platform
        ret['is_%s_platform' % platform] = True
        return ret

    def parse_spider_info(self):
        """
        is_spider
        spider_name
        """
        ret = {}
        spider = get_re_result(SPIDER_PATTERN, self.agent, None)
        if not spider:
            return ret
        ret['is_spider'] = True
        ret['spider_name'] = spider
        return ret

    def parse_app_info(self):
        """
        is_app
        is_ios_app
        is_android_app
        """
        raise NotImplementedError

    def _get_app_version_num(self, version_string):
        """
            约定版本号有3段, 每段最大99
            version_string: 1.23.12
            return 12312
        """
        part = 3
        versions = [int(v) for v in version_string.split('.')]
        if len(versions) < part:
            versions += [0] * (part - len(versions))

        v = '%02d%02d%02d' % tuple(int(v) for v in versions)
        return int(v)

    def _get_ios_app_info(self):
        """
        app_device_id
        app_version
        app_version_id
        app_version_num
        """
        raise NotImplementedError

    def _get_android_app_info(self):
        """
        app_device_id
        app_version
        app_version_id
        app_version_num
        """
        raise NotImplementedError

    def parse_mobile_browser_info(self):
        ret = {
            'is_mobile_browser': is_mobile_browser(self.agent)
        }
        return ret
