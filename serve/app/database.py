from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

POSTGRES_DATABASE_URL = "postgresql://mpsxwbpk:Xs9g67JIW5yZLgZHcjBuLInFMIpH_hCk@satao.db.elephantsql.com/mpsxwbpk"

engine = create_engine(POSTGRES_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
