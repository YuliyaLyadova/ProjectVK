import vk
import time
import sys

sys.path.append("..")

from service.base import VK_TOKEN
from utils.db_session import session as db_session
from utils.models import VKGroupBase


def main():
    session = vk.Session(access_token='ACESS TOKEN')
    api = vk.API(session, v='5.92')

    fields = ['group_name', 'is_closed',
              'deactivated', 'group_type', 'description',
              'members_count','trending', 'wall']

    get_group_info(api, fields, 50000, 50050)



def get_group_info(api,fields, group_id_to_begin, group_id_to_end):
    sess = db_session()

    for id in range(group_id_to_begin, group_id_to_end+1):
        group_info = api.groups.getById(group_id=id, fields=fields)


        group = sess.query(VKGroupBase).filter_by(
            VKGroupBase.group_id == group_info[id]['id']).first()

        group_id = int(group_info[id]['id']),
        group_name = group_info[id]['screen_name'],
        is_closed = int(group_info[id]['is_closed']),
        is_deactivated = int(1) if group_info[id].get('deactivated') else int(0),
        group_type = group_info[id].get('type'),
        description = group_info[id].get('description') if group_info[id].get('description') else int(0),
        members_count = int(group_info[id]['members_count'] if group_info[id]['members_count'] else int(0)),
        trending = int(group_info[id]['trending'] if group_info[id]['trending'] else int(0),
        wall = int(group_info[id]['wall'])


        #if group is None:
   
        sess.add_all([group_id=group_id,
            group_name=group_name,
            is_closed=is_closed,
            is_deactivated=is_deactivated,
            group_type=group_type,
            description=description,
            members_count=members_count,
            trending=trending,
            wall=wall])
        

        time.sleep(0.3)
    sess.commit()
    sess.close()

    print(f'Operation took {str(time.clock() - start_time)} seconds')


if __name__ == '__main__':
    main()
