# *_*coding:utf-8*_*
"""
链接管理
"""

class UrlManager(object):
    """
    判断是待爬取还是已爬取过的连接
    """
    def __init__(self):
        self.new_urls = []
        self.old_urls = []

    def add_new_url(self, url):
        """
        :param url:
        :return:
        """
        if url is None:
            return
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.append(url)

    def add_new_urls(self, urls):
        """
        :param urls:
        :return:
        """
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)

    def has_new_url(self):
        """
        :return:
        """
        return len(self.new_urls) != 0

    def get_new_url(self):
        """
        :return:
        """
        new_url = self.new_urls.pop(0)
        self.old_urls.append(new_url)
        return new_url

