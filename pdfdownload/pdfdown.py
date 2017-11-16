__author__ = 'seven'
import requests
import codecs
import json
import os
import re
'''
单进程下载
'''
header = {
    'Referer': 'http://www.jameshardie.co.nz/specifiers/cad-library',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

##将要获取的数据源写入文件当中
def writedatatojson():
    data_response = requests.get('http://cdnmaster.smartb.im/staging/td/jh/scripts/databoom.js',headers = header)
    datatable = re.search('my.dt=(.)*;my',data_response.text).group(0).split(';my')[0]
    datatable = json.loads(datatable[7:])
    with codecs.open('data.json', 'w') as file:
        file.write(json.dumps(datatable))
        file.close()
##从文件当中获取json数据
def getdatafromjson():
    with open('data.json') as json_file:
        data = json.load(json_file)
        return data
##下载文件
def download(category,file_name,pdf_url,dwg_url,gif_url):
    #新建文件夹
    if not os.path.exists(category):
        os.makedirs(category)
        print("创建文件夹成功")
    #下载pdf
    print("正在下载pdf")
    pdf_response = requests.get(pdf_url,stream=True,headers = header)
    with open(category+'/'+file_name+'.pdf','wb') as pdf_file:
        pdf_file.write(pdf_response.content)
    print("pdf下载完成")

    print("正在下载dwg")
    dwg_response = requests.get(dwg_url,stream=True,headers = header)
    with open(category+'/'+file_name + '.dwg', 'wb') as dwg_file:
        dwg_file.write(dwg_response.content)
    print("dwg下载完成")

    print("正在下载gif")
    gif_response = requests.get(gif_url,stream=True,headers = header)
    with open(category+'/'+file_name + '.gif', 'wb') as gif_file:
        gif_file.write(gif_response.content)
    print("gif下载完成")

if __name__ == '__main__':
    baseurl = 'http://cdnmaster.smartb.im/staging/td/jh/cadbim/'
    current_dir = os.getcwd()
    writedatatojson()
    datas = getdatafromjson()
    for data in datas[1:]:
        os.chdir(os.path.join(current_dir))
        category = data[-4]
        file_name = str(data[-1]).replace(category+'/','')
        down_url =str(data[-1])
        #pdf 下载链接
        pdf_url = '%s%s.pdf'%(baseurl,'pdf/'+down_url)
        #dwg下载链接
        dwg_url = '%s%s.dwg'%(baseurl,'dwg/'+down_url)
        #gif下载链接
        gif_url = '%s%s.gif'%(baseurl,'thumbs/'+down_url)
        download(category,file_name,pdf_url,dwg_url,gif_url)


