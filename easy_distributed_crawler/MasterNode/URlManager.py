# coding:utf-8
import pickle
import hashlib

class UrlManager(object):
    def __init__(self):
        ## 未爬取URL集合
        self.new_urls = self.load_progress('new_urls.txt')
        ## 已经爬取的URl集合
        self.old_urls = self.load_progress('old_urls.txt')

    ##判断是否有未爬取的Url
    def has_new_url(self):
        return self.new_url_size()!=0

    ##获取未爬取URl集合的大小
    def new_url_size(self):
        return len(self.new_urls)

    ## 获取未爬取的URl
    def get_new_url(self):
        new_url = self.new_urls.pop()
        m = hashlib.md5()
        m.update(new_url)
        self.old_urls.add(m.hexdigest()[8:-8])
        return new_url

    ## 新的url添加到未爬取的url集合中
    def add_new_url(self,url):
        if url is None:
            return
        m = hashlib.md5()
        m.update(url)
        url_md5 = m.hexdigest()[8:-8]
        if url not in self.new_urls and url_md5 not in self.old_urls:
            self.new_urls.add(url)

    ##将新的url添加到未爬取的url集合
    def add_new_urls(self,urls):

        if urls is None or len(urls)==0:
            return

        for url in urls:
            self.add_new_url(url)

    ##获取已爬取url集合大小
    def old_url_size(self):
        return len(self.old_urls)

    ##保存进度
    def save_progress(self,path,data):
        with open(path,'wb') as f:
            pickle.dump(data,f)

    ###从本地文件加载进度
    def load_progress(self,path):
        print('[+]从文件中加载进度:%s'% path)
        try:
            with open(path,'rb') as f:
                tmp = pickle.load(f)
                return tmp
        except:
            print("【!】无进度文件，创建： %s" % path)
        return set()