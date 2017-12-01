import asyncio
import aiohttp
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import multiprocessing
import re

urls = ['https://www.toutiao.com/ch/news_hot/',
        'https://www.toutiao.com/ch/news_entertainment/',
        'https://www.toutiao.com/ch/news_finance/',
        'https://www.toutiao.com/ch/news_sports/',
        'https://www.toutiao.com/ch/news_tech/',
        ]

def configure_driver():
    opts = Options()
    opts.add_argument('--headless')
    prefs = {"profile.managed_default_content_settings.images": 2}
    opts.add_experimental_option("prefs", prefs)
    opts.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36')
    driver = webdriver.Chrome(chrome_options=opts,executable_path='D:\soft\chromedriver\chromedriver.exe')
    return driver

async def get_page_souse(url):
    '''
    :param pull_down_num: 下拉次数
    :param pixel: 每次下拉像素
    :return:
    '''
    pull_down_num = 300
    pixel = 200
    driver = configure_driver()
    driver.get(url)
    time.sleep(.5)
    entry = await get_info(0,driver.page_source)
    for i in range(pull_down_num):
        driver.execute_script('window.scrollTo(0,%s);'%pixel)
        pixel += 200
        entry = await get_info(entry,driver.page_source)
        time.sleep(.3)

async def get_info(entry,response):
    '''
    :param entry: 跳过的条目
    :param response: 网页源码
    :return:  这次条条目数量
    '''
    try:
        all_info = BeautifulSoup(response,'lxml').find('div',{'class':'wcommonFeed'}).find_all('li',{'class':'item'})
    except:
        return
    for li in all_info[entry:]:
        try:
            title = li.find('a',{'class':'link'}).text.replace(" ",'')
            href = li.find('a',{'class':'link'})['href']
        except AttributeError:
            continue
        else:

            if href.startswith('http://')|href.startswith('https://')|href.startswith('/api/'):
                continue
            else:
                href = 'https://www.toutiao.com/%s' % href
                await get_response(href)

    return len(all_info)

async def get_response(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            assert resp.status ==200
            await parse(await resp.text())

async def parse(response):
    catch_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    try:
        title = re.search('<title>(.+)</title>',response).group(1)
    except:
        title =None
    try:
        name = re.search('name:(.+)\,avat',response).group(1)
    except:
        name =None
    try:
        catogory = re.search('chineseTag:(.+)\,',response).group(1)
    except:
        catogory=None
    try:
        pub_time = re.search('time: \'(.+)\'',response).group(1)
    except:
        pub_time = None

    result = {
        'catch_date':catch_date,
        'title':title,
        'name':name,
        'catogory':catogory,
        'pub_time':pub_time
    }
    return result



def run(url):
    loop = asyncio.get_event_loop()
    tasks = [get_page_souse(url),]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

if __name__ == '__main__':
    p = multiprocessing.Pool(len(urls))
    for url  in urls:
        p.apply_async(run,args=(url,))
    p.close()
    p.join()
