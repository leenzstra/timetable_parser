from datetime import datetime
from sqlalchemy import Table, Index, Integer, String, Column, Text, \
    DateTime, Boolean, PrimaryKeyConstraint, \
    UniqueConstraint, ForeignKeyConstraint
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()



class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    faculty = Column(String(100), nullable=False)
    direction = Column(String(100), nullable=False)
    group_name = Column(String(50), nullable=False)
    group_url = Column(String(256), nullable=False)
    table_kind = Column(String(100), nullable=False)

    def __init__(self, faculty, direction, group_name, group_url, table_kind) -> None:
        self.faculty = faculty
        self.direction = direction
        self.group_name = group_name
        self.group_url = group_url
        self.table_kind = table_kind

    def __repr__(self) -> str:
        return "{}, {}, {}, {}, {}".format(self.faculty, self.direction, self.group_name, self.group_url, self.table_kind)


class Timetable(Base):
    __tablename__ = 'timetables'

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer)
    day = Column(Integer, nullable=False)
    week_num = Column(Integer, nullable=False)
    table_json = Column(JSON, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(['group_id'], ['groups.id']),
    )

    def __init__(self, group_id, day, week_num, table_json) -> None:
        self.group_id = group_id
        self.day = day
        self.week_num = week_num
        self.table_json = table_json

    def __repr__(self) -> str:
        return "{}, {}, {}, {}".format(self.group_id, self.day, self.week_num, self.table_json)

class Session(Base):
    __tablename__ = 'session'

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer)
    addition = Column(String(100), nullable=True)
    exams = Column(JSON, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(['group_id'], ['groups.id']),
    )

    def __init__(self, group_id, addition, exams) -> None:
        self.group_id = group_id
        self.addition = addition
        self.exams = exams

    def __repr__(self) -> str:
        return "{}, {}, {}".format(self.group_id, self.addition, self.exams)