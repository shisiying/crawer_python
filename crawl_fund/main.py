'''
使用selenium模拟翻页
使用beautifulsoup解析网页
使用sqlacheme存储入库
多进程调用抓取方法process
使用manager进行进程数据共享
'''
from selenium import webdriver
from selenium.webdriver.support.ui import  WebDriverWait

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
    pass

if __name__=='__main__':
    # 初始化selenium
    driver = webdriver.PhantomJS()
    driver.get('http://fund.eastmoney.com/fund.html')
    totalpage=getPageTotal(driver)
    getData(driver,1,totalpage)




