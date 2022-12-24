from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, Boolean, Time
from sqlalchemy.orm import relationship

from . import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(String(9), nullable=False, unique=True, primary_key=True)
    state = Column(String(20), default='START')

    subjects = relationship("Subject", back_populates="user", foreign_keys="Subject.user_id")
    subsubjects = relationship("SubSubject", back_populates="user", foreign_keys="SubSubject.user_id")
    additional_info = relationship("AdditionalInfo", back_populates="user", foreign_keys="AdditionalInfo.user_id")
    records = relationship("Records", back_populates="user", foreign_keys="Records.user_id")

    def __repr__(self):
        return f"<User({self.id} {self.name})>"


class AdditionalInfo(Base):
    __tablename__ = 'additional_info'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    user_id = Column(String(9), ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    type = Column(String(15))
    value = Column(String(20))

    user = relationship("User", back_populates="additional_info", uselist=False)


class Subject(Base):
    __tablename__ = 'subject'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    user_id = Column(String(9), ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(15), nullable=False)

    user = relationship("User", back_populates="subjects", uselist=False)
    subsubjects = relationship("SubSubject", back_populates="subject", foreign_keys="SubSubject.subject_id")
    records = relationship("Records", back_populates="subject", foreign_keys="Records.subject_id")

    def __repr__(self):
        return f"<Subject({self.id} {self.name})>"

    def __str__(self):
        return self.name


class SubSubject(Base):
    __tablename__ = 'sub_subject'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    subject_id = Column(Integer, ForeignKey("subject.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(String(9), ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(15), nullable=False)

    subject = relationship("Subject", back_populates="subsubjects", uselist=False)
    user = relationship("User", back_populates="subsubjects", uselist=False)
    records = relationship("Records", back_populates="subsubject", foreign_keys="Records.sub_subject_id")

    def __repr__(self):
        return f"<SubSubject({self.id} {self.name})>"


class Records(Base):
    __tablename__ = "records"

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    user_id = Column(String(9), ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    timedelta = Column(Time, nullable=False)
    date = Column(Date, nullable=False)
    description = Column(Text(300))
    subject_id = Column(Integer, ForeignKey("subject.id", ondelete="CASCADE"), nullable=False)
    sub_subject_id = Column(Integer, ForeignKey("sub_subject.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="records", uselist=False)
    subject = relationship("Subject", back_populates="records", uselist=False)
    subsubject = relationship("SubSubject", back_populates="records", uselist=False)

    def __repr__(self):
        return f"<SubSubject({self.id} {self.timedelta})>"
