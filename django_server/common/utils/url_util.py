# -*- coding: utf-8 -*-
import re
import redis
import requests
import hashlib
import urllib.request, urllib.error, urllib.parse
from tld import get_tld
from urllib.parse import urljoin, urlparse
from html.parser import HTMLParser


def url_join(url, href):
    """
    格式化链接
    @param url : 原文链接
    @param href: 需要被格式化的链接
    @return    : 已格式化的链接
    """
    badUrlPrefix = ['javascript:']

    _href = href.split('#')[0]
    if _href.startswith('http://') or _href.startswith('https://'):
        return _href

    for b in badUrlPrefix:
        if _href.startswith(b):
            return None

    return urljoin(url, href)

def url_format_in_page(url, page):
    """
    格式化页面page中所有<a>标签中的href
    @param url : 该页url
    @param page: 页面内容
    @return    : 链接已转化的页面
    """
    def url_concat(matchobj):
        newUrl = url_join(url, matchobj.group(3))
        return '<a%shref="%s"%s>'%(matchobj.group(1),newUrl,matchobj.group(5))
    _page = re.sub(r'''<a(.*?)href\s*=\s*([\"\s]*)([^\"\']+?)([\"\s]+)(.*?)>''', url_concat, page, flags=re.S|re.I)
    return _page

def get_domain(url):
    p = urlparse(url)
    domain = p.netloc
    return domain

MOBILE_DOAMIN_RE = re.compile(r'^https?://(m|3g)\.')
MOBILE_HTML5_RE = re.compile(r'</\s*(header|footer)\s*>')
MOBILE_SCRIPT_RE = re.compile(r'<\s*script.*?src="[^"]*(allmobilize\.min\.js)[^"]*"', flags=re.I)
META_APPLICABLE_DEVICE_RE = re.compile(r'<meta\s+name="applicable-device"\s+content="([,\s\w+])"')
META_MOBILE_RE = re.compile(r'<\s*meta\s+name="(apple.*?|viewport|HandheldFriendly|MobileOptimized|x5-orientation|x5-fullscreen)"', flags=re.I)
def is_mobile_applicable(html, url=None):
    """
    页面是否在移动设备可阅读
    """
    if url:
        if MOBILE_DOAMIN_RE.match(url):
            return True
    m = META_MOBILE_RE.search(html)
    if m:
        return True
    m = META_APPLICABLE_DEVICE_RE.search(html)
    if m:
        devices = m.group(1)
        if devices.find('mobile') >= 0:
            return True
        return False
    if MOBILE_HTML5_RE.search(html):
        return True
    if MOBILE_SCRIPT_RE.search(html):
        return True
    # if html.find('<meta name="mobile-agent"'):
    #     return False
    return False

word_split_re = re.compile(r'(\s+)')
simple_url_re = re.compile(r'^https?://\[?\w', re.IGNORECASE)
simple_url_2_re = re.compile(r'^www\.|^(?!http)\w[^@]+\.(com|edu|gov|int|mil|net|org)$', re.IGNORECASE)
simple_email_re = re.compile(r'^\S+@\S+\.\S+$')
TRAILING_PUNCTUATION = ['.', ',', ':', ';', '.)', '"', '\'']
WRAPPING_PUNCTUATION = [('(', ')'), ('<', '>'), ('[', ']'), ('&lt;', '&gt;'), ('"', '"'), ('\'', '\'')]
def get_replace_urls(text, replace=None, url_format='<a href="{url}" rel="nofollow" target="_blank">{url}</a>'):
    """
    获取正文中的链接, 替换文中url
    若replace不为None, 则以(replace+递增数)替换正文中的url;
    若replace为None, 则替换为a标签, 默认标签形式为url_format
    @return (urls, text)
    """
    urls = []
    words = word_split_re.split(text)
    replace_i = 0
    for i, word in enumerate(words):
        if '.' in word or '@' in word or ':' in word:
            lead, middle, trail = '', word, ''
            for punctuation in TRAILING_PUNCTUATION:
                if middle.endswith(punctuation):
                    middle = middle[:-len(punctuation)]
                    trail = punctuation + trail
            for opening, closing in WRAPPING_PUNCTUATION:
                if middle.startswith(opening):
                    middle = middle[len(opening):]
                    lead = lead + opening
                # Keep parentheses at the end only if they're balanced.
                if (middle.endswith(closing)
                        and middle.count(closing) == middle.count(opening) + 1):
                    middle = middle[:-len(closing)]
                    trail = closing + trail
            url = None
            if simple_url_re.match(middle):
                url = middle
            elif simple_url_2_re.match(middle):
                url = 'http://%s' % middle
            elif ':' not in middle and simple_email_re.match(middle):
                local, domain = middle.rsplit('@', 1)
                try:
                    domain = domain.encode('idna').decode('ascii')
                except UnicodeError:
                    continue
                url = 'mailto:%s@%s' % (local, domain)
            mid = middle
            if url:
                urls.append(url)
                if replace is None:
                    mid = url_format.format(url=middle)
                else:
                    mid = '%s%s ' % (replace, replace_i)
                    replace_i += 1
            words[i] = '%s%s%s' % (lead, mid, trail)
    return (urls, ' '.join(words))


class RedirectURLParser:
    URL_PREFIX = 'REDIRECT_URL'
    B2C_SITES = ['newegg.cn', 'newegg.com', 'amazon.cn', 'amazon.com', 'amazon.co.jp', \
                 'jd.com', 'yixun.com', 'taobao.com', 'dangdang.com', 'yhd.com','sfbest.com', 'tmall.com', 'bestbuy.com', 'suning.com']

    def __init__(self):
        self._rs = redis.StrictRedis(db=3, password='smyfredis')
        #self._rs = redis.StrictRedis()
        self._htmlparser = HTMLParser()

    def try_to_get_url_from_cache(self, url):
        try:
            url = self._try_to_get_url_from_cache(url)
        except:
            url = False
        return url

    def _try_to_get_url_from_cache(self, url):
        name = hashlib.md5('%s-%s' % (self.URL_PREFIX, url)).digest()
        data = self._rs.hgetall(name)
        if data:
            if data['is_last']:
                return data['url']
            else:
                return self._try_to_get_url_from_cache(data['url'])
        else:
            return False

    def _cache_url(self, url, next_url, is_last=False):
        try:
            name = hashlib.md5('%s-%s' % (self.URL_PREFIX, url)).digest()
            self._rs.hset(name, 'url', next_url)
            self._rs.hset(name, 'is_last', is_last)
        except Exception as e:
            print(e)


    def _unescape_url(self, url):
        """
        对输入URL进行反转义 处理类似：http:&#x2F;&#x2F;www.disneystore.com&#x2
        """
        try:
            url = self._htmlparser.unescape(url)
        except Exception as e:
            print('unescape_url failed , url=%s')
            url = ''
        return  url

    def parse_redirect_url2(self, url):
        """
        根据抽出来的b2c_url 解析跳转后真正的产品链接, using urllib to get redirect url
        """
        url = self._unescape_url(url)
        found_url = self._try_to_get_url_from_cache(url)
        if found_url:
            return found_url
        opener = urllib.request.build_opener(urllib.request.HTTPRedirectHandler)
        request = opener.open(url)
        return request.url


    def parse_redirect_url(self, url):
        """
        根据抽出来的b2c_url 解析跳转后真正的产品链接
        """
        print('url', url)
        url = self._unescape_url(url)
        found_url = self.try_to_get_url_from_cache(url)
        if found_url:
            return found_url
        #mgpyh.com 暂时没法处理，所以先不转换
        if 'mgpyh.com' in url:
            self._cache_url(url, url, True)
            return  url
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:37.0) Gecko/20100101 Firefox/37.0',
                  'content-type': 'application/json'
                }
        try:
            r = requests.get(url, allow_redirects=True, headers=headers, timeout=2)
        except Exception as e:
            print(e)
            print(url)
            return
        if r.status_code == 200:
            if not r.history:
                try:
                    found_url = re.search(r'<meta\s*http-equiv="refresh"\s*content="\d+;url=(?P<url>[^"]+)"\s*/?\s*>', r.text, re.I).group('url')
                except:
                    #用来处理 类似dealmoon.com这种导向非国内主流b2c网站的情况
                    #TODO 优化，目前的做法如果走到这一步，目标网站的页面也被抓了下来，有点浪费带宽
                    self._cache_url(url, url, True)
                    return  url
                if found_url:
                    return self._handle_found_url(found_url, url)
                else:
                    print('fail to find url in r.text ')
            else:
                #found_url = r.history[-1].headers.get('location', '')
                found_url = r.url
                return self._handle_found_url(found_url, url)
        else:
            #TODO 异常处理
            print(r.status_code)
            return

    def _handle_found_url(self, found_url, url):
        if 'redirect.cps.yixun.com' in found_url or 's.click.taobao.com' in found_url or 'union.suning.com' in found_url:
            self._cache_url(url, found_url, False)
            return self.parse_redirect_url(found_url)
        else:
            domain = get_tld(found_url)
            print(domain)
            if domain in self.B2C_SITES:
                self._cache_url(url, found_url, True)
                return found_url
            else:
                parent_domain = get_tld(url)
                if parent_domain == domain:
                    print('%s is not in our vendor' % domain)
                    self._cache_url(url, found_url, True)
                    return found_url
                self._cache_url(url, found_url, False)
                return self.parse_redirect_url(found_url)

if __name__ == '__main__':
    # page = """
    #     <a href="/resadf"></a>
    #     <a href="http://bai.com"></a>
    #     <a class="test" href="http://bai.com"></a>
    # """
    # print url_format_in_page('http://www.11.com',page)

    #url = "http://www.czfxh.com/category/goods/ri_yong_bai_huo"
    #url = 'http://cn.dealmoon.com/exec/j/?d=398326'
    #url = 'http://www.tsdxb.com/77229.html'
    #url = 'http://cn.dealmoon.com/exec/j/?d=395496'
    #url= 'http://cn.dealmoon.com//exec/j/?d=407755'
    #url = 'http://cn.dealmoon.com/43-The-North-Face-Mens-Gordon-Anza-Fleece-Jacket/407755.htm'
    #url = 'http://www.huihui.cn/hui/24183138/redirect'
    # url = 'http://www.mgpyh.com/goods/r4raw'
    # parser = RedirectURLParser()
    # x = parser.parse_redirect_url(url)
    # print x
    # url = 'http://cn.dealmoon.com/exec/j/?d=400488'
    # print parser.parse_redirect_url2(url)
    print(get_replace_urls('www.baidu.com'))