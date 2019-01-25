import vk
import time

from service.base import VK_TOKEN
from utils.db_session import session as db_session
from utils.models import VKGroupBase


def get_group_info(api, fields, group_id_to_begin, group_id_to_end):
    sess = db_session()

    for group_id in range(group_id_to_begin, group_id_to_end):
        group_info = api.groups.getById(group_id=group_id, fields=fields)


        group = sess.query(VKGroupBase).filter(
            VKGroupBase.username == group_info['id']
        ).first()

        group_id = int(group_info['id']),
        group_name = group_info['screen_name'],
        is_closed = bool(group_info.get('is_closed')),
        is_deactivated = True if group_info.get('deactivated') else False,
        group_type = group_info.get('type'),
        description = group_info.get('description'),
        members_count = int(group_info['members_count']),
        trending = int(group_info.get('trending')),
        wall = int(group_info.get('wall'))

        if group:
            group.group_id = group_id,
            group.group_name = group_name,
            group.is_closed = is_closed,
            group.is_deactivated = is_deactivated,
            group.group_type = group_type,
            group.description = description,
            group.members_count = members_count,
            group.trending = trending,
            group.wall = wall
        else:
            sess.add(
                VKGroupBase(
                    group_id=group_info['id'],
                    group_name=group_info['id'],
                    is_closed=group_info['id'],
                    is_deactivated=group_info['id'],
                    group_type=group_info['id'],
                    description=group_info['id'],
                    members_count=group_info['id'],
                    trending=group_info['id'],
                    wall=group_info['id'],
                )
            )
    sess.commit()
    sess.close()

    print(f'Operation took {str(time.clock() - start_time)} seconds')


def main():
    session = vk.Session(access_token=VK_TOKEN)
    api = vk.API(session, v='5.92')

    fields = ['group_name', 'is_closed',
              'deactivated', 'group_type',
              'description', 'members_count',
              'trending', 'wall']

    get_group_info(api, fields, 1, 5)


if __name__ == '__main__':
    main()
