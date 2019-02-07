import pandas as pd
import sqlite3
import networkx as nx
import matplotlib.pyplot as plt
import numpy

conn = sqlite3.connect("C:\projects\ProjectInsta\ProjectInsta_TR\dbdata\db.sqlite3")

groups = pd.read_sql_query("select * from vkgroupbase", conn)
members = pd.read_sql_query("select * from groupmembersbase", conn)
cur=conn.cursor()

group_ids=list(pd.unique(members['group_id']))
print(group_ids)

myc = conn.cursor()
res_14=myc.execute('select groupmembersbase.city_id from groupmembersbase where groupmembersbase.group_id=14').fetchall()
mr_14=pd.DataFrame(res_14)[0].tolist()

res_11787=myc.execute('select groupmembersbase.city_id from groupmembersbase where groupmembersbase.group_id=11787').fetchall()
mr_11787=pd.DataFrame(res_11787)[0].tolist()

res_691=myc.execute('select groupmembersbase.city_id from groupmembersbase where groupmembersbase.group_id=691').fetchall()
mr_691=pd.DataFrame(res_691)[0].tolist()

res_577=myc.execute('select groupmembersbase.city_id from groupmembersbase where groupmembersbase.group_id=577').fetchall()
mr_577=pd.DataFrame(res_577)[0].tolist()

res_25=myc.execute('select groupmembersbase.city_id from groupmembersbase where groupmembersbase.group_id=25').fetchall()
mr_25=pd.DataFrame(res_25)[0].tolist()

res_430=myc.execute('select groupmembersbase.city_id from groupmembersbase where groupmembersbase.group_id=430').fetchall()
mr_430=pd.DataFrame(res_430)[0].tolist()

res_316=myc.execute('select groupmembersbase.city_id from groupmembersbase where groupmembersbase.group_id=316').fetchall()
mr_316=pd.DataFrame(res_316)[0].tolist()

res_1614=myc.execute('select groupmembersbase.city_id from groupmembersbase where groupmembersbase.group_id=1614').fetchall()
mr_1614=pd.DataFrame(res_1614)[0].tolist()


members_result = {}
members_result[14]=mr_14
members_result[11787]=mr_11787
members_result[691]=mr_691
members_result[577]=mr_577
members_result[25]=mr_25
members_result[430]=mr_430
members_result[316]=mr_316
members_result[1614]=mr_1614
print(len(members_result))


c = conn.cursor()
gm_ids=c.execute('select group_id,group_name, members_count from vkgroupbase;').fetchall()
gm_ids_1=pd.DataFrame(gm_ids)
#print(gm_ids_1[:5])
g_ids=gm_ids_1[0].tolist()
#print(g_ids)
g_names=gm_ids_1[1].tolist()
#print(g_names)
m_counts=gm_ids_1[2].tolist()
#print(m_counts)


keys=g_ids
values=g_names
group_names=dict(zip(keys,values))
#print(group_names)

keys=g_ids
values=m_counts
members_count=dict(zip(keys,values))
#print(members_count)


group_ids=[11787, 691, 14, 577, 25, 430, 316, 1614]
graph=nx.Graph()

for i_group in group_ids:
    group_n=group_names[i_group]
        
    for grn in group_n:
        graph.add_node(grn,with_labels=1, size=m_counts[i_group])
        
    for k_group in group_ids:
        if k_group!=i_group:
            intersection = set(members_result[k_group]).intersection(set(members_result[i_group]))

            if len(intersection)>0:
                graph.add_edge(members_result[i_group], members_result[k_group], weight=len(intersection))
    

    nx.draw(graph,with_labels=1)
         
    plt.savefig('C:\projects\ProjectInsta\ProjectInsta_TR\dbdata\plot_cities.png')