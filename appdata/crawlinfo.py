# _*_ coding: utf-8 _*_
__author__ = 'seven'
__date__ = '2017/11/17 20:51'

import demjson
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from appdata import User


##target url
userinfourl = ''

##your head
heads = {
    'Content-Type': '',
    'Content-Length': '',
    'Connection': '',
    'Accept-Encoding': '',
    'User-Agent': '',
    'UserToken': ''
}
## database connect
dburl="mysql+pymysql://root:[密码]@localhost/[数据库]?charset=utf8"
engine = create_engine(dburl,echo=True)
mysession = sessionmaker(bind=engine)()

##获取数据
def getdatafromuser(heads,userid,page):
    header = {
        'Content-Type':heads['Content-Type'],
        'Content-Length':heads['Content-Length'],
        'Connection':heads['Connection'],
        'Accept-Encoding':heads['Accept-Encoding'],
        'User-Agent':heads['User-Agent'],
        'UserToken': heads['UserToken']
    }
    params ={
       'logintype': 1,
        'userid': userid,
        'p' : page
    }
    response = requests.post(url=userinfourl,data=params,headers=header)

    return response.json()

##批量插入数据库
def insertdata(user_data):
    datalist = []
    for user_data in user_data:
        user = User(user_data['phone'],user_data['datetime'],user_data['amount'],user_data['num'])
        ##构造数据库实体化对象列表，方便批量插入
        datalist.append(user)
        # 批量插入
    mysession.add_all(datalist)  # 批量新增
    mysession.commit()
    mysession.close()

if __name__ == '__main__':
    ##genrate userid
    for userid in range(1,200000):
        ##set True
        flag = True
        ##set page =1
        page = 1
        ##genrate
        while flag:
            rturn_data = getdatafromuser(heads=heads,userid=userid,page=page)
            ##json change to python list
            return_data =demjson.decode(rturn_data,'utf-8')
            ##data is empty,set page flag False
            if len(rturn_data['result']['list'])==0:
                flag = False
            else:
                ##page+1
                page =page +1
                ##数据批量入库
                insertdata(return_data)


