from sqlalchemy import create_engine
import urllib.parse
from sqlalchemy.orm import sessionmaker

password = "sai@1404"

encoded_password = urllib.parse.quote(password)

db_url = f"postgresql://postgres:{encoded_password}@localhost:9999/telusko"
engine = create_engine(db_url)
session= sessionmaker(autocommit=False,autoflush=False,bind=engine)