from sqlalchemy import create_engine, Column, Integer, String, DateTime, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+mysqlconnector://root:password@localhost/lung_cancer_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

class CTScanResult(Base):
    __tablename__ = "ct_results"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255))
    prediction = Column(String(50))
    timestamp = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

def init_db():
    Base.metadata.create_all(bind=engine)


