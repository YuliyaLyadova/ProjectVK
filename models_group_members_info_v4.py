import vk
import json
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


start_time = time.clock()

def main():
    session = vk.Session(access_token='ACCESS TOKEN')
    api = vk.API(session, v='5.92')

    fields = ["sex", "bdate","city","country","education","universities","schools","relation"]
    
    group_info=[{'group_id':213,'members_count':4196},{'group_id':424,'members_count':3875},{'group_id':429,'members_count':4609}]
    group_info_len=len(group_info)
    item=0

    while item < group_info_len:
        group_id=group_info[item]['group_id']
        group_count=group_info[item]['members_count']
        item+=1

        get_members_info(api, fields, group_id,group_count)
        print(f'Operation took {str(time.clock()-start_time)} seconds')

    else:

        print('all is done. great job!')

  



def get_members_info(api,fields, group_id,group_count):   

    engine = sa.create_engine(sa.engine.url.URL(**DATABASE['default']))
    Session_x = sessionmaker(bind=engine)
    sess = Session_x()

    offset=0

    while offset<1001:

        members_info=api.groups.getMembers(group_id=group_id, offset=offset,fields=fields)
        print(type(members_info))
        print(members_info.keys())
     
        group_id = int(group_id),
        member_id = int(members_info['items']['id']),
        first_name = members_info['items']['first_name'],
        last_name = members_info['items']['last_name'],
        is_closed = int(0) if members_info['items']['is_closed']==False else int(0)
        is_deactivated = int(1) if members_info['1']['items'].get('deactivated') else int(0)
        sex = int(members_info['items']['sex']),
        bdate=members_info['items']['bdate'],
        city_id=int(members_info['items']['city']['id']),
        city_title=members_info['items']['city']['title'],
        country_id=int(members_info['items']['country']['id']),
        country_title=members_info['items']['country']['title']

        while len(members_info['items'])<5001:
            offset+=1000
            members_info=api.groups.getMembers(group_id=group_id, offset=offset,fields=fields)
            
            group_id = int(group_id),
            member_id = int(members_info['items']['id']),
            first_name = members_info['items']['first_name'],
            last_name = members_info['items']['last_name'],
            is_closed = int(0) if members_info['items']['is_closed']==False else int(0)
            is_deactivated = int(1) if members_info['items'].get('deactivated') else int(0)
            sex = int(members_info['items']['sex']),
            bdate=members_info['items']['bdate'],
            city_id=int(members_info['items']['city']['id']),
            city_title=members_info['items']['city']['title'],
            country_id=int(members_info['items']['country']['id']),
            country_title=members_info['items']['country']['title']
        
        else:
            print('all members are at home, feeling good')
            
    else:
        print('mission completed')

    
    #time.sleep(0.3)    

        
    sess.add_all(GroupMembersBase(
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
        country_id=country_title,
        country_title=country_title))
   
    sess.commit()
    sess.close()

 


if __name__ == '__main__':
    main()
