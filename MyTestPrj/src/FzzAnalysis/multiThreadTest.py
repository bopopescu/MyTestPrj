'''
Created on 2016-8-24

@author: A
'''
import string
from model.Team import Team
from FzzAnalysis.FzzAnaTeam import FzzAnaTeam
import threading
from time import ctime

def run(list=[]):
#     print list

    for team in list:
#         print team
        team.getTeamData()
       
        if team.isDraw():
            print team.slpdsc
            print team.printStr
        if team.totalBall([0,1]):
            print team.slpdsc
            print team.printStr

if __name__ == '__main__':
    print ctime()
    atask = FzzAnaTeam()
    atask.getTeamList(4240)
    mlen = len(atask.team_list)
    list1 = atask.team_list[:mlen/2]
    list2 = atask.team_list[mlen/2:]
    t1 = threading.Thread(target=run,args=(list1,))
    
    t2 = threading.Thread(target=run,args=(list2,))
    t1.setDaemon(True)
    t2.setDaemon(True)
    t2.start()
    t1.start()
    t1.join(20)
    print ctime()
