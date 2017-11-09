from crawl_fund.Spiders.Fund import SaveDb,getFundhtml
from sqlalchemy import create_engine
from crawl_fund.common.config import dburl
from sqlalchemy.orm import sessionmaker
from crawl_fund.mappers.Fund import Myfund
import csv
import pandas
if __name__=='__main__':
    #将抓取的数据文件入库
    # SaveDb()
    #写入csv文件当中
    # engine = create_engine(dburl, echo=True)
    # mysession=sessionmaker(bind=engine)()
    # result=mysession.query(Myfund).limit(10).all()
    # with open('./csvfiles/fund.csv','w',encoding='UTF-8') as file:
    #     writer=csv.writer(file)
    #     writer.writerow(['fcode','fname','NAV','ACCNAV','updatetime','fdate','DGR','DGV','fee'])
    #     for re in result:
    #         writer.writerow([re.fcode, re.fname, re.NAV, re.ACCNAV, re.updatetime, re.fdate, re.DGR, re.DGV, re.fee])
    #     file.close()
    pd=pandas.read_csv('./csvfiles/fund.csv',dtype={'fcode':pandas.np.str})
    result=pd.sort_values(by='NAV',ascending=False)
    print(result)