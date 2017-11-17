# _*_ coding: utf-8 _*_
import requests

def login(user_name,passwd):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'cookie': 'beans_dmp_done = 1;IPLOC = CN;SUV = 1710021626598866;reqtype = pc;gidinf = x099980109ee0ce6660204c290009a05135098259632;beans_freq = 1;lastpassport = 15626832124;jv = 4de511653f75dab9336e058a95ad09ef - qgxCfp3p1510458408529'
    }
    form_data = {
        'userid': user_name,
        'password': passwd,
        'persistentCookie': 1,
        'appid': 107405,
        'callback': 'passport401_cb1510458090735'
    }


s = requests.Session()
user_name = '15626832124'
passwd = 'hello2016'



