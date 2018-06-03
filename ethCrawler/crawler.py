import requests
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from TradeList import tradelist

import re

dburl="mysql+pymysql://root:123@localhost/eth?charset=utf8"


##初始化数据库
engine = create_engine(dburl, echo=True)

def sendPost(page):

    payload ={'address':'0xc38e2669cc249748eab2c86e9e371481a1919293','currency':'ETH','page':page,'pageSize':20}
    headers = {
                'Host': 'scan-api.spancer.cn',
                'Accept': 'application/json, text/plain, */*',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36C',
                'Content-Type': 'application/json;charset=UTF-8',
                'Accept-Language':'zh-CN,zh;q=0.9',
                'Accept-Encoding':'gzip, deflate',
                'Origin':'http://www.qukuai.com',
                }
    r = requests.post('http://scan-api.spancer.cn//v1/address/getInfo',data=json.dumps(payload),headers=headers)
    result = json.loads(r.text)

    if result['code']==200 and len(result['data']['tradeList']):
        return result['data']['tradeList']
    else:
        return None
def saveData(data):
    ##批量插入
    ##初始化数据库连接
    mysession = sessionmaker(bind=engine)()
    dataList = []
    tradeRow={}
    for item in data:

        ###判断交易哈希是否存在
        res = mysession.query(tradelist).filter_by(
            txHash=item['txHash']).all()
        if len(res) != 0:
            continue
        if int(item['confirmCount'])>5 and float(re.split('[+-]',item['amount'])[1])>0:
            tradeRow['txHash'] = item['txHash']
            tradeRow['blockHeight'] = item['blockHeight']
            tradeRow['amount'] = item['amount']
            tradeRow['confirmTime'] = item['confirmTime']
            tradeRow['originatorAdress'] = item['inList'][0]['address']
            tradeRow['recevierAdress'] = item['outList'][0]['address']
            tradeRow['brokerage'] = item['brokerage']
            treadList = tradelist(**tradeRow)
            dataList.append(treadList)

    mysession.add_all(dataList)  # 批量新增
    mysession.commit()
    mysession.close()


def main():
    for page in range(1,9999):
        data = sendPost(page)
        if data!=None:
            saveData(data)
        else:
            exit()

main()