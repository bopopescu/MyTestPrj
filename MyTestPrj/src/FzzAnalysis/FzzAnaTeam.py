# *-* coding:UTF-8 *-*
'''
Created on 2016年5月24日

@author: Administrator
'''

import urllib
import json
import string
from model.Team import Team
import os
import csv
import sys
import time
import threading
from Queue import Queue

class FzzAnaTeam(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.team_list = []
        self.getTeamList()
        
    def getTeamList(self, lgid=None):
        srcpath = os.path.abspath(os.path.join(sys.path[0], os.pardir))
        fileName = 'teamlist_Fzz_2017.csv'
        targetpath = os.path.join(srcpath, 'docs', fileName)
        
        mFile = open(targetpath, 'r')
        reader = csv.reader(mFile)
        self.team_list = []
        
        for line in reader:
            if lgid == None:                
                tmpteam = Team(line[0])
                tmpteam.teamname = line[1].decode('gbk')
                self.team_list.append(tmpteam)
            else:
                if str(lgid) == line[2]:
                    tmpteam = Team(line[0])
                    tmpteam.teamname = line[1].decode('gbk')
                    self.team_list.append(tmpteam)

def produce(queue,proqueue,threadid):

    while proqueue.empty() == False:
        try:
            tmpteam = proqueue.get(1,2)
#             print 'thdid:%s    teamid:%s' % (threadid,tmpteam.teamid)
            tmpteam.getTeamData()
            queue.put(tmpteam)
        except:
            print 'error'
        
def comsume(queue):
    while True:
        try:
            tmpteam = queue.get(1,3)
#             if tmpteam.analysisTeamTotalBall(4,True):
#                 print tmpteam.slpdsc
#                 print tmpteam.printStr
            if tmpteam.totalBall(range(4,20)):
                print tmpteam.printStr
        except:
            print "%s:  finished!" % time.ctime()
            break
            
if __name__ == '__main__':
    
    print time.ctime()
    atask = FzzAnaTeam()
    atask.getTeamList(4240)
    
    protqueue = Queue()
    for team in atask.team_list:
        protqueue.put(team)
    myqueue = Queue()
    proThds = []
    for i in range(10):
        tmpThd = threading.Thread(target=produce,args=(myqueue,protqueue,i))
        tmpThd.setDaemon(True)
        proThds.append(tmpThd)
    for thd in proThds:
        thd.start()
    
    comsuThds = []
    for i in range(3):
        tmpThd = threading.Thread(target=comsume,args=(myqueue,))
        tmpThd.setDaemon(True)
        comsuThds.append(tmpThd)
    for thd in comsuThds:
        thd.start()
   
#     time.sleep(1)
#     t2 = threading.Thread(target=comsume,args=(myqueue,))
#     t2.setDaemon(True)
#     t2.start()
    
    for thd in proThds:
        thd.join()
    for thd in comsuThds:
        thd.join()

#     for team in atask.team_list:
#         team.getTeamData()
#          
#         if team.analysisHalfDraw(False,1):
#             print team.slpdsc
#             print team.printStr
#         if team.analysisTeamTotalBall(2):
#             print team.slpdsc
#             print team.printStr
#         if team.analysisTeamTotalBallLess(1,True):
#             print team.slpdsc
#             print team.printStr
#         if team.analysisDraw():
#             if team.printStr != '':
#                 print team.slpdsc
#                 print team.printStr
#         
#         team.writedown(u'E:\个人\竞猜数据\DS足球')
    

    print time.ctime()