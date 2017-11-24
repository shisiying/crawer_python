# coding: utf-8
from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Complainrecord(Base):
    __tablename__ = 'complainrecord'

    approvalNumber = Column(String(255), primary_key=True, nullable=False)
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
    customerName = Column(String(255))
    highwaySection = Column(String(255))
    list = Column(String(255), primary_key=True, nullable=False)
    complain = Column(String(255))
    photo = Column(String(255))
    accessory = Column(Text)
