from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

#create engine
engine=create_engine(DATABASE_URL)

#create session
sessionLOCAL=sessionmaker(autocommit=False,autoflush=False,bind=engine)

#base class
Base=declarative_base()
