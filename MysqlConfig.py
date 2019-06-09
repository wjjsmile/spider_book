import pymysql
class DB(object):
    # 传入数据库名 参数
    def __init__(self,DB,HOST="127.0.0.1",PORT=3306,USER='root',charset='utf8'):
        self.HOST=HOST
        self.PORT=PORT
        self.USER=USER
        self.DB=DB
        self.charset=charset
        self.connect = pymysql.connect(host=self.HOST, port=self.PORT, user=self.USER, db=self.DB,
                                       charset=self.charset)
        print("mysql数据库连接成功....")
        self.cur = self.connect.cursor()