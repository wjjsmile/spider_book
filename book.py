import requests
from bs4 import BeautifulSoup
def get_bookinfo(selfurl):
    for page in range(1,41):    #每个月份书籍最多不超过40页
        url=selfurl+'/page/'+str(page)
        print("正在爬取的页面是:",url)
        response=requests.get(url)
        if response.status_code==404:
            print('一个月份书籍爬取完毕')
            break
        soup=BeautifulSoup(response.text,'lxml')
        all=soup.select('#primary > ul > li> div.content > h2 > a')
        for n in all:
            every_res=requests.get(n['href']).text
            so=BeautifulSoup(every_res,'lxml')
            book_name=so.select('#primary > h1')[0].get_text() #书籍名字
            book_clas=so.select('#primary > div.postinfo > div.left > a')
            book_clas=[a.get_text() for a in book_clas] #书籍类别
            book_class=''
            for n in book_clas:
                book_class+=n #这里列表形式无法插入数据库 故转成字符串形式
            book_photo=so.select('#content > p:nth-child(1)>img') #书籍封面
            if book_photo==[]:
                book_photo=''
            else:
                book_photo=book_photo[0]['src']
                #书籍封面这里有些页面会报错（可能无封面），应该在这里判断下.
            a=so.select('#content > div > p.downlink > strong > a')
            b=requests.get(a[0]['href'])
            v=BeautifulSoup(b.text,'lxml')
            p=v.select('body > div.list > a:nth-child(1)')
            pan_link=p[0]['href']  #网盘资源链接
            passwad=v.select('body > div:nth-child(4) > p:nth-child(7)')
            pan_passwd=passwad[0].get_text().split()[0].split('：')[-1] #网盘密码
            book_info={
                    'book_name':book_name,
                    'pan_link':pan_link,
                    'pan_passwd':pan_passwd,
                    'book_class':book_class,
                    'book_photo':book_photo
            }
            yield book_info 
