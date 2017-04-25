# *_*coding:utf-8*_*
"""
程序入口
"""

from Tieba_Spider import html_downloader, url_manager, html_parser, store_table
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class SpiderMain(object):
    """
    玩家对客服正面、负面情感分析
    """
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.stroe = store_table.ResultMain("config.ini")

    def craw(self, root_urls):
        """
        如果有待爬取的url,取出一个,页面解析并写入
        """
        count = 1
        self.urls.add_new_url(root_urls)
        while self.urls.has_new_url():
            new_url = self.urls.get_new_url()

            print 'craw %d:%s' % (count, new_url)
            html_cont = self.downloader.download(new_url)
            if html_cont is None:
                continue
            try:
                new_urls, new_data = self.parser.parse(new_url, html_cont)
            except Exception,errorinfo:
                continue
            self.urls.add_new_urls(new_urls)
            self.stroe.collect_datas(new_data)
            if count == 2500:
                break
            count += 1

        self.stroe.output_table()


if __name__ == "__main__":
    root_url = "http://tieba.baidu.com/f?ie=utf-8&kw=%E5%A4%A7%E7%9A%87%E5%B8%9D"
    obj_spider = SpiderMain()
    obj_spider.craw(root_url)
