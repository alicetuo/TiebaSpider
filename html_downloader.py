# *_*coding:utf-8*_*

import urllib2
import sys
import webbrowser as web
import requests

reload(sys)
sys.setdefaultencoding('utf8')


class HtmlDownloader(object):
    """
    拉取html页面，并返回
    """
    def download(self, url):
        """
        :param self:
        :param url:
        :return:
        """
        try:
            if url is None:
                return None
            r = requests.get(url, timeout=5)
            r.raise_for_status()
            r.encoding = 'utf8'
            return r.text
        except:
          return "产生异常"
