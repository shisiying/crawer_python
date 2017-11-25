# coding: utf-8
from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Servercheck(Base):
    __tablename__ = 'servercheck'

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
    approvalHistory = Column(Text)
    currentProcessingName = Column(String(255))
    reviewTake = Column(String(255))
    highwaySection = Column(String(255))
    serverName = Column(String(255))
    CPU = Column(String(255))
    RAM = Column(String(255))
    virusDB = Column(String(255))
    virusDBphoto = Column(Text)
    CPUphoto = Column(Text)
    presentTime = Column(String(255))
    presentSite = Column(String(255))
