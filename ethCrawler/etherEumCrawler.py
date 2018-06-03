import requests
from bs4 import BeautifulSoup
import re
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from EthTradeList import Etherscantradelist

dburl="mysql+pymysql://root:hello2016@localhost/eth?charset=utf8"


##初始化数据库
engine = create_engine(dburl, echo=True)
mysession = sessionmaker(bind=engine)()

logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler("log.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

token ='0x0d0707963952f2fba59dd06f2b425ace40b492fe'
page =1

def sendRequest(token,page):
    targetUrl = 'https://etherscan.io/tokentxns?a={token}&ps=100&p={page}'.format(token=token,page=page)
    headers ={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
        'Accept':'*/*'
    }
    r= requests.get(targetUrl,headers=headers)
    if r.status_code==200:
        soup = BeautifulSoup(r.content,'lxml')
        return soup.find(name='table',class_='table table-hover')
    else:
        logger.info(targetUrl+' reposne is not 200')
        return False

def parseHtml(htmlData):


    if htmlData!=None:
        tradeRow = {}
        dataList = []

        for datatr in htmlData.find_all(name='tr')[1:]:
            tdRow = datatr.find_all(name='td')

            ###判断交易哈希是否存在
            res = mysession.query(Etherscantradelist).filter_by(
                txHash=tdRow[0].get_text().strip()).all()
            if len(res) != 0:
                continue

            tradeRow['txHash'] = tdRow[0].get_text().strip()
            tradeRow['age'] = tdRow[1].span['title'].strip()
            tradeRow['fromadress'] = tdRow[2].get_text().strip()
            tradeRow['to'] = tdRow[4].get_text().strip()
            tradeRow['value'] = tdRow[5].get_text().replace(',','').strip()
            tradeRow['token'] = re.match('/token/(.+)\?',tdRow[6].a['href']).group(1).strip()
            tradeRow['name'] = str(tdRow[6].get_text()).lower().strip()
            treadList = Etherscantradelist(**tradeRow)
            dataList.append(treadList)
    return dataList


def saveToDataBase(dataModel):
    mysession.add_all(dataModel)  # 批量新增
    mysession.commit()
    mysession.close()

def main():
    pages = 1000
    for page in range(1,pages+1):
        saveToDataBase(parseHtml(sendRequest(token,page)))

if __name__ == '__main__':
    main()