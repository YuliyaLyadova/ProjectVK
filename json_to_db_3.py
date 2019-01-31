import json
import sys

sys.path.append("..")

from service.base import VK_TOKEN
from utils.db_session import Session as db_session
from utils.models import VKGroupBase

def json_to_db(fields,id_to_begin,id_to_end):
    sess = db_session()

    for id in range(id_to_begin,id_to_end+1):
        with open('C:\projects\ProjectInsta\ProjectInsta_TR\dbdata\mt_group_info.json','r') as file:
            group_info=json.load(file)

            sess.add(VKGroupBase(                  

            group_id = group_info[id]['id'],
            group_name = group_info[id]['name'],
            is_closed =  group_info[id]['is_closed'],
            is_deactivated = int(1) if group_info[id].get('deactivated') else int(0),
            group_type = group_info[id]['type'],
            members_count = group_info[id].get('members_count',int(0)),
            trending = group_info[id].get('trending',int(0)),
            wall = group_info[id].get('wall',int(0))
                                    )
                    )
            sess.commit()
            sess.close()

    print(f'Operation took {str(time.clock() - start_time)} seconds')


def main():
    fields = ['group_id','group_name', 'is_closed',
              'deactivated','group_type', 'members_count',
              'trending', 'wall']

    json_to_db(fields, 1, 24411)


if __name__ == '__main__':
    main()
