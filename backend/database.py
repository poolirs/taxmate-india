from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
Base = declarative_base()
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://ravipooli:Welcome123#@localhost:5432/taxmate"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
