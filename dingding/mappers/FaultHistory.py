# coding: utf-8
from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Faulthistory(Base):
    __tablename__ = 'faulthistory'

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
    historicalApproverName = Column(Text)
    approvalHistory = Column(Text)
    currentProcessingName = Column(String(255))
    reviewTake = Column(String(255))
    highwaySection = Column(String(255))
    controalStation = Column(String(255))
    Station = Column(String(255))
    lane = Column(String(255))
    faultType = Column(String(255))
    faultPhenomenon = Column(String(255))
    otherPhenomenon = Column(String(255))
    result = Column(String(255))
    presentTime = Column(String(255))
    presentSite = Column(String(255))
    photo = Column(Text)
    photo2 = Column(Text)
    photo3 = Column(Text)
    photo4 = Column(Text)
