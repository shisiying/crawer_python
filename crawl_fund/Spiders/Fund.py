# -*- coding: utf-8 -*-
'''
使用selenium模拟翻页
使用beautifulsoup解析网页
使用sqlacheme存储入库
'''
import os
from datetime import datetime
from crawl_fund.common.config import dburl
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from crawl_fund.mappers.Fund import Myfund
from crawl_fund.common.function import getText
engine = create_engine(dburl,echo=True)

##获取基金每一页的数据，并且写入到文件当中
def getFundhtml():
    # 初始化selenium
    driver = webdriver.PhantomJS()
    driver.get('http://fund.eastmoney.com/fund.html')
    totalpage = getPageTotal(driver)
    getData(driver, 1, totalpage)
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
        with open(os.path.abspath('..')+"\htmls\{0}.txt".format(x),'wb') as f:
            ##只抓取表格部分，方便beautifulsoup解析数据
            f.write(driver.find_element_by_id("tableDiv").get_attribute("innerHTML").encode('utf-8'))
            f.close()

def SoupFundData(html):
    #读取htmls文件夹的每一个文件
        soup=BeautifulSoup(html,'html.parser')
        fCodes = soup.find("table", id="oTable").tbody.find_all("td", "bzdm")  # 基金编码集合
        fDate = soup.find("table", id="oTable").thead.find("td", colspan='2').get_text()  # 基金日期
        ##获取基金代码
        result=[]
        for fCode in fCodes:
            result.append({"fcode": fCode.get_text()
                              , "fname": fCode.next_sibling.find("a").get_text()
                              , "NAV": getText(fCode.next_sibling.next_sibling)
                              , "ACCNAV": getText(fCode.next_sibling.next_sibling.next_sibling)
                              , "DGV": fCode.parent.find("td", "rzzz").get_text()  # 日增长值，取fcode所在的父元素(tr)，然后find
                              , "DGR": fCode.parent.find("td", "rzzl").get_text()  # 日增长率
                              , "fee": getText(fCode.parent.find("div", "rate_f"))  # 费率,注意这里不要定位到A元素,有的基金没有这个div，所以要做判断
                              , "updatetime": datetime.now().isoformat(sep=' ', timespec="seconds")
                              , "fdate": fDate}
                          )
       ##返回每一页的数据集
        return result

def SaveDb():
    ##抓取文件的路径
    datadir='./htmls'
    allpath=os.listdir(datadir)
    ##初始化数据库连接
    mysession = sessionmaker(bind=engine)()
    dataList=[]
    for filename in allpath:
        if os.path.isfile(os.path.join(datadir, filename)):
            ##读取抓取的文本文件
            with open(os.path.join(datadir,filename), "r",encoding='UTF-8') as file:
                fileCnt = file.read()
                file.close()
            resultSet=SoupFundData(fileCnt)
            for result in resultSet:
                myfund = Myfund(**result)
                ##构造数据库实体化对象列表，方便批量插入
                dataList.append(myfund)
    #批量插入
    mysession.add_all(dataList)  # 批量新增
    mysession.commit()
    mysession.close()






