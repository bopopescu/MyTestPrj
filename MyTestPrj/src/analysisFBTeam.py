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

class AnalySisFBTeam(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.team_list = []
        self.getTeamList()
        
    def getTeamList(self):
        srcDir = os.getcwd()
        docDir = os.path.join(srcDir, 'docs')
        filename = os.path.join(docDir, 'teamTest.csv')
        
        mFile = open(filename, 'r')
        reader = csv.reader(mFile)
        
        for line in reader:
            tmpteam = Team(line[0])
            tmpteam.teamname = line[1].decode('gbk')
            self.team_list.append(tmpteam)
    
        
if __name__ == '__main__':
    atask = AnalySisFBTeam()
    for team in atask.team_list:
        team.toString()
        team.analysisTeamTotalBall(0, False)
        team.analysisTeamTotalBall(1, False)
        team.analysisTeamTotalBall(2, False)
        team.analysisTeamTotalBallLess(1, False)
        team.analysisTeamTotalBallMore(4, False)