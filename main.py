from pnrpu_parser import parse_table_groups
import timetable_parser as tp
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
import os
import dotenv
import models
import json

dotenv.load_dotenv()

if (os.environ['PARSE_TIMETABLE'] != "1"):
    print("NO PARSING")
    exit()

print("PARSING", flush=True)
login = os.getenv("POSTGRES_LOGIN")
passw = os.getenv("POSTGRES_PASS")
host = os.getenv("HOST")

engine = create_engine(
    "postgresql+psycopg2://{}:{}@{}/timetabledb".format(login, passw, host))
# engine = create_engine("postgresql://user:hackme@localhost/store")
Session = sessionmaker(bind=engine)

# if (os.environ['PARSE_GROUPS'] == "1"):
print("PARSE GROUPS")
groups = parse_table_groups()

with Session() as session:
    session.query(models.Group).delete()
    session.commit()

with Session() as session:
    session.add_all(groups)
    session.commit()

with Session() as session:
    session.query(models.Timetable).delete()
    session.query(models.Session).delete()
    session.commit()
    

timetable_id = 1
session_id = 1
with Session() as session:
    groups = session.query(models.Group).all()
    print(groups)
    for g in groups:
        # print(g.table_kind)
        if 'сессия' in g.table_kind:
            ttable = tp.get_timetable_from_url(g.group_url, True)
            for t in ttable:
                session_model = models.Session(
                    g.id, t.addition, t.exams)
                session_model.id = session_id
                session_id += 1
                session.merge(session_model)
        elif ', )' not in g.table_kind:
            ttable = tp.get_timetable_from_url(g.group_url, False)
            for t in ttable:
                # json_tt = json.dumps(t.time_class_dict, ensure_ascii=False)
                # print(json_tt)
                table_model = models.Timetable(
                    g.id, t.day_name, t.week_num, t.time_class_dict)
                table_model.id = timetable_id
                timetable_id += 1
                session.merge(table_model)
        else:
            print("skipped", g.group_url)
    session.commit()
