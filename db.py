import dotenv
import os
import models
import itertools

from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import Session, sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy import select

import time

dotenv.load_dotenv()

class DBInstance():
    db_name = 'timetabledb'

    def __init__(self):
        login = os.getenv('POSTGRES_LOGIN')
        password = os.getenv('POSTGRES_PASS')
        host = os.getenv("HOST")
        
        self.engine = create_engine("postgresql+psycopg2://{}:{}@{}/{}".format(login, password, host, DBInstance.db_name))
        # self.engine = create_engine("postgresql://user:hackme@localhost/store")
        self.session = sessionmaker(bind=self.engine)

    def get_groups(self):
        with Session(bind=self.engine) as session:
            groups = session.query(models.Group).distinct(models.Group.group_name).all()
            group_names = list(map(lambda g: g.group_name, groups))
            return group_names
        
    def get_facultys(self):
        with Session(bind=self.engine) as session:
            stmt = select(models.Group.faculty).distinct()
            faculty_names = set(map(lambda g: g[0], session.execute(stmt).all()))
            return faculty_names

    def get_facultys_dict(self):
        with Session(bind=self.engine) as session:
            stmt = select(models.Group.faculty, models.Group.direction).group_by(models.Group.faculty, models.Group.direction)
            qry = session.execute(stmt).all()
            grouped = {}
            for k, v in qry:
                if k not in grouped:
                    grouped[k] = []
                grouped[k].append(v)

            return grouped

    def get_directions_dict(self):
        with Session(bind=self.engine) as session:
            stmt = select(models.Group.direction, models.Group.group_name).group_by(models.Group.direction, models.Group.group_name)
            qry = session.execute(stmt).all()
            grouped = {}
            for k, v in qry:
                if k not in grouped:
                    grouped[k] = []
                grouped[k].append(v)

            return grouped

    def get_timetable(self, group, table_kind, week_num):
        with Session(bind=self.engine) as session:
            #tic = time.perf_counter()
            subq1 = select(models.Group.id).where(models.Group.group_name == group).filter(models.Group.table_kind.contains(table_kind))
            stmt = select(models.Timetable.day, models.Timetable.table_json).where(models.Timetable.group_id.in_(subq1)).where(models.Timetable.week_num == week_num)
            qry = session.execute(stmt).all()
            table = list(map(lambda g: (g[0], g[1]), qry))
            #print(table)
            #toc = time.perf_counter()
            #print(toc-tic)
            return table

    def get_timetable_for_day(self, group, table_kind, week_num, day):
        with Session(bind=self.engine) as session:
            subq1 = select(models.Group.id).where(models.Group.group_name == group).filter(models.Group.table_kind.contains(table_kind))
            stmt = select(models.Timetable.day, models.Timetable.table_json).where(models.Timetable.group_id.in_(subq1)).where(models.Timetable.week_num == week_num).filter(models.Timetable.day.contains(day))
            qry = session.execute(stmt).all()
            table = list(map(lambda g: (g[0], g[1]), qry))
            return table

    def get_session(self, group):
        with Session(bind=self.engine) as session:
            subq1 = select(models.Group.id).where(models.Group.group_name == group)
            stmt = select(models.Session.addition, models.Session.exams).where(models.Session.group_id.in_(subq1))
            qry = session.execute(stmt).all()
            table = list(map(lambda g: (g[0], g[1]), qry))
            return table

# tic = time.perf_counter()
# db = DBInstance()
# db.get_session('АД-17-1с')
# toc = time.perf_counter()
# print(toc-tic)
