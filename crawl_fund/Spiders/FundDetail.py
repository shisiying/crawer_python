##获取基金详情页的总页数据
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
    return (driver,all_page)
#获取每一页基金详情的数据并且写入文件当中
def getData(driver,page):
    datadir='./htmls/details'
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
    ##写入文件当中
    with open(os.path.abspath('..')+"\htmls\details"+"\{0}.txt".format(page),'wb') as file:
        file.write(driver.find_element_by_id('jztable').get_attribute('innerHTML').encode('utf-8'))
        file.close()

##多线程开始抓取页面
def beginSpider():
    pass
