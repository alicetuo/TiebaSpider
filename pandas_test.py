# *-*coding:utf-8*-*

import pandas as pd
import MySQLdb
import ConfigParser
from sqlalchemy import create_engine


class ResultMain(object):
    """
    config file read
    """

    def __init__(self, path,):
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
            self.conn = create_engine(
                "mysql+mysqldb://{0}:{1}@{2}:{3}/{4}?charset=utf8".format(
                    mysql_user,
                    mysql_pwd,
                    mysql_host,
                    mysql_port,
                    mysql_db),
                encoding='utf8',
                pool_recycle=10)
        except Exception as errorInfo:
            print 'configfile read failed!'
            print errorInfo
            raise

    def query_sql(self):
        """
        :return:
        """

        sql = "select * from python_test.test_copy"
        sql1 = 'select * from python_test.test'
        df = pd.read_sql(sql, self.conn, index_col='id')
        print df
        df1_info = pd.read_sql(sql1, self.conn, index_col='id')

        df.update(df1_info)

        # df.to_sql(con=self.conn, name='test_copy', if_exists='replace', index=False)


if __name__ == "__main__":
    obj = ResultMain("config.ini")
    obj.query_sql()
