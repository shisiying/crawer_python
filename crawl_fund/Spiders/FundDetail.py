##获取基金详情页的总页数据
import csv
from threading import Thread,Lock

from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from crawl_fund.common.config import detailurl
import os
#获得基金稀详情页总的页数
def initSpider(detailurl):
    driver = webdriver.PhantomJS()
    ##访问基金详情页地址
    driver.get(detailurl)
    #找到下一页的按钮前面，就是总页数
    getPage_text=driver.find_element_by_id("pagebar").find_element_by_xpath("div[@class='pagebtns']/label[text()='下一页']/preceding-sibling::label[1]").get_attribute("innerHTML")
    ## 获得总的页数
    all_page=int(''.join(filter(str.isdigit,getPage_text)))
    ##获得基金编码
    fcode_text=driver.find_element_by_xpath("//*[@id='bodydiv']/div[8]/div[3]/div[1]/div[1]/div[1]/h4/a").get_attribute('innerHTML')
    fcode = ''.join(filter(str.isdigit, fcode_text))
    return (driver,all_page,fcode)
#获取每一页基金详情的数据并且写入文件当中
def getData(driver,pagelist,fcode,lock):
    for page in pagelist:
        ##加锁
        lock.acquire()
        ##第一页不需要处理，直接抓取数据写入文件保存当中
        if page==1:
            pass
        else:
            ##获取跳转输入框
            tonum=driver.find_element_by_id("pagebar").find_element_by_xpath("div[@class='pagebtns']/input[@class='pnum']")
            ##获取跳转框
            jumbtn=driver.find_element_by_id("pagebar").find_element_by_xpath("div[@class='pagebtns']/input[@class='pgo']")
            ##清除输入框的输入
            tonum.clear()
            ##为输入框赋值
            tonum.send_keys(str(page))
            ##点击跳转按钮
            jumbtn.click()
            ##判断是否出现cur的翻页的标志
            WebDriverWait(driver,20).until(lambda driver:driver.find_element_by_id("pagebar").find_element_by_xpath("div[@class='pagebtns']/label[@value={0} and @class='cur']".format(page))!=None)
        ##创建文件夹
        if not os.path.exists(os.path.abspath('..')+"\htmls\details"+"\{0}".format(fcode)):
            os.mkdir(os.path.abspath('..')+"\htmls\details"+"\{0}".format(fcode))
        ##写入文件当中
        with open(os.path.abspath('..')+"\htmls\details"+"\{0}\{1}.txt".format(fcode,page),'wb') as file:
            file.write(driver.find_element_by_id('jztable').get_attribute('innerHTML').encode('utf-8'))
            file.close()
            #释放锁
            lock.release()

##多线程开始抓取页面
def beginSpider(detailurl):
    ##获取到driver以及总的页数
    (driver,allpage,fcode)=initSpider(detailurl)
    #创建锁，防止线程不安全，因为延迟导致数据重复
    lock=Lock()
    #对页码进行分段
    page_r=range(1,int(allpage)+1)
    ##每个线程分配10页，构造分页列表
    step=10
    fenye_pagelist=[page_r[x:x+step] for x in range(0,len(page_r),step)]
    threadList=[]
    ##执行进程
    for r in fenye_pagelist:
        t=Thread(target=getData,args=(driver,r,fcode,lock))
        threadList.append(t)
        t.start()
    for t in threadList:
        t.join()##等待所有线程全部抓取完成才执行主线程

##使用beautifulsoup解析页面
def soupData(html,fcode):
    soup=BeautifulSoup(html,'html.parser')
    trs=soup.find("table").tbody.find_all('tr')
    result=[]
    for tr in trs:
        tds=tr.find_all("td")
        result.append({
            "fcode":fcode,
            "fdate":tds[0].get_text(),
            "NAV":tds[1].get_text(),
            "ACCNAV":tds[2].get_text(),
            "DGR":tds[3].get_text(),
            "pstate":tds[4].get_text(),
            "rstate":tds[5].get_text()
        })
    return result
##将解析之后的内容写入csv文件当中
def writeTocsc():
    datadir=os.path.abspath('..')+'/htmls/details'
    allpath_dir=os.listdir(datadir)
    ##遍历每个文件夹得文件
    for path_dir in allpath_dir:
        allpath_file=os.listdir(os.path.join(datadir,path_dir))
        ##读取每个文件
        ##临时数组，存储每一个基金解析完后的数据
        templist = []
        for path_file in allpath_file:
            #判断是否文件
            if os.path.isfile(os.path.join(os.path.join(datadir,path_dir),path_file)):
                with open(os.path.join(os.path.join(datadir,path_dir),path_file),'rb') as file:
                    fileCnt=file.read().decode('utf-8')
                    file.close()
                    templist=templist+soupData(fileCnt,path_dir)
        ##写入csv文件当中
        with open(os.path.abspath('..')+'\csvfiles\{0}.csv'.format(path_dir),'w',encoding='utf-8',newline='') as f:
            writer=csv.writer(f)
            writer.writerow(['fcode','fdate','NAV','ACCNAV','DGR','pstate','rstate'])
            for t_l in templist:
                writer.writerow([t_l['fcode'],t_l['fdate'],t_l['NAV'],t_l['ACCNAV'],t_l['DGR'],t_l['pstate'],t_l['rstate']])
            f.close()
        # ##重置临时存储数组
        templist = []
beginSpider(detailurl)
writeTocsc()
