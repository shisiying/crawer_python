# _*_ coding: utf-8 _*_
__author__ = 'seven'
__date__ = '2017/11/17 20:51'

import json
import time
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from appdata.common.User import Userinfo


##target url
userinfourl = 'http://api.renrengyw.com/Api/Userv9/recomLog'

##your head
heads = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
}
## database connect
dburl="mysql+pymysql://root:[密码]@localhost/[数据库名字]?charset=utf8"
engine = create_engine(dburl,echo=True)
mysession = sessionmaker(bind=engine)()

##获取数据
def getdatafromuser(heads,userid,page):

    taget_url = userinfourl+"?p={}&logintype=1&userid={}".format(page,userid)
    header = {
        'User-Agent':heads['User-Agent'],
    }
    response = requests.get(url=taget_url,headers=header)
    return response.json()

##批量插入数据库
def insertdata(user_data,userid):
    datalist = []
    for user_data in user_data:
        user = Userinfo(phone=user_data['phone'],datetime=user_data['datetime'],amount=user_data['amount'],num=user_data['num'],userid=userid,name=user_data['name'])
        ##构造数据库实体化对象列表，方便批量插入
        datalist.append(user)
        # 批量插入
    mysession.add_all(datalist)  # 批量新增
    mysession.commit()
    mysession.close()

if __name__ == '__main__':
    ##genrate userid
    for userid in range(1,200000):
        print('userid')
        print(userid)
        ##set True
        flag = True
        ##set page =1
        page = 1
        ##genrate
        while flag:
            print('page:')
            print(page)
            return_data = getdatafromuser(heads=heads,userid=userid,page=page)
            ##data is empty,set page flag False
            if len(return_data['result']['list'])==0:
                flag = False
            else:
                ##page+1
                page =page +1
                ##数据批量入库
                insertdata(return_data['result']['list'],userid)
                ##延时3秒
                time.sleep(3)



