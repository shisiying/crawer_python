# coding: utf-8
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Userinfo(Base):
    __tablename__ = 'userinfo'

    id = Column(Integer, primary_key=True)
    phone = Column(String(20), nullable=False)
    datetime = Column(String(20), nullable=False)
    amount = Column(Integer, nullable=False)
    num = Column(String(50), nullable=False)
    userid = Column(Integer, nullable=False)
    name = Column(String(10), nullable=False)
