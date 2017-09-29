# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class JijinDatum(Base):
    __tablename__ = 'jijin_data'

    id = Column(Integer, primary_key=True)
    code = Column(String(21), nullable=False)
    name = Column(String(100), nullable=False)
    grow_value = Column(String(10), nullable=False)
    grow_rate = Column(String(10), nullable=False)
    insert_date = Column(DateTime, nullable=False)
