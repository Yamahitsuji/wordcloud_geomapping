from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from db.setting import Base


class Article(Base):
    __tablename__ = 'article'
    id = Column('id', Integer, primary_key=True)
    title = Column('title', String(190))
    url = Column('url', String(190))
    latitude = Column('latitude', Float)
    longitude = Column('longitude', Float)
    read = Column('read', Text)
    text = Column('text', Text)
    created_at = Column('created_at', DateTime, default=datetime.now)
    updated_at = Column('updated_at', DateTime, default=datetime.now)
