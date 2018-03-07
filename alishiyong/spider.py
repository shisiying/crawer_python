# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import csv
import re


def configure_driver():
    opts = Options()
    opts.add_argument('--headless')
    prefs = {"profile.managed_default_content_settings.images": 2}
    opts.add_experimental_option("prefs", prefs)
    opts.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36')
    driver = webdriver.Chrome(chrome_options=opts, executable_path='D:\soft\chromedriver\chromedriver.exe')
    return driver

def getShiyongItem():

    # shiyongUrl = 'https://try.taobao.com/#q=%E5%86%AC%E8%99%AB%E5%A4%8F%E8%8D%89&group=FIN'
    driver = configure_driver()
    # driver.get(shiyongUrl)
    # getItem(driver.page_source)

    ##翻页
    # totalPage = BeautifulSoup(driver.page_source, 'lxml').find('li', class_="pg-next").find_previous_sibling("li").get_text().strip()
    # totalPage = int(totalPage)+1
    # for page in range(1,8):
    #     shiyongPageUrl = 'https://try.taobao.com/#q=%E5%86%AC%E8%99%AB%E5%A4%8F%E8%8D%89&group=FIN&p={}'.format(page)
    #     driver.get(shiyongPageUrl)
    #     getItem(driver.page_source)
    shiyongPageUrl = 'https://try.taobao.com/#q=%E5%86%AC%E8%99%AB%E5%A4%8F%E8%8D%89&group=FIN&p={}'.format(page)
    driver.get(shiyongPageUrl)
    getItem(driver.page_source)

def getItem(response):
    ItemLinks = BeautifulSoup(response, 'lxml').find_all('a', class_="tb-try-ra-item-link")
    for link in ItemLinks:
        with open('itemLinks.txt', 'a') as infile:
            infile.write('https://try.taobao.com'+link['href'] + '\n')
        infile.close()

def getReportRow():
    with open('itemLinks.txt', 'r') as infile:
        for itemLink in infile.readlines():
            if '#tab-report' in itemLink:
                getReports(itemLink.strip())
    infile.close()

def getReports(itemLink):
    driver = configure_driver()
    driver.get(itemLink)
    writeReport(driver.page_source)

    ##ajax翻页
    hasNext = exitElement(driver,'li[class="pg-next"]')
    ###有翻页
    while hasNext!=False:
        ##点击下一页
        hasNext.click()
        time.sleep(2)
        writeReport(driver.page_source)

        ##判断是否是最后一页
        isLast = exitElement(driver,'li[class="pg-next pg-disabled"]')
        if isLast != False:
            ##若是则不翻页
            hasNext =False
        else:
            hasNext = exitElement(driver, 'li[class="pg-next"]')


def writeReport(response):
    ItemLinks = BeautifulSoup(response, 'lxml').find_all('a', class_="report")
    for link in ItemLinks:
        with open('reportLinks.txt', 'a') as infile:
            infile.write('https://try.taobao.com' + link['href'] + '\n')
        infile.close()

def exitElement(driver,select):
    try:
        selecttor = driver.find_element_by_css_selector(select)
        return selecttor
    except:
        return False

def getReportInfo():
    with open('reportLinks.txt', 'r') as infile:
        for reportLink in infile.readlines():
                reportRow = parseReport(reportLink.strip())
                insertCsv(reportRow)
    infile.close()

def parseReport(reportLink):
    driver = configure_driver()
    driver.get(reportLink)

    soup = BeautifulSoup(driver.page_source, 'lxml')

    ##商品名字
    goodName = soup.find('h1').get_text().strip()

    ##综合评分
    score = re.findall('\d+\.\d+',soup.find('span',class_='score-str').find_previous_sibling("span").get_text().strip())[0]

    lbllabel = soup.find_all('span',class_='lbl')
    costPerformance = None
    Effect = None
    Flavor = None
    Packing = None
    Occupation = None
    Constellation = None
    LikeType = None
    TastePreferences = None
    Age = None
    PersonalityLabel = None
    Gender =None

    for lblrow in lbllabel[5:]:

        if lblrow.get_text()=='性价比：':
            costPerformance = lblrow.find_next_sibling('span').find_next_sibling('span').get_text().strip()

        if lblrow.get_text() == '功效：':
            Effect = lblrow.find_next_sibling('span').find_next_sibling('span').get_text().strip()

        if lblrow.get_text() == '口味：':
            Flavor = lblrow.find_next_sibling('span').find_next_sibling('span').get_text().strip()

        if lblrow.get_text() == '包装：':
            Packing = lblrow.find_next_sibling('span').find_next_sibling('span').get_text().strip()

        if lblrow.get_text() == '职业：':
            Occupation = lblrow.find_next_sibling(text=True).strip()

        if lblrow.get_text() == '星座：':
            Constellation = lblrow.find_next_sibling(text=True).strip()

        if lblrow.get_text() == '性别：':
            Gender = lblrow.find_next_sibling(text=True).strip()

        if lblrow.get_text() == '喜好种类：':
            LikeType = lblrow.find_next_sibling(text=True).strip()

        if lblrow.get_text() == '口味喜好：':
            TastePreferences = lblrow.find_next_sibling(text=True).strip()

        if lblrow.get_text() == '年龄：':
            Age = lblrow.find_next_sibling(text=True).strip()

        if lblrow.get_text() == '个性标签：':
            PersonalityLabel = lblrow.find_next_sibling(text=True).strip()

    return [goodName,score,costPerformance,Effect,Flavor,Packing,Constellation,Gender,LikeType,Occupation,Age,TastePreferences,PersonalityLabel,reportLink]

def writeHeader():
    with open("report.csv", "a+", encoding='gb18030') as csvfile:
        writer = csv.writer(csvfile)
        # 先写入columns_name
        writer.writerow(["商品名字", "综合评分", "性价比",'功效','口味','包装','星座','性别','喜好种类','职业','年龄','口味喜好','个性标签','报告URL'])
    csvfile.close()

def insertCsv(row):
    with open("report.csv", "a+", encoding='gb18030') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(row)
    csvfile.close()

def run():
    getReportInfo()
run()

