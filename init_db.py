from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
import models
import os
import dotenv

dotenv.load_dotenv()

print("INIT DB")

if (os.environ['INIT_TIMETABLE'] != "1"):
    print("NO INIT")
    exit()

login = os.getenv("POSTGRES_LOGIN")
passw = os.getenv("POSTGRES_PASS")
host = os.getenv("HOST")

print(login, host)

# engine = create_engine("postgresql+psycopg2://{}:{}@database".format(login, passw))
# # engine = create_engine("postgresql://user:hackme@localhost/store")
# session = sessionmaker(bind=engine)
# with engine.connect() as conn:
#     conn.execute("commit")
#     # Do not substitute user-supplied database names here.
#     conn.execute(f"CREATE DATABASE timetabledb")

engine = create_engine("postgresql+psycopg2://{}:{}@{}/timetabledb".format(login, passw, host))
# engine = create_engine("postgresql://user:hackme@localhost/store")
session = sessionmaker(bind=engine)  

models.Base.metadata.drop_all(engine)
models.Base.metadata.create_all(engine)
