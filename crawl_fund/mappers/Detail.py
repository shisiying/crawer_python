# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, Numeric, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Funddetail(Base):
    __tablename__ = 'funddetail'

    id = Column(Integer, primary_key=True)
    fcode = Column(String(10), nullable=False)
    fdate = Column(DateTime)
    NAV = Column(Numeric(10, 4))
    ACCNAV = Column(Numeric(10, 4))
    DGR = Column(String(20))
    pstate = Column(String(20))
    rstate = Column(String(20))
