# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class tradelist(Base):
    __tablename__ = 'tradelist'

    id = Column(Integer, primary_key=True)
    txHash = Column(String(70, 'utf8_unicode_ci'))
    blockHeight = Column(String(10, 'utf8_unicode_ci'))
    amount = Column(String(30, 'utf8_unicode_ci'))
    originatorAdress = Column(String(50, 'utf8_unicode_ci'))
    recevierAdress = Column(String(50, 'utf8_unicode_ci'))
    confirmTime = Column(DateTime)
    brokerage = Column(String(15, 'utf8_unicode_ci'))
