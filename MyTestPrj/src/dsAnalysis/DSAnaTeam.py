# *-* coding:UTF-8 *-*
'''
Created on 2016年5月24日

@author: Administrator
'''

import urllib
import json
import string
from model.TeamDS import TeamDS
import os
import csv
import sys
import datetime

class DSAnaTeam(object):
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
        srcpath = os.path.abspath(os.path.join(os.path.split(os.path.realpath(__file__))[0], os.pardir))
        now = datetime.datetime.now()
        mYear = now.strftime('%Y')
        fileName = 'teamlist_DS_%s.csv' % mYear
        targetpath = os.path.join(srcpath, 'docs', fileName)

        
        mFile = open(targetpath, 'r')
        reader = csv.reader(mFile)
        self.team_list = []
        
        for line in reader:
            if lgid == None:                
                tmpteam = TeamDS(line[0])
                tmpteam.teamname = line[1].decode('gbk')
                self.team_list.append(tmpteam)
            else:
                if str(lgid) == line[2]:
                    tmpteam = TeamDS(line[0])
                    tmpteam.teamname = line[1].decode('gbk')
                    self.team_list.append(tmpteam)
        
if __name__ == '__main__':

    atask = DSAnaTeam(85)
    atask.getTeamList()
    for team in atask.team_list:
        #   读数据
        team.getTeamData()
        #   分析数据
        team.analysisDraw()
        # team.TotalCorner(range(12,30),showDetl=False)
#         team.writedown(u'E:\个人\竞猜数据\DS足球')