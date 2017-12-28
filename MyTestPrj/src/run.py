# *-* coding:UTF-8 *-*
'''
Created on 2016年5月25日

@author: Administrator
'''

from model.League import League
import os
import json
import csv


league_500_list = ['3753','3444','3748', '3749', '3756','3773', '3527', '3757', '3760', '3826', '3901', '3524','3798','4038', '3460', '3840','3841']


# 通过联赛id列表获取teamid，写入csv
def loadteamidData(lgeid_list=[]):
    if lgeid_list == None:
        return 
    
    league_list = []
    srcDir = os.getcwd()
    docDir = os.path.join(srcDir, 'docs')
    filename = os.path.join(docDir, 'teamlist_500.csv')
    
    
    for lgid in lgeid_list:
        mLeague = League(lgid)
        mLeague.fromLeagueidGetTeamid()
        league_list.append(mLeague)
        
    mFile = open(filename, 'wb')
    writer = csv.writer(mFile)
    
    for lgeitem in league_list:
        for item in lgeitem.team_dict:
            writer.writerow([item, lgeitem.team_dict[item].encode('gbk'), lgeitem.leagueid])
    
    mFile.close()
    
def loadteamidData_ds(lge_list=[]):
    if lge_list == None:
        return 
    
    league_list = []
    srcDir = os.getcwd()
    docDir = os.path.join(srcDir, 'docs')
    filename = os.path.join(docDir, 'teamTest.csv')
    
    
    for lge in lge_list:
        mLeague = League(lge)
        mLeague.fromLeagueidGetTeamid()
        league_list.append(mLeague)
        
    mFile = open(filename, 'wb')
    writer = csv.writer(mFile)
    
    for lgeitem in league_list:
        for item in lgeitem.team_dict:
            writer.writerow([item,lgeitem.team_dict[item]])
    
    mFile.close()
    
if __name__ == '__main__':
    loadteamidData(league_500_list)
    pass
#     lines = []
#     
#     mLeague = League('3749')
#     team_dict = mLeague.fromLeagueidGetTeamid()
#     srcDir = os.getcwd()
#     docDir = os.path.join(srcDir, 'docs')
#     filename = os.path.join(docDir, 'teamTest.csv')
#     mFile = open(filename, 'ab+')
#     reader = csv.reader(mFile)
#     writer = csv.writer(mFile)
#     for line in reader:
#         lines.append(line)
# 
#     for item in team_dict.keys():
#         if  [item,team_dict[item]] in lines:
#             pass
#         else:
#             writer.writerow([item,team_dict[item]])
#     mFile.close()

    
