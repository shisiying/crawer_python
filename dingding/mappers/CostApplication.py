# coding: utf-8
from sqlalchemy import Column, DateTime, String, Text,Integer
from sqlalchemy.ext.declarative import declarative_base
'''费用申请表'''

Base = declarative_base()
metadata = Base.metadata


class Costapplication(Base):
    __tablename__ = 'costapplication'

    costType = Column(String(255))
    approvalNumber = Column(String(255), primary_key=True, nullable=False)
    headlin = Column(String(255))
    approvalStatus = Column(String(255))
    approvalResult = Column(String(255))
    approvalTime = Column(DateTime)
    approvalFinshTime = Column(DateTime)
    initiatorsNumber = Column(String(255))
    initiatorsUserID = Column(String(255))
    initiatorsName = Column(String(255))
    InitiatorsDepartment = Column(String(255))
    historicalApproverName = Column(Text)
    approvalHistory = Column(Text)
    currentProcessingName = Column(String(255))
    reviewsTake = Column(String(255))
    companyName = Column(String(255))
    highwaySection = Column(String(255))
    type = Column(String(255))
    expensesStatement = Column(Integer, primary_key=True, nullable=False)
    projectName = Column(String(255))
    tradeMark = Column(String(255))
    specificationModels = Column(String(255))
    units = Column(String(255))
    amount = Column(String(255))
    unitPrice = Column(String(255))
    totalPrice = Column(String(255))
    stationName = Column(String(255))
    laneNumber = Column(String(255))
    useLocation = Column(String(255))
    remark = Column(String(255))
    photo = Column(Text)
    otherAccessory = Column(String(Text))
    applicaionReason = Column(String(255))
