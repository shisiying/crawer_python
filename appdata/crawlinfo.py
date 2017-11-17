#coding=utf-8
import json
import requests
userinfourl = ''
heads = {
    'Content-Type': '',
    'Content-Length': '',
    'Connection': '',
    'Accept-Encoding': '',
    'User-Agent': '',
    'UserToken': ''
}

def getdatafromuser(heads,userid,page):
    header = {
        'Content-Type':heads['Content-Type'],
        'Content-Length':heads['Content-Length'],
        'Connection':heads['Connection'],
        'Accept-Encoding':heads['Accept-Encoding'],
        'User-Agent':heads['User-Agent'],
        'UserToken': heads['UserToken']
    }
    params ={
       'logintype': 1,
        'userid': userid,
        'p' : page
    }
    requests.post(url=userinfourl,data=params,headers=header)
