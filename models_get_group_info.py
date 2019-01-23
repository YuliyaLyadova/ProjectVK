import vk
import pprint
import json
import time
import collections

start_time=time.clock()
session = vk.Session(access_token='MY TOKEN INSERTED')
api = vk.API(session,v='5.92')

fields=['group_name','is_closed','deactivated','group_type','description','members_count','trending','wall']

#vk:limit=3 requests per second


def get_group_info():
    groupid=1
    while groupid<4:
        group_info=api.groups.getById(group_id=groupid, fields=fields)
    
        #pprint.pprint(group_info)
        with open('group_info_test.json','a') as f:
            json.dump(group_info,f,indent=2)

        time.sleep(0.3)
        
        groupid+=1 

get_group_info()

print('Operation took '+str(time.clock()-start_time)+' seconds')


