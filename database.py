from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker





import os
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
SQLALCHEMY_DATABASE_URL = 'sqlite:///'+os.path.join(BASE_DIR,'baza.db?check_same_thread=False')
SECRET_KEY = 'SOME-SECRET-KEY'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True, pool_recycle=300)
# engine=create_engine('mysql+pymysql://root@localhost:3306/diagnosis')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def database():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
