from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

DATABASE_URL = "postgresql://user:postgres@localhost/hr_system"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Drop all tables
Base.metadata.drop_all(engine)

# Recreate the tables after cleaning
Base.metadata.create_all(engine)

session.close()
