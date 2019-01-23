import sqlalchemy as sa
from sqlalchemy import Column
from sqlalchemy import String, Integer, Date

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import json


engine=create_engine('sqlite:///vkgroupbase.db', echo=True)

Base.metadata.bind = engine
#command to create new DB

class VKGroupBase(Base):
    __tablename__ = 'vkgroupbase'
    group_id=Column('group_id',String(500),primary_key=True)
    group_name=Column('group_name', String(100))
    is_closed=Column('is_closed',Integer)
    deactivated=Column('deactivated',Integer)
    group_type=Column('group_type', String(50))
    description=Column('description', String(1000))
    members_count=Column('members_count', Integer)
    trending=Column('trending',Integer)
    wall=Column('wall', Integer)

    def __init__(self,group_id,group_name,is_closed,deactivated,group_type,description,members_count,trending,wall):
        self.group_id=group_id
        self.group_name=group_name
        self.is_closed=is_closed
        self.deactivated=deactivated
        self.group_type=group_type
        self.description=description
        self.members_count=members_count
        self.trending=trending
        self.wall=wall

# Создание таблицы
Base.metadata.create_all(engine)

