# *-* coding:UTF-8 *-*
'''
Created on 2016年5月24日

@author: Administrator
'''

import urllib
import json
import string
import os
import csv
import sys
import traceback
import pdb


def getTeamList(lgid=None):
    srcpath = os.path.abspath(os.path.join(sys.path[0], os.pardir))
    fileName = 'teamlist_500.csv'
    targetpath = os.path.join(srcpath, 'docs', fileName)

    mFile = open(targetpath, 'r')
    reader = csv.reader(mFile)
    team_list = []

    for line in reader:
        if lgid == None:
            line[1] = line[1].decode('gbk')
            team_list.append(line)

        else:
            if str(lgid) == line[2]:
                line[1] = line[1].decode('gbk')
                team_list.append(line)
    mFile.close()
    return team_list

def getTeamId(teamName):
    mTlist = getTeamList()
    if teamName != None:
        for teamItem in mTlist:
            if teamItem[1].find(teamName) > -1:
                return teamItem[0]
    return None

class Team(object):
    '''
    classdocs
    '''
    urldomain = "http://liansai.500.com/index.php"
    MAXCYCLELIMIT = 6

    def __init__(self, tid):
        '''
        Constructor
        '''
        self.teamid = str(tid)
        self.teamname = ''
        self.teamData = None
        self.rsp_json = ''
        self.printStr = ''
        self.slpdsc = ''
#         self.getTeamData()
    
    def getTeamData(self):
#         http://liansai.500.com/index.php?c=teams&a=ajax_fixture&records=100&hoa=0&tid=3434
#             "VSDATE": "2016-06-18 18:00:00",
#             "STATUSID": "5",
#             "FIXTUREID": "559381",
#             "MATCHDATE": "2016-06-18",
#             "HOMETEAMID": "492",
#             "AWAYTEAMID": "1029",
#             "HOMESCORE": "1",
#             "HOMEHTSCORE": "1",
#             "AWAYSCORE": "2",
#             "AWAYHTSCORE": "1",
#             "HOMETEAMSXNAME": "神  户",
#             "AWAYTEAMSXNAME": "鹿  岛",
#             "SIMPLEGBNAME": "日职",
#             "MATCHGBNAME": "日本职业J1联赛",
#             "SEASONID": "3748",
#             "MATCHID": "39",
#             "BACKCOLOR": "#017001",
#             "HANDICAPLINE": "0.75",
#             "HOMEMONEYLINE": "0.880",
#             "HANDICAPLINENAME": "受半球/一球",
#             "AWAYMONEYLINE": "0.980",
#             "WIN": "4.22",
#             "DRAW": "3.71",
#             "LOST": "1.72",
#             "BIGMONEYLINE": "0.75",
#             "HANDINAME": "2.5/3",
#             "SMALLMONEYLINE": "1.05",
#             "RESULT": "<span class=\\\"lred\\\">胜</span>",
#             "lpl_on": "负",
#             "PAN": "赢半",
#             "BS": "大"
        strParams = "?c=teams&a=ajax_fixture&records=100&hoa=0"
        strParams += "&tid=%s" % self.teamid
        url = self.urldomain + strParams
        rsp = urllib.urlopen(url).read()
        if rsp == None or rsp == '':
            return ''
        try:
            self.rsp_json = json.loads(rsp)
            self.teamData = json.loads(rsp)
        except BaseException:
            print 'Error:teamid=%s' % self.teamid
        #getTeamName
        if self.rsp_json['list'][0]['HOMETEAMID'] == self.teamid:
            self.teamname =  self.rsp_json['list'][0]['HOMETEAMSXNAME']
        else:
            self.teamname =  self.rsp_json['list'][0]['AWAYTEAMSXNAME']
        self.slpdsc += url + '\n' + self.rsp_json['list'][0]['SIMPLEGBNAME'] + ' ' + self.teamname + '\n'
        self.printStr += self.slpdsc.encode('utf-8')
        return self.rsp_json
        
    def analysisTeamDiffBall(self, sce = 0, showDetl = True):
        if self.rsp_json == '':
            self.getTeamData()
        maxcycle = 0
        bingotime = 0
        mLen = len(self.rsp_json['list'])
        count = mLen
        tempTag = mLen + 1;
        totalGain = 0
        self.printStr = ''
        for i in range(mLen):
            if maxcycle > self.MAXCYCLELIMIT:
                break
            
            if self.teamid == self.rsp_json['list'][mLen-1-i]['HOMETEAMID']:
                mainScore = int(self.rsp_json['list'][mLen-1-i]['HOMESCORE'])
                subordinateScore = int(self.rsp_json['list'][mLen-1-i]['AWAYSCORE'])
            else:
                mainScore = int(self.rsp_json['list'][mLen-1-i]['AWAYSCORE'])
                subordinateScore = int(self.rsp_json['list'][mLen-1-i]['HOMESCORE'])
#             pdb.set_trace()
            if mainScore - subordinateScore == sce:
                diff = tempTag - count
                odds = 3.0
                lastbet = 50 * (2 ** (diff-1))
                gain = lastbet * odds - (2*lastbet) + 50
                totalGain += gain
                if showDetl:
                    self.printStr += "%d && %s; %d 次最后投%d赚%d\n" % (count, odds,diff,lastbet,gain)
#                     print "%d && %s; %d 次最后投%d赚%d" % (count, odds,diff,lastbet,gain)
                tempTag = count
                bingotime += 1
                if diff > maxcycle:
                    maxcycle = diff
            count -= 1
        if tempTag > maxcycle + 1:
            maxcycle = tempTag
        
        self.printStr += '让%d球最大周期：%d轮\n' % (sce,maxcycle)
        self.printStr += '中的次数：%d\n' % bingotime
        self.printStr += '现在到达第%d轮\n' % (tempTag-1)
        self.printStr += "总利润%d\n" % totalGain
        if maxcycle <= self.MAXCYCLELIMIT:
            return True
        return False


    # 总进球数
    def analysisTeamTotalBall(self, sce = (0,), showDetl = True):
        if self.rsp_json == '':
            self.getTeamData()
        maxcycle = 0
        bingotime = 0
        mLen = len(self.rsp_json['list'])
        count = mLen
        tempTag = mLen + 1;
        totalGain = 0
        self.printStr = ''
        for i in range(mLen):
            if maxcycle > self.MAXCYCLELIMIT:
                break
            score_sum = int(self.rsp_json['list'][mLen-1-i]['HOMESCORE']) + int(self.rsp_json['list'][mLen-1-i]['AWAYSCORE'])
            if score_sum in sce:
                diff = tempTag - count
                odds = 3.0
                lastbet = 50 * (2 ** (diff-1))
                gain = lastbet * odds - (2*lastbet) + 50
                totalGain += gain
                if showDetl:
                    self.printStr += "%d && %s球; %d 次最后投%d赚%d\n" % (count, score_sum,diff,lastbet,gain)
#                     print "%d && %s; %d 次最后投%d赚%d" % (count, odds,diff,lastbet,gain)
                tempTag = count
                bingotime += 1
                if diff > maxcycle:
                    maxcycle = diff
            count -= 1
        if tempTag > maxcycle + 1:
            maxcycle = tempTag
        
        self.printStr += '%s球最大周期：%d轮\n' % (sce,maxcycle)
        self.printStr += '中的次数：%d\n' % bingotime
        self.printStr += '现在到达第%d轮\n' % (tempTag-1)
        self.printStr += "总利润%d\n" % totalGain
        if maxcycle <= self.MAXCYCLELIMIT:
            return True
        return False

    # 总进球数含关键进球数
    def analysisTeamMainTotalBall(self, sce=(0,), showDetl=True):
        if self.rsp_json == '':
            self.getTeamData()
        maxcycle = 0
        bingotime = 0
        mLen = len(self.rsp_json['list'])
        count = mLen
        tempTag = mLen + 1;#过程中记录命中序号
        totalGain = 0
        self.printStr = ''
        for i in range(mLen):
            if maxcycle > self.MAXCYCLELIMIT:
                break
            score_sum = int(self.rsp_json['list'][mLen - 1 - i]['HOMESCORE']) + int(
                self.rsp_json['list'][mLen - 1 - i]['AWAYSCORE'])
            if score_sum in sce[1:]:
                # diff = tempTag - count
                # odds = 3.0
                # lastbet = 50 * (2 ** (diff - 1))
                # gain = lastbet * odds - (2 * lastbet) + 50
                # totalGain += gain
                if showDetl:
                    self.printStr += "%d && %s球; \n" % (count, score_sum)
                    # self.printStr += "%d && %s球; %d 次最后投%d赚%d\n" % (count, score_sum, diff, lastbet, gain)
                    #                     print "%d && %s; %d 次最后投%d赚%d" % (count, odds,diff,lastbet,gain)
                tempTag -= 1


            if score_sum in sce[:1]:
                diff = tempTag - count
                odds = 3.0
                lastbet = 50 * (2 ** (diff - 1))
                gain = lastbet * odds - (2 * lastbet) + 50
                totalGain += gain
                if showDetl:
                    self.printStr += "%d && %s球; %d 次最后投%d赚%d\n" % (count, score_sum, diff, lastbet, gain)
                    #                     print "%d && %s; %d 次最后投%d赚%d" % (count, odds,diff,lastbet,gain)
                tempTag = count
                bingotime += 1
                if diff > maxcycle:
                    maxcycle = diff
            count -= 1
        if tempTag > maxcycle + 1:
            maxcycle = tempTag

        self.printStr += '%s球最大周期：%d轮\n' % (sce, maxcycle)
        self.printStr += '中的次数：%d\n' % bingotime
        self.printStr += '现在到达第%d轮\n' % (tempTag - 1)
        self.printStr += "总利润%d\n" % totalGain
        if maxcycle <= self.MAXCYCLELIMIT:
            return True
        return False

    # 半场总进球数
    def analysisTeamHalfTotalBall(self, sce = 0, showDetl = True):
        if self.rsp_json == '':
            self.getTeamData()
        maxcycle = 0
        bingotime = 0
        mLen = len(self.rsp_json['list'])
        count = mLen
        tempTag = mLen + 1;
        totalGain = 0
        for i in range(mLen):
            score_sum = int(self.rsp_json['list'][mLen-1-i]['HOMEHTSCORE']) + int(self.rsp_json['list'][mLen-1-i]['AWAYHTSCORE'])
            if score_sum == sce:
                diff = tempTag - count
                odds = 3.0
                lastbet = 50 * (2 ** (diff-1))
                gain = lastbet * odds - (2*lastbet) + 50
                totalGain += gain
                if showDetl:
                    print "%d && %s; %d 次最后投%d赚%d" % (count, odds,diff,lastbet,gain)
                tempTag = count
                bingotime += 1
                if diff > maxcycle:
                    maxcycle = diff
            count -= 1
        if tempTag > maxcycle + 1:
            maxcycle = tempTag
        print '半场%d球最大周期：%d轮' % (sce,maxcycle)
        print '中的次数：%d' % bingotime
        print '现在到达第%d轮' % (tempTag-1)
        print "总利润%d" % totalGain

    def totalBall(self, num=[2], showDetl=True):
        if self.teamData == []:
            self.getTeamData()
        maxcycle = 0
        bingotime = 0
        mLen = len(self.teamData['list'])
        count = mLen
        tempTag = mLen + 1;
        totalGain = 0

        for i in range(mLen):
            try:
                scoreH = string.atoi(self.teamData['list'][mLen - 1 - i]['HOMESCORE'])
                scoreA = string.atoi(self.teamData['list'][mLen - 1 - i]['AWAYSCORE'])
                ball_sum = scoreH + scoreA
            except Exception, e:
                print traceback.format_exc()
                print 'Excute to the line %s' % str(mLen - 1 - i)
                print self.teamData[mLen - 1 - i]
                return False
            # print '%d:%s|%s' % (i,self.teamData[mLen-1-i][-3],cornerdata)

            if ball_sum in num:
                diff = tempTag - count
                odds = 2
                lastbet = 50 * (2 ** (diff - 1))
                gain = lastbet * odds - (2 * lastbet) + 50
                totalGain += gain
                if showDetl:
                    self.printStr += '%d && %s赔率%d个进球; %d 次最后投%d赚%d' % (count, odds, ball_sum, diff, lastbet, gain)
                    self.printStr += '\n'
                tempTag = count
                bingotime += 1
                if diff > maxcycle:
                    maxcycle = diff
            count -= 1
        if tempTag > maxcycle + 1:
            maxcycle = tempTag
        self.printStr += '%s个进球最大周期：%d轮' % ('-'.join([str(i) for i in num]), maxcycle)
        self.printStr += '\n'
        self.printStr += '中的次数：%d' % bingotime
        self.printStr += '\n'
        self.printStr += '现在到达第%d轮' % (tempTag - 1)
        self.printStr += '\n'
        self.printStr += "总利润%d" % totalGain
        self.printStr += '\n'
        return True

    # 平局
    def isDraw(self, num = range(0,51,2), showDetl = True):
        if self.teamData == None:
            self.getTeamData()
        maxcycle = 0
        bingotime = 0
        mLen = len(self.teamData['list'])
        count = mLen
        tempTag = mLen + 1;
        totalGain = 0


        for i in range(mLen):
            try:
                scoreH = string.atoi(self.teamData['list'][mLen-1-i]['HOMESCORE'])
                scoreA = string.atoi(self.teamData['list'][mLen-1-i]['AWAYSCORE'])
                ball_sum = scoreH + scoreA
            except Exception,e:
                print traceback.format_exc()
                print 'Excute to the line %s' % str(mLen-1-i)
                print self.teamData[mLen-1-i]
                return
            # print '%d:%s|%s' % (i,self.teamData[mLen-1-i][-3],cornerdata)

            if scoreH == scoreA and ball_sum in num:
                diff = tempTag - count
                if self.teamData['list'][mLen-1-i]['DRAW'] == None:
                    odds = 3
                else:
                    odds = string.atof(self.teamData['list'][mLen-1-i]['DRAW'])
                lastbet = 50 * (2 ** (diff-1))
                gain = lastbet * odds - (2*lastbet) + 50
                totalGain += gain
                if showDetl:
                    self.printStr += '%d && %s赔率%d个进球平局; %d 次最后投%d赚%d' % (count, odds,ball_sum,diff,lastbet,gain)
                    self.printStr += '\n'
                tempTag = count
                bingotime += 1
                if diff > maxcycle:
                    maxcycle = diff
            count -= 1
        if tempTag > maxcycle + 1:
            maxcycle = tempTag
        self.printStr += '%s个进球平局最大周期：%d轮' % ('-'.join([str(i) for i in num]),maxcycle)
        self.printStr += '\n'
        self.printStr += '中的次数：%d' % bingotime
        self.printStr += '\n'
        self.printStr += '现在到达第%d轮' % (tempTag-1)
        self.printStr += '\n'
        self.printStr += "总利润%d" % totalGain
        self.printStr += '\n'
        return True

    # 半场平局
    def analysisHalfDraw(self, showDetl = True, moreth = 0):
        if self.rsp_json == '':
            self.getTeamData()
        maxcycle = 0
        bingotime = 0
        mLen = len(self.rsp_json['list'])
        count = mLen
        tempTag = mLen + 1;
        totalGain = 0
        self.printStr = ''
        
        for i in range(mLen):
            if maxcycle > self.MAXCYCLELIMIT:
                break
            
            htsce = self.rsp_json['list'][mLen-1-i]['HOMEHTSCORE']
            atsce = self.rsp_json['list'][mLen-1-i]['AWAYHTSCORE']
            try:
                sumsce = int(htsce) + int(atsce)
                if htsce == atsce and sumsce >= moreth:
                    diff = tempTag - count
                    odds = 2.15
                    lastbet = 50 * (2 ** (diff-1))
                    gain = lastbet * odds - (2*lastbet) + 50
                    totalGain += gain
                    if showDetl:
                        self.printStr += "%d && %s; %d 次最后投%d赚%d\n" % (count, odds,diff,lastbet,gain)
                    tempTag = count
                    bingotime += 1
                    if diff > maxcycle:
                        maxcycle = diff
            except:
                print 'teamid:%s teamname:%s' % (self.teamid,self.teamname)
                print self.rsp_json['list'][mLen-1-i]
                print 'count=%d' % count
                print 'error for htsce:%s atsce:%s' % (htsce,atsce)
                print '\n'
                return False
            count -= 1
        if tempTag > maxcycle + 1:
            maxcycle = tempTag
        
        self.printStr += '半场平局最大周期：%d轮\n' % maxcycle
        self.printStr += '中的次数：%d\n' % bingotime
        self.printStr += '现在到达第%d轮\n' % (tempTag-1)
        self.printStr += "总利润%d\n" % totalGain
        if maxcycle < self.MAXCYCLELIMIT+1:
            return True
        return False

    # 胜局
    def analysisWin(self):
        if self.rsp_json == '':
            self.getTeamData()
        isWin = True
        odds = 1.0
        mLen = len(self.rsp_json['list'])
        count = mLen;
        tempTag = mLen + 1
        totalGain = 0
        for i in range(mLen):
            if self.rsp_json['list'][mLen-1-i]['RESULT'].find('胜') > 0:
                isWin = True
                if self.rsp_json['list'][mLen-1-i]['lpl_on'] == '胜':
                    if not self.rsp_json['list'][mLen-1-i]['WIN'] == None:
                        odds = string.atof(self.rsp_json['list'][mLen-1-i]['WIN'])
                    else:
                        isWin = False
                elif self.rsp_json['list'][mLen-1-i]['lpl_on'] == '负':
                    if not self.rsp_json['list'][mLen-1-i]['LOST'] == None:
                        odds = string.atof(self.rsp_json['list'][mLen-1-i]['LOST'])
                    else:
                        isWin = False
            else:
                isWin = False
                
            if isWin:
                diff = tempTag - count
                lastbet = 50 * (2 ** (diff-1)) 
                gain = lastbet * odds - (2*lastbet) + 50
                totalGain += gain
                print "%d && %s; %d 次最后投%d赚%d" % (count, odds, diff, lastbet, gain)
                tempTag = count
            count -= 1
        print "总利润%d" % totalGain
    
    def analysisHalfWin(self, showDetl = True):
        if self.rsp_json == '':
            self.getTeamData()
        mLen = len(self.rsp_json['list'])
        
        count = mLen;
        tempTag = mLen + 1;
        maxcycle = 0
        bingotime = 0
        totalGain = 0
        for i in range(mLen):
            mYes = False
            htsce = self.rsp_json['list'][mLen-1-i]['HOMEHTSCORE']
            atsce = self.rsp_json['list'][mLen-1-i]['AWAYHTSCORE']
            if self.teamid == self.rsp_json['list'][mLen-1-i]['HOMETEAMID']:
                if htsce > atsce:
                    mYes = True
            else:
                if htsce < atsce:
                    mYes = True
            if mYes:
                diff = tempTag - count
                odds = 2.15
                lastbet = 50 * (2 ** (diff-1))
                gain = lastbet * odds - (2*lastbet) + 50
                totalGain += gain
                if showDetl:
                    print "%d && %s; %d 次最后投%d赚%d" % (count, odds,diff,lastbet,gain)
                tempTag = count
                bingotime += 1
                if diff > maxcycle:
                    maxcycle = diff
            count -= 1
        if tempTag > maxcycle + 1:
            maxcycle = tempTag
         
        print '半场平最大周期：%d轮' % (maxcycle)
        print '中的次数：%d' % bingotime
        print '现在到达第%d轮' % (tempTag-1)
        print "总利润%d" % totalGain
      
    def toString(self):
        print self.teamid
        print self.teamname
        if self.rsp_json != '':
            print self.rsp_json
        
if __name__ == '__main__':
    testTid = getTeamId(u'布雷斯')
    print testTid
    mTeam = Team(1603)

    if mTeam.isDraw():
        print mTeam.printStr
    # if mTeam.totalBall([0,1]):
    #     print mTeam.printStr

