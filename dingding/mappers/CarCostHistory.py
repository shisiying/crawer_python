# coding: utf-8
from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Carcosthistory(Base):
    __tablename__ = 'carcosthistory'

    approvalNumber = Column(String(255), primary_key=True)
    headlin = Column(String(255))
    approvalStatus = Column(String(255))
    approvalResult = Column(String(255))
    approvalTime = Column(DateTime)
    approvalFinshTime = Column(DateTime)
    initiatorsNumber = Column(String(255))
    initiatorsUserID = Column(String(255))
    initiatorsName = Column(String(255))
    initiatorsDepartment = Column(String(255))
    historicalApproverName = Column(String(255))
    approvalHistory = Column(String(255))
    currentProcessingName = Column(String(255))
    reviewsTake = Column(String(255))
    carNumber = Column(String(255))
    highwaySection = Column(String(255))
    mileage = Column(String(255))
    oilPrice = Column(String(255))
    cost = Column(String(255))
    instrumenBoardPhoto = Column(Text)
    receiptPhoto = Column(Text)
