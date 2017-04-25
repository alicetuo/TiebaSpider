# -*- coding:utf-8 -*-

import MySQLdb
import ConfigParser
import pandas


class ResultMain(object):
    """
    config file read
    """

    def __init__(self, path):
        try:
            self.datas = []
            self.path = path
            self.cf = ConfigParser.ConfigParser()
            self.cf.read(self.path)
            mysql_host = self.cf.get("DBCONFIG", "host")
            mysql_user = self.cf.get("DBCONFIG", "user")
            mysql_pwd = self.cf.get("DBCONFIG", "passwd")
            mysql_port = self.cf.getint("DBCONFIG", "port")
            mysql_db = self.cf.get("DBCONFIG", "db")
            self.conn = MySQLdb.connect(
                host=mysql_host,
                user=mysql_user,
                passwd=mysql_pwd,
                port=mysql_port,
                db=mysql_db,
                init_command='set names utf8mb4')
            self.cursor = self.conn.cursor()
        except Exception as errorInfo:
            print 'configfile read failed!'
            print errorInfo
            raise

    def collect_datas(self, data):
        """
        :param data:
        :return:
        """
        if data is None:
            return
        self.datas.append(data)

    def output_table(self):
        """
        数据处理
        """
        try:
            for data in self.datas:
                try:
                    tmp_url = data["url"][0]
                    tmp_name = data["game_name"][0]
                    tmp_content = data["content"]
                    tmp_title = data["title"][0]
                    tmp_author = data["author"]
                    tmp_floor = data["floor"]
                    tmp_datetime = data["datetime"]
                except BaseException:
                    continue

                for i in range(len(tmp_content)):
                    insert_content = tmp_content[i]
                    insert_author = tmp_author[i]
                    insert_floor = tmp_floor[i]
                    insert_datetime = tmp_datetime[i]
                    insert_sql = "replace into spider_info (game_name,url_links,title,author,content,floor,datetime)" \
                                 "values('{0}','{1}','{2}','{3}','{4}','{5}','{6}');".format(tmp_name, tmp_url, MySQLdb.escape_string(tmp_title),
                                                                                             insert_author, MySQLdb.escape_string(insert_content), insert_floor, insert_datetime)
                    print insert_sql
                    self.cursor.execute(insert_sql)
                    self.conn.commit()

        except Exception as errorInfo:
            print errorInfo
            raise
