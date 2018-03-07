import requests
import os
from bs4 import BeautifulSoup
from multiprocessing import Process
import sys
import time
sys.setrecursionlimit(1000000) #例如这里设置为一百万

url = [
    'https://ns.postcc.us/htm_data/8/1711/2813398.html'
]

def getImageUrl(url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36',
    }
    time.sleep(2)
    html = requests.get(url,headers=header)
    html.encoding = 'gbk'
    Soup = BeautifulSoup(html.text,'lxml')
    title = Soup.title.get_text().split('-')[0].split(' ')[0]
    imgsrc = Soup.select('input[type="image"]')
    return {'title':title,'imgsrcs':imgsrc}

def downloadImg(imageLists,title,range_list):

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36',
    }
    if not os.path.exists('img/'+title):
        os.makedirs('img/'+title)
        print("创建文件夹--{}成功".format(title))
    for imglist in range_list:
        try:
            img = imageLists[imglist]
        except:
            pass
        print("正在下载图片"+str(imglist))
        img_response = requests.get(img.get('src'), stream=True, headers=header)
        with open('img/'+title + '/' + str(imglist) + '.jpg', 'wb') as img_file:
            img_file.write(img_response.content)
        print("下载图片" + str(imglist)+'成功')

def run(imageLists):
    blocks = range(1, len(imageLists['imgsrcs']) + 1)
    step = 10
    ##将数据分段，实行多线程下载
    range_lists = [blocks[x:x + step] for x in range(0, len(blocks), step)]
    processlist = []
    for range_list in range_lists:
        p = Process(target=downloadImg, args=(imageLists['imgsrcs'],imageLists['title'], range_list))
        processlist.append(p)
    for ps in processlist:
        ps.start()

if __name__ == '__main__':
    for ll in url:
        imglist = getImageUrl(ll)
        run(imglist)
