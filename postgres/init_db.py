from sqlalchemy import create_engine
from models import Base

DATABASE_URL = "postgresql://user:postgres@localhost/hr_system"

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
