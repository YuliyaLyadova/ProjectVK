import vk
import time
import sys

sys.path.append("..")

from utils.models import VKGroupBase

import sqlalchemy as sa
from sqlalchemy import create_engine
import sys
sys.path.append("..")

from sqlalchemy.orm import sessionmaker
from service.base import DATABASE

def main():
    session = vk.Session(access_token='ACCESS TOKEN')
    api = vk.API(session, v='5.92')

    fields = ['group_name', 'is_closed',
              'deactivated', 'group_type',
              'members_count','trending', 'wall']

    get_group_info(api, fields, 50000, 50030)


def get_group_info(api,fields, group_id_to_begin, group_id_to_end):
    engine = sa.create_engine(sa.engine.url.URL(**DATABASE['default']))
    Session_x = sessionmaker(bind=engine)
    sess = Session_x()


    for id in range(group_id_to_begin, group_id_to_end+1):
        group_info = api.groups.getById(group_id=id, fields=fields)
        #group = sess.query(VKGroupBase).filter(VKGroupBase.group_id == group_info[id]['id']).first()

        group_id = int(group_info[id]['id']),
        group_name = group_info[id]['screen_name'],
        is_closed = int(group_info[id]['is_closed']),
        is_deactivated = int(1) if group_info[id].get('deactivated') else int(0),
        group_type = group_info[id].get('type'),
        #description = group_info[id].get('description'),
        members_count = int(group_info[id]['members_count'] if group_info[id]['members_count'] else 0),
        trending = int(group_info[id]['trending'] if group_info[id]['trending'] else 0),
        wall = int(group_info[id]['wall']
        #time.sleep(0.3)

        
    sess.add_all([group_id, group_name, is_closed,is_deactivated, group_type,members_count, trending,wall])

    
    sess.commit()
    sess.close()

    print(f'Operation took {str(time.clock() - start_time)} seconds')




if __name__ == '__main__':
    main()
