from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import Config


engine = create_engine('sqlite:///flaskpro.db', connect_args={'check_same_thread': False})
Session = sessionmaker(bind=engine)
session= Session()
Base = declarative_base()