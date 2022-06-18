from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql://postgres:root@185.217.131.133:5432")

Base = declarative_base()

class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    cost = Column(String)




Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


# create a session
session = Session()
