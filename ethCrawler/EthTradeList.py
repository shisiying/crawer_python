# coding: utf-8
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Etherscantradelist(Base):
    __tablename__ = 'etherscantradelist'

    id = Column(Integer, primary_key=True)
    txHash = Column(String(70, 'utf8_unicode_ci'))
    age = Column(String(30, 'utf8_unicode_ci'))
    fromadress = Column(String(42, 'utf8_unicode_ci'))
    to = Column(String(42, 'utf8_unicode_ci'))
    value = Column(String(20, 'utf8_unicode_ci'))
    token = Column(String(42, 'utf8_unicode_ci'))
    name = Column(String(50, 'utf8_unicode_ci'))
