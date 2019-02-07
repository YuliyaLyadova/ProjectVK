import vk
import time
import sys
from sqlalchemy import and_
from dateparser import parse

sys.path.append("..")

from service.base import VK_TOKEN
from utils.db_session import session as db_session
from utils.models import VKGroupBase, GroupMembersBase


def get_group_info(api,fields, group_id_to_begin, group_id_to_end):
    sess = db_session()

    chunks_with_group_ids = get_chunk(list(range(group_id_to_begin, group_id_to_end+1)), 499)

    for chunk in chunks_with_group_ids:
        group_info = api.groups.getById(group_ids=chunk, fields=fields)

        for group_vk in groups_info:

            group = sess.query(VKGroupBase).filter(
                VKGroupBase.group_id == int(group_vk['id'])).first()

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
                sess.add(VKGroupBase(
                group_id=group_id,
                group_name=group_name,
                is_closed=is_closed,
                is_deactivated=is_deactivated,
                group_type=group_type,
                description=description,
                members_count=members_count,
                trending=trending,
                wall=wall))

    sess.commit()
    sess.close()

    #print(f'Operation took {str(time.clock() - start_time)} seconds')

def collect_members(api, fields,group_id):
    sess = db_session()

    # group = sess.query(VKGroupBase).filter(
    #              VKGroupBase.members_count<10000 and VKGroupBase.members_count> 5000
    #          )
    #groups = sess.query(VKGroupBase).filter(
    
    #             and_(VKGroupBase.members_count<10000, VKGroupBase.members_count> 5000)
    
    #        )
    
    groups=[922,7073,77690]
    

    for gr in groups:
        group = sess.query(VKGroupBase).filter(
                VKGroupBase.group_id == gr).first()
        offset=0

        members_integer=int(group.members_count/1000)
        members_tail=group.members_count - members_integer*1000

        for _ in range(members_integer):
            members = api.groups.getMembers(group_id=group_id, offset=offset, fields=fields)

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
                    bdate = parse(member.get('bdate'))
                    bdate = bdate.date() if bdate else None
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
            offset += 1000

         
        members = api.groups.getMembers(group_id=group_id, offset=offset, count=members_tail,
                                             fields=fields)  

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




def main():
    session = vk.Session(access_token='d2f5660e65e69324e0658cb78d2065a2d1c55b2a54d2528924f9285c68002a5b2bc0d4c6d6d3046420eaf')
    api = vk.API(session, v='5.92')

    #fields = ['group_name', 'is_closed',
    #          'deactivated', 'group_type',
    #          'members_count','trending', 'wall']

    fields=['group_id','member_id','first_name',
    'last_name','is_closed','is_deactivated','sex',
    'bdate','city_id','city_title','country_id','country_title']

    groups=[922,7073,77690]


    collect_members(api, fields,groups)


if __name__ == '__main__':
    main()
