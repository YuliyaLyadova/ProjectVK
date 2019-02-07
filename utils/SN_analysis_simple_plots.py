import pandas as pd
import sqlite3
import networkx as nx
import matplotlib.pyplot as plt
import numpy
import seaborn as sns
from pylab import rcParams
rcParams['figure.figsize'] = 8, 5
import sklearn
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler

#connect to database
conn = sqlite3.connect("C:\projects\ProjectInsta\ProjectInsta_TR\dbdata\db.sqlite3")

groups = pd.read_sql_query("select * from vkgroupbase", conn)
members = pd.read_sql_query("select * from groupmembersbase", conn)

#delete unevenly filled columns and identify columns with useful data
groups=groups.dropna()
useful_attr=['group_id','group_name','is_closed','is_deactivated','members_count','wall']

members=members.dropna()
#members_year=members['bdate'].dt.year

#Disctribution of groups in first 100K
MC_Dist_groups = groups[[x for x in groups.columns if 'members_count' in x] + ['group_id']]
MC_Dist_groups.groupby('group_id').sum().plot()

plt.savefig('C:\projects\ProjectInsta\ProjectInsta_TR\dbdata\MC_dist_plot.png')

#SNS Disctribution of groups in first 100K
sns.distplot(groups.members_count)
plt.savefig('C:\projects\ProjectInsta\ProjectInsta_TR\dbdata\MC_dist_plt_sns.png')


#SNS Groups Pairs of attrs
cols = ['group_id', 'is_deactivated', 'is_closed', 'members_count', 'wall']
sns_plot = sns.pairplot(groups[cols])
plt.savefig('C:\projects\ProjectInsta\ProjectInsta_TR\dbdata\pairplot.png')

#SNS Members Pairs of attrs
cols = ['group_id', 'member_id','first_name','last_name', 'sex', 'bdate','city_id']
sns_plot = sns.pairplot(members[cols])
plt.savefig('C:\projects\ProjectInsta\ProjectInsta_TR\dbdata\members_pairplot.png')

#SNS sexes distribution
_, axes = plt.subplots(1, 2, sharey=True, figsize=(16,6))
sns.countplot(x='first_name', hue='sex', data=members, ax=axes[0])
sns.countplot(x='bdate', hue='sex', data=members, ax=axes[1])
plt.savefig('C:\projects\ProjectInsta\ProjectInsta_TR\dbdata\S_Dist.png')


#SNS names distribution
sns.countplot(x='first_name', hue='sex', data=members)
plt.savefig('N_Dist.png')

#is there anything really?
groups_nls = groups.drop(['id', 'group_name','group_type','description'], axis=1)
groups_nls['is_closed'] = pd.factorize(groups_nls['is_closed'])[0]
#groups_nls['is_deactivated] = pd.factorize(groups_nls['is_deactivated'])[0]
scaler = StandardScaler()
groups_nls_scaled = scaler.fit_transform(groups_nls)
tsne = TSNE(random_state=17)
tsne_representation = tsne.fit_transform(groups_nls_scaled)
plt.scatter(tsne_representation[:, 0], tsne_representation[:, 1], 
            c=groups['is_deactivated'].map({True: 'blue', False: 'orange'}))
plt.savefig('\dbdata\Is_Really.png')