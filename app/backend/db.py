from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import Column, Integer, String, Boolean

engine = create_engine('sqlite:///taskmanager.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()


class Base(DeclarativeBase):
	pass
