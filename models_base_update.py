from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os


#подключаемся к созданной базе
engine=create_engine('sqlite:///vkgroupbase.db', echo=True)
engine.connect()

# Создание сессии для записи новых данных


def save_new_info():
    Session=sessionmaker(bind=engine)
    session=Session()
    new_info=os.path.abspath('C://projects/.../group_info.json')
    json_group_info=open(new_info).read()
    new_entries=[]
    for entry in json_group_info:
        new_entry = VKGroupBase(group_id=new_info[int('id')+1]['id'],
                              group_name=new_info[int('id')+1]['group_name'],
                              deactivated=new_info[int('id')+1]['deactivated'],
                              group_type=new_info[int('id')+1]['group_type'],
                              description=new_info[int('id')+1]['description'],
                              members_count=new_info[int('id')+1]['members_count'],
                              trending=new_info[int('id')+1]['trending'],
                              wall=new_info[int('id')+1]['wall']
                              )
        new_entries.append(entry)
    session.add(new_entries)
    session.commit()
    




