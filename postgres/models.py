from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

Base = declarative_base()

resume_hobby = Table('resume_hobby', Base.metadata,
                     Column('resume_id', Integer, ForeignKey('resume.id'), primary_key=True),
                     Column('hobby_id', Integer, ForeignKey('hobby.id'), primary_key=True)
)


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    resume = relationship("Resume", uselist=False, back_populates="user")


class Resume(Base):
    __tablename__ = 'resume'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), unique=True, nullable=False)
    resume_title = Column(String(100))
    user = relationship("User", back_populates="resume")
    hobbies = relationship("Hobby", secondary=resume_hobby, back_populates="resumes")
    previous_jobs = relationship("PreviousJob", back_populates="resume")


class Hobby(Base):
    __tablename__ = 'hobby'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    resumes = relationship("Resume", secondary=resume_hobby, back_populates="hobbies")


class PreviousJob(Base):
    __tablename__ = 'previous_job'
    id = Column(Integer, primary_key=True, autoincrement=True)
    resume_id = Column(Integer, ForeignKey('resume.id'), nullable=False)
    city = Column(String(100), nullable=False)
    institution_name = Column(String(100), nullable=False)
    resume = relationship("Resume", back_populates="previous_jobs")
