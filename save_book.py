import requests
from bs4 import BeautifulSoup
import book
import time
from MysqlConfig import DB
from multiprocessing import Pool
db=DB("book")
def insert(Book_info):
    INSERT_sql = "INSERT INTO book_info(pan_link,book_name,pan_passwd,book_class,book_photo) VALUES('%s','%s','%s','%s','%s')"
    try:
        print(Book_info)
        db.cur.execute(INSERT_sql % (Book_info["pan_link"],Book_info["book_name"],Book_info["pan_passwd"],Book_info["book_class"],Book_info["book_photo"]))
        db.connect.commit()
        print("插入数据成功...")
    except Exception as e:
        print(e)
def main(selfurl):
    print('开始爬取',selfurl)
    for Book in book.get_bookinfo(selfurl):
        insert(Book)
if __name__ == '__main__':
    start=time.time()
    pool=Pool(15)
    url_index = 'http://mebook.cc/'
    req = requests.get(url_index)
    swd = BeautifulSoup(req.text, 'lxml')
    month = swd.select('#archives-dropdown-2 > option')[1:]
    selfurls=[n['value'] for n in month]  # 这里得到所有月份书籍的汇总
    pool.map(main,tuple(selfurls))
    pool.close()
    pool.join()
    end=time.time()
    print("共用时",end-start)

