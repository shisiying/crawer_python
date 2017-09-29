# -*- coding: utf-8 -*-
'''
使用selenium模拟翻页
使用beautifulsoup解析网页
使用sqlacheme存储入库
多进程调用抓取方法process
使用manager进行进程数据共享
'''
from selenium import webdriver
from selenium.webdriver.support.ui import  WebDriverWait
from bs4 import BeautifulSoup
import os
import time
from sqlalchemy import Column,String,Integer,create_engine
from sqlalchemy.orm import sessionmaker
from crawl_fund.jijin import JijinDatum



##获取总的页数
def getPageTotal(driver):
    getTotalPage_text = driver.find_element_by_id("pager").find_element_by_xpath("span[@class='nv']").text
    total_page = ''.join(filter(str.isdigit, getTotalPage_text))  ##得到一共是多少页数
    return int(total_page)
##获取分页，并将每一页的数据写进htmls文件夹中
def getData(driver,start,end):
    for x in range(start,end+1):
        tonum=driver.find_element_by_id("tonum")#得到跳转输入框
        jumbtn=driver.find_element_by_id("btn_jump")#跳转得到按钮
        tonum.clear()
        tonum.send_keys(str(x))#发送跳转页数
        jumbtn.click()#模拟点击确定跳转按钮
        #判断找到某页成功的标志
        WebDriverWait(driver,30).until(lambda driver:driver.find_element_by_id('pager').find_element_by_xpath("span[@value={0} and @class!='end page']".format(x)).get_attribute(
            'class').find("at") != -1)
        #写入文件中
        with open("./htmls/{0}.txt".format(x),'wb') as f:
            ##只抓取表格部分，方便beautifulsoup解析数据
            f.write(driver.find_element_by_id("tableDiv").get_attribute("innerHTML").encode('utf-8'))
            f.close()
def Soup():
    #读取htmls文件夹的每一个文件
    for filename in os.listdir(os.getcwd()+'/htmls'):
        with open(os.getcwd()+'/htmls/'+filename,'r',encoding='UTF-8') as file:
                print(filename)
                soup=BeautifulSoup(file.read(),'html.parser')
                ##获取基金代码
                code=[code.get_text() for code in soup.find_all('td',class_='bzdm')]
                name=[name.contents[0].contents[0].get_text() for name in soup.find_all("td",class_='tol')]
                ##基金增长值和增长是会改变的,变为black,green，所以合并这三种类型，就涵盖了全部
                group_value_red=[group_value.get_text() for group_value in  soup.find_all("td",class_='rzzz red')]
                group_value_black =[group_value.get_text() for group_value in soup.find_all("td", class_='rzzz black')]
                group_value_green = [group_value.get_text() for group_value in soup.find_all("td", class_='rzzz green')]
                group_value=group_value_red+group_value_black+group_value_green

                group_rate_red1=[group_rate.get_text() for group_rate in soup.find_all("td", class_='rzzl bg red')]
                group_rate_red2 = [group_rate.get_text() for group_rate in soup.find_all("td", class_='bg rzzl red')]
                group_rate_black=[group_rate.get_text() for group_rate in soup.find_all("td", class_='bg rzzl black')]
                group_rate_green = [group_rate.get_text() for group_rate in soup.find_all("td", class_='bg rzzl green')]
                group_rate=group_rate_red1+group_rate_red2+group_rate_black+group_rate_green

                for count in range(0,len(code)):
                    jijin_code = code[count]
                    jijin_name = name[count]
                    jijin_group_value = group_value[count]
                    jijin_group_rate = group_rate[count]
                    data = {'code': jijin_code, 'name': jijin_name, 'grow_value': jijin_group_value,
                            'grow_rate': jijin_group_rate}
                    inserDb(data)
def inserDb(data):
    engine = create_engine('mysql+pymysql://root:hello2016@localhost/jijin?charset=utf8')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    newfuns=JijinDatum(code=data['code'],name=data['name'],grow_value=data['grow_value'],grow_rate=data['grow_rate'],insert_date=time.strftime('%Y-%m-%d',time.localtime(time.time())))
    session.add(newfuns)
    session.commit()
    session.close()

if __name__=='__main__':
    #初始化selenium
    driver = webdriver.PhantomJS()
    driver.get('http://fund.eastmoney.com/fund.html')
    totalpage=getPageTotal(driver)
    getData(driver,1,totalpage)
    Soup()




