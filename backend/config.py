from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
# import urllib.parse
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

username = os.getenv("username")
password = os.getenv("password")
# password = urllib.parse.quote(password)
port = os.getenv("port")
database = os.getenv("database")    
host = os.getenv("host")

DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/job_portal"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

# Create a Base class for declarative models
Base = declarative_base()

# Dependency function to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()