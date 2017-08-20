#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import random
import re
import shutil
import urllib2

from user_agents import agents


class WallPaper(object):
    def __init__(self, url, timeout=None, max_retry_time=None, path=None, num=None, size=None):
        self.path = path if path else '{dir}/pic'. \
            format(dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.url = url
        self.headers = {
            'User-Agent': random.choice(agents)
        }
        self.timeout = timeout if timeout else 60
        self.max_retry_time = int(max_retry_time) if max_retry_time else 3
        self.num = int(num) if num else 10  # 0下载全量 其他下载指定数量
        self.size = size if size else 'small'

        # todo 经常检验不能连网站，但是浏览器可以连接
        # if not self.can_conn_site:
        #     self.raise_req_error(etype='connect')

        # 错误码及正则表达式常量
        self.ERROR_RESP_CODE = [400, 403, 404, 429, 500, 503, 504]
        _SMALL_PIC_REGEX = r'<img\ .*?src="(/images/wallpapers/\d+-\d+x\d+.jpg)"'
        _NEXT_PAGE_REGEX = r'<li class="nextPage"><a href="(/wallpapers/.*)">Next</a>'
        _BIG_PIC_SUB_REGEX = r'<a class="image" href="(.*?)" target="_blank">'
        _BIG_PIC_MAIN_REGEX = r'<p><a href="(/images/wallpapers/\d+-\d+x\d+.jpg)" class="download">'
        self._SMALL_PIC_PATTERN = re.compile(_SMALL_PIC_REGEX)
        self._BIG_PIC_SUB_PATTERN = re.compile(_BIG_PIC_SUB_REGEX)
        self._BIG_PIC_MAIN_PATTERN = re.compile(_BIG_PIC_MAIN_REGEX)
        self._NEXT_PAGE_PATTERN = re.compile(_NEXT_PAGE_REGEX)

    @property
    def can_conn_site(self):
        """判断能否和网站连通"""
        try:
            urllib2.urlopen(self.url, timeout=self.timeout)
            return True
        except urllib2.URLError:
            return False

    @property
    def download_big_pic(self):
        """是否下载大图"""
        return self.size == 'big'

    @staticmethod
    def raise_req_error(etype=None, url=None):
        """请求异常静态方法"""
        if etype == 'max_retry':
            raise urllib2.URLError('max_retry_error: fail request {url} '
                                   'too many time'.format(url=url))
        elif etype == 'connect':
            raise urllib2.URLError('can not connect the `wall paper` site check '
                                   'your browser open `http://www.socwall.com/` '
                                   'or retry later.')

    def get_resp(self, url, retry_time=0):
        """获取网页源代码"""
        req = urllib2.Request(url, headers=self.headers)
        response = urllib2.urlopen(req, timeout=self.timeout)

        if response.getcode() in self.ERROR_RESP_CODE:
            response = self.retry_req(retry_time=retry_time)

        return response

    def retry_req(self, retry_time):
        """重试 获取HTML"""
        if not self.can_conn_site:
            self.raise_req_error(etype='connect')
        elif retry_time > self.max_retry_time:
            self.raise_req_error(etype='max_retry', url=self.url)
        else:
            retry_time += 1
            return self.get_resp(self.url, retry_time=retry_time)

    def parse(self):
        """解析网页下载图片"""
        url = self.url
        url_pic_lst = []

        while len(url_pic_lst) < self.num:
            resp = self.get_resp(url)
            html = resp.read()

            if self.download_big_pic:
                url_pic_lst.extend(self._parse_big_pic(html))
            else:
                url_pic_lst.extend(self._parse_small_pic(html))

            url = self._parse_next_page(html)

            # 到达最后一页
            if not url:
                break

        self._download_pic(url_pic_lst[0: self.num])

    def _parse_small_pic(self, html):
        """解析下载小图"""
        page_url_lst = map(self._subsite_url, self._SMALL_PIC_PATTERN.findall(html))
        return page_url_lst

    def _parse_big_pic(self, html):
        """解析下载大图"""
        sub_big_pic_lst = map(self._subsite_url, self._BIG_PIC_SUB_PATTERN.findall(html))
        page_url_lst = map(self._parse_sub_big_pic, sub_big_pic_lst)
        return page_url_lst

    def _parse_sub_big_pic(self, url):
        """解析下载大图sub程序"""
        resp = self.get_resp(url)
        html = resp.read()

        return self._subsite_url(self._BIG_PIC_MAIN_PATTERN.findall(html)[0])

    def _parse_next_page(self, html):
        """获取下一页的url"""
        next_page = self._NEXT_PAGE_PATTERN.findall(html)[0]
        return self._subsite_url(next_page) if next_page else False

    def _subsite_url(self, part_url):
        """返回子页面完整url"""
        return self.url + part_url[1:]

    def _download_pic(self, url_lst):
        """下载图片"""
        self.create_folder()
        len_ = len(url_lst)
        curr_ = 0

        for url in url_lst:
            curr_ += 1
            print 'total picture num:{total_no}, downloading NO.{pic_no} picture\r'. \
                format(total_no=len_, pic_no=curr_),

            path = os.path.join(self.path, os.path.split(url)[1])
            with open(path, 'wb+') as f:
                f.write(self.get_resp(url).read())

        print 'finish download picture.'

    def create_folder(self):
        """创建文件夹"""
        if os.path.exists(self.path):
            self.del_path()
        os.makedirs(self.path)

    def del_path(self):
        """删除文件或文件夹"""
        if os.path.isfile(self.path):
            os.remove(self.path)
        elif os.path.isdir(self.path):
            shutil.rmtree(self.path)
