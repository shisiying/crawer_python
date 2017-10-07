##获取基金详情页的总页数据
from selenium import webdriver
from crawl_fund.common.config import detailurl

def initSpider(detailurl):
    driver = webdriver.PhantomJS()
    ##访问基金详情页地址
    driver.get(detailurl)
    #找到下一页的按钮前面，就是总页数
    getPage_text=driver.find_element_by_id("pagebar").find_element_by_xpath("div[@class='pagebtns']/label[text()='下一页']/preceding-sibling::label[1]").get_attribute("innerHTML")
    print(getPage_text)

initSpider(detailurl)