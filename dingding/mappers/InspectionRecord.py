# coding: utf-8
from sqlalchemy import Column, DateTime, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Inspectionrecord(Base):
    __tablename__ = 'inspectionrecord'

    type = Column(String(255))
    approvalNumber = Column(String(255), primary_key=True)
    headline = Column(String(255))
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
    reviewTake = Column(String(255))
    highwaySection = Column(String(255))
    recordType = Column(String(255))
    site = Column(String(255))
    otherSite = Column(String(255))
    temperature = Column(String(255))
    humidness = Column(String(255))
    jobContent = Column(String(255))
    foundFault = Column(String(255))
    presentTime = Column(String(255))
    presentSite = Column(String(255))
    photo = Column(String(255))
    photo2 = Column(String(255))
    photo3 = Column(String(255))
    photo4 = Column(String(255))
