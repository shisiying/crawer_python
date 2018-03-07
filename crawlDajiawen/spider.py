# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import csv
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030') #改变标准输出的默认编码


def getTopGoodsId(url):
    goodIdList = []
    driver = configure_driver()
    driver.get(url)
    goodInfo = BeautifulSoup(driver.page_source, 'lxml').find_all('a',class_='pic-link J_ClickStat J_ItemPicA')
    for goodRow in goodInfo:
        with open('goodid.txt', 'a') as infile:
                infile.write(goodRow['data-nid']+'\n')
        infile.close()

    ## 翻页
    nextpage = driver.find_element_by_css_selector('a[trace="srp_bottom_page2"]')
    nextpage.click()
    time.sleep(2)

    goodInfoPage = BeautifulSoup(driver.page_source, 'lxml').find_all('a',class_='pic-link J_ClickStat J_ItemPicA')
    for goodRowpage in goodInfoPage[:6]:
        with open('gooid.txt', 'a') as infile:
                infile.write(goodRowpage['data-nid']+'\n')
        infile.close()

def makeDjiawenUrl(goodId):
    dajiwenUrl = 'https://h5.m.taobao.com/wendajia/question2017.html?refId={}'.format(goodId)
    return dajiwenUrl

def configure_driver():
    opts = Options()
    opts.add_argument('--headless')
    prefs = {"profile.managed_default_content_settings.images": 2}
    opts.add_experimental_option("prefs", prefs)
    opts.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36')
    driver = webdriver.Chrome(chrome_options=opts, executable_path='D:\soft\chromedriver\chromedriver.exe')
    return driver

def get_page_source(url):

    driver = configure_driver()
    driver.get(url)
    driver.execute_script("document.getElementById('wdj').scrollTop=100000")
    time.sleep(2)
    parse(driver.page_source)

def parse(response):
    questionDiv = BeautifulSoup(response, 'lxml').find_all('div',class_="question mgb16")
    answerDiv = BeautifulSoup(response, 'lxml').find_all('div',class_="answer mgb22")
    goodsName = BeautifulSoup(response, 'lxml').find('div',class_="it-name").get_text()
    dataList=[]

    for row in zip(questionDiv,answerDiv):
        if len(row)!=0:
            dataList.append([goodsName,row[0].find_next('div',class_="title text").get_text(),row[1].find_next('p',class_="title text").get_text()])
    insertIntoCsv(dataList)

def insertIntoCsv(data):
    with open("dajiawen.csv", "a+",encoding='gb18030') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)
    csvfile.close()

def writeHeader():
    with open("dajiawen.csv", "a+", encoding='gb18030') as csvfile:
        writer = csv.writer(csvfile)
        # 先写入columns_name
        writer.writerow(["商品名字", "问题", "答案"])
    csvfile.close()

def run():
    writeHeader()
    with open('goodid.txt', 'r') as infile:
       for id in infile.readlines():
           dajiawenUrl = makeDjiawenUrl(id.strip())
           get_page_source(dajiawenUrl)
    infile.close()


##淘宝搜索销量优先的查询链接
top50url = 'https://s.taobao.com/search?q=%E5%86%AC%E8%99%AB%E5%A4%8F%E8%8D%89&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&sort=sale-desc'

run()