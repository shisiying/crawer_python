# coding: utf-8
from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Importantevent(Base):
    __tablename__ = 'importantevent'

    approvalNumber = Column(String(255), primary_key=True)
    headline = Column(String(255))
    approvalStatus = Column(String(255))
    approvalResult = Column(String(255))
    approvalTime = Column(DateTime)
    approvalFinishTime = Column(DateTime)
    initiatorsNumber = Column(String(255))
    initiatorsUserID = Column(String(255))
    initiatorsName = Column(String(255))
    InitiatorsDepartment = Column(String(255), nullable=False)
    historicalApproverName = Column(Text)
    approvalHistory = Column(Text)
    currentProcessingName = Column(String(255))
    reviewTake = Column(String(255))
    department = Column(String(255))
    highwaySection = Column(String(255))
    eventTime = Column(String(255))
    FinshTime = Column(String(255))
    influenceTime = Column(String(255))
    eventSite = Column(String(255))
    eventType = Column(String(255))
    eventDescription = Column(String(255))
    influence = Column(String(255))
    method = Column(String(255))
    loss = Column(String(255))
    lossCapital = Column(String(255))
    photo = Column(Text)
    accessory = Column(String(255))
