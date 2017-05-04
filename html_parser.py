# *_*coding:utf-8*_*

from bs4 import BeautifulSoup
import re
import urlparse
import json


class HtmlParser(object):
    """
    xx
    """
    def _get_new_urls(self, page_url, soup):
        """
        找出根路径以及待解析的URL链接
        """
        new_urls = []
        links = soup.find_all('a', attrs={"class": re.compile(r"(j_th_tit)|(pagination-item)")}
                              , href=re.compile(r"/f\?+\w|/p/\d"))

        replay_links = soup.find_all('a', href=re.compile(r"/p/\d+\?+pn=*"))

        for link in links:
            new_url = link['href']
            new_full_url = urlparse.urljoin(page_url, new_url)
            print new_full_url
            new_urls.append(new_full_url)

        for link in replay_links:
            sub_new_url = link['href']
            sub_new_full_url = urlparse.urljoin(page_url, sub_new_url)
            if sub_new_full_url not in new_urls:
                new_urls.append(sub_new_full_url)
        return new_urls

    def _get_new_data(self, page_url, soup):
        """
        :param page_url:
        :param soup:
        :return: store data
        """
        res_data = {}
        # root_url= re.findall(r"http://tieba.baidu.com/f\?+\w", page_url)
        # print root_url
        # if not res_data.has_key("rooturl"):
        #     res_data["rooturl"] = [root_url]
        # else:
        #     res_data["rooturl"].append(root_url)
        # print res_data

        if re.match(r"http://tieba.baidu.com/p/\d", page_url):
            try:
                authors = soup.find_all('a', attrs={"class": re.compile("(p_author_name)|(j_user_card)")})
                summary_content = soup.find_all('div', attrs={"id": re.compile("post_content_+\d")})
                game_name = soup.find('a', attrs={"class": re.compile("(card_title_fname)|(plat_title_h3)")})
                title_node = soup.find('title')

                # other_info & other_info 取时间和楼层，解析方式不同
                other_info = soup.find_all("div", attrs={"class": re.compile("(l_post)|(j_l_post)|(l_post_bright)")})
                other_info1 = soup.find_all('span', class_="tail-info")
                if "game_name" not in res_data:
                    res_data["game_name"] = [game_name.get_text().strip()]
                else:
                    res_data["game_name"].append(game_name.get_text().strip())
                if "url" not in res_data:
                    res_data["url"] = [page_url]
                else:
                    res_data["url"].append(page_url)

                if "title" not in res_data:
                    res_data['title'] = [title_node.get_text().strip()]
                else:
                    res_data["title"].append(title_node.get_text().strip())

                for author in authors:
                    if "author" not in res_data:
                        res_data["author"] = [author.get_text().strip()]
                    else:
                        res_data["author"].append(author.get_text().strip())

                for new_content in summary_content:
                    if "content" not in res_data:
                        res_data["content"] = [new_content.get_text().strip()]
                    else:
                        res_data["content"].append(new_content.get_text().strip())
                for dates in other_info1:
                    if re.match(r"^[1-2][0-9][0-9][0-9]-([1][0-2]|0?[1-9])-([12][0-9]|3[01]|0?[1-9])"
                                r" ([01][0-9]|[2][0-3]):[0-5][0-9]$", dates.get_text()):
                        if "datetime" not in res_data:
                            res_data["datetime"] = [dates.get_text().strip()]
                        else:
                            res_data["datetime"].append(dates.get_text().strip())

                    elif re.match(r"\d", dates.get_text()):
                        if "floor" not in res_data:
                            res_data["floor"] = [dates.get_text().strip()]
                        else:
                            res_data["floor"].append(dates.get_text().strip())

                # for detail in other_info:
                #     text = json.loads(detail["data-field"])
                #     date_info = text["content"]
                #     if not res_data.has_key("datetime"):
                #         res_data["datetime"] = [date_info['date']]
                #     else:
                #         res_data["datetime"].append(date_info["date"])
                #
                #     if not res_data.has_key("floor"):
                #         res_data["floor"] = [date_info['post_index']]
                #     else:
                #         res_data["floor"].append(date_info["post_index"])
                return res_data
            except Exception, e:
                print e

    def parse(self, page_urls, html_cont):
        """
        :param page_urls:
        :param html_cont:
        :return:urls & res_data
        """
        if page_urls is None or html_cont is None:
            return
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        new_urls = self._get_new_urls(page_urls, soup)
        new_data = self._get_new_data(page_urls, soup)
        return new_urls, new_data
