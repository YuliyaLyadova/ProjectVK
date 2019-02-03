import vk
import argparse
from dateparser import parse

from service.base import VK_TOKEN
from utils.db_session import session as db_session
from utils.models import VKGroupBase, GroupMembersBase
from utils.chunks import get_chunk


def get_group_info(api, fields, group_id_to_begin, group_id_to_end):
    sess = db_session()

    chunks_with_group_ids = get_chunk(list(range(group_id_to_begin, group_id_to_end+1)), 499)

    for chunk in chunks_with_group_ids:
        groups_info = api.groups.getById(group_ids=chunk, fields=fields)

        for group_vk in groups_info:

            group = sess.query(VKGroupBase).filter(
                VKGroupBase.group_id == int(group_vk['id'])
            ).first()

            group_id = int(group_vk['id'])
            group_name = str(group_vk['screen_name'])
            is_closed = True if group_vk.get('is_closed') else False
            is_deactivated = True if group_vk.get('deactivated') else False
            group_type = str(group_vk.get('type'))
            description = str(group_vk.get('description'))
            members_count = int(group_vk.get('members_count', 0))
            trending = int(group_vk.get('trending', 0))
            wall = int(group_vk.get('wall', 0))

            if group:
                group.group_id = group_id
                group.group_name = group_name
                group.is_closed = is_closed
                group.is_deactivated = is_deactivated
                group.group_type = group_type
                group.description = description
                group.members_count = members_count
                group.trending = trending
                group.wall = wall
            else:
                sess.add(
                    VKGroupBase(
                        group_id=group_id,
                        group_name=group_name,
                        is_closed=is_closed,
                        is_deactivated=is_deactivated,
                        group_type=group_type,
                        description=description,
                        members_count=members_count,
                        trending=trending,
                        wall=wall
                    )
                )
        sess.commit()
        sess.close()


def collect_members(api, fields, group_id, offset=0, limit=1000):
    sess = db_session()

    # group = sess.query(VKGroupBase).filter(
    #             VKGroupBase.group_id == group_id
    #         ).first()

    members = api.groups.getMembers(group_id=group_id, offset=offset, count=limit, fields=fields)

    for member in members['items']:

        member_id = int(member['id'])
        db_member = sess.query(GroupMembersBase).filter(
            GroupMembersBase.member_id == member_id
        ).first()

        first_name = member.get('first_name', 'Unknown')
        last_name = member.get('last_name', 'Unknown')
        is_closed = False if member.get('is_closed') else True
        is_deactivated = True if member.get('deactivated') else False
        sex = int(member.get('sex'))
        try:
            bdate = parse(member.get('bdate')).date()
        except TypeError:
            bdate = None
        city_id = int(member.get('city', {}).get('id', 0))
        city_title = member.get('city', {}).get('title')
        country_id = int(member.get('country', {}).get('id', 0))
        country_title = member.get('country', {}).get('title')

        if db_member:
            db_member.group_id = group_id
            db_member.first_name = first_name
            db_member.last_name = last_name
            db_member.is_closed = is_closed
            db_member.is_deactivated = is_deactivated
            db_member.sex = sex
            db_member.bdate = bdate
            db_member.city_id = city_id
            db_member.city_title = city_title
            db_member.country_id = country_id
            db_member.country_title = country_title
        else:
            sess.add(
                GroupMembersBase(
                    group_id=group_id,
                    member_id=member_id,
                    first_name=first_name,
                    last_name=last_name,
                    is_closed=is_closed,
                    is_deactivated=is_deactivated,
                    sex=sex,
                    bdate=bdate,
                    city_id=city_id,
                    city_title=city_title,
                    country_id=country_id,
                    country_title=country_title,
                )
            )
    sess.commit()
    sess.close()


def main(members=False):
    session = vk.Session(access_token=VK_TOKEN)
    api = vk.API(session, v='5.92')

    group_fields = ['group_name', 'is_closed',
                    'deactivated', 'group_type',
                    'description', 'members_count',
                    'trending', 'wall']

    member_fields = ['sex', 'bdate', 'city', 'country', 'has_mobile',
                     'status', 'last_seen', 'common_count']

    if members:
        collect_members(api, member_fields, 11787)
    else:
        get_group_info(api, group_fields, 10000, 100000)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--get_members", help="Collect VK groups members")
    args = parser.parse_args()
    if args.get_members:
        main(members=True)
    else:
        # main()
        pass
