# coding: utf-8
from sqlalchemy import Column, Date, DateTime, String, Text
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Dailyworkreport(Base):
    __tablename__ = 'dailyworkreport'

    approvalNumber = Column(String(255), primary_key=True)
    headline = Column(String(255))
    approvalStatus = Column(String(255))
    approvalResult = Column(String(255))
    approvalTime = Column(DateTime)
    approvalFinishTime = Column(DateTime)
    initiatorsNumber = Column(String(255))
    initiatorsUserID = Column(String(255))
    initiatorsName = Column(String(255))
    initiatorsDepartment = Column(String(255))
    historicalApproverName = Column(String(255))
    approverHistory = Column(Text)
    currentProcessingName = Column(String(255))
    reviewTake = Column(String(255))
    highwaySection = Column(String(255))
    date = Column(Date)
    weather = Column(String(255))
    temperature = Column(String(255))
    rate = Column(String(255))
    ratePhoto = Column(Text)
    workGoing = Column(String(255))
    unfinshedWork = Column(String(255))
    importantEvent = Column(String(255))
    photo = Column(Text)
    accessory = Column(Text)
