from sqlalchemy import Column, Integer, String, Date, create_engine, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
DSN = 'postgres://nelot:12345@localhost:5432/netol_flask'
engine = create_engine(DSN)


class Advertisement(Base):
    __tablename__ = 'advertisement'

    advert_id = Column(Integer, primary_key=True)
    description = Column(Text)
    owner = Column(String(40))
    created_at = Column(Date)


if __name__ == '__main__':
    Base.metadata.create_all(engine)
