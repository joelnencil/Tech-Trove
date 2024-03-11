
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql://joelnencil:123456@localhost:5432/postgres"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

class UserDetails(Base):
    __tablename__ = "users"

    email = Column(String, primary_key=True, index=True)
    password = Column(String)

Base.metadata.create_all(bind=engine)