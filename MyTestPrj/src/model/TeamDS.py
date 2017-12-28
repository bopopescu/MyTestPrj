# *-* coding:UTF-8 *-*
'''
Created on 2016年5月24日

@author: Administrator
'''
import traceback
import urllib2
import string
import re
import pdb
from pyquery import PyQuery as pyq

class TeamDS(object):
    '''
    classdocs
    '''
    urldomain = "http://www.dszuqiu.com"

    def __init__(self, tid):
        '''
        Constructor
        '''
        self.printStr = ''
        self.teamid = str(tid)
        self.teamname = ''
        self.rsp = ''
        self.rsps = []
        self.teamData = []
#         self.getTeamData()
        self.writelines = []
    
    def getTeamData(self):

        strParams = "/team/"
        strParams += self.teamid
        url = self.urldomain + strParams
        print 'url:%s' % url
        send_headers = {
            'Host': 'www.dszuqiu.com',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Connection':'keep-alive'
        }
        req = urllib2.Request(url,headers=send_headers)
        # self.writelines.append(url)
        self.rsp = urllib2.urlopen(req).read()
        # print self.rsp
   
        if self.rsp != '':
            mpyq = pyq(self.rsp)
            print 'title:%s' % mpyq('head title').text()
            #町田泽维亚（日本） - DS足球
            self.teamname = mpyq('head title').text().split('-')[0].split(u'（')[0]
            self.printStr = self.teamname.encode('utf-8') + '\n'
            self.writelines.append(mpyq('head title').text())
#           判断有多少分页
            pagelis = mpyq('ul.pagination li')
            if pagelis.length == 0:
                self.getTeamPageData(url)
                return
             
            for i in range(pagelis.length-1):
                purl = self.urldomain + pagelis.eq(i).find('a').attr('href')
                self.getTeamPageData(purl)

            # for item in self.teamData:

    def getTeamPageData(self, url):
        print 'url:%s' % url
        send_headers = {
            'Host': 'www.dszuqiu.com',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Connection':'keep-alive'
        }
        req = urllib2.Request(url,headers=send_headers)
        tmp_rsp = urllib2.urlopen(req).read()
        if tmp_rsp != '' or tmp_rsp != None:
            mpyq = pyq(tmp_rsp)
            sq_tables = mpyq('section.content.active table.live-list-table')    #可能会有2个table，未开始和已结束
            target_tb = sq_tables.eq(-1)
            # trs = mpyq('section.content.active table.live-list-table tbody tr')   #error
            trs = target_tb.find('tbody tr')
            for i in range(trs.length):
                tds = trs.eq(i).children() #英冠 2016/10/29 22:00 [10] 利茲 v 伯顿阿尔比恩 [15] （ -0.5 / 2.0,2.5 / 10.5 ） - -- - -- - -- - -- 析
                if tds.eq(10).text().find('-') == -1:
                    tmplist = [tds.eq(j).text() for j in range(tds.length)]
                    self.teamData.append(tmplist)
    
    def totalCorner(self, cner = [9,10,11], showDetl = True):
        if self.teamData == []:
            self.getTeamData()
        maxcycle = 0
        bingotime = 0
        mLen = len(self.teamData)
        count = mLen
        tempTag = mLen + 1;
        totalGain = 0
        pattern = r'(\d+ : \d+).*'

        for i in range(mLen):
            try:
                cornerdata = re.match(pattern,self.teamData[mLen-1-i][10]).group(1)
                corner_sum = sum([int(i) for i in cornerdata.split(':')])
            except Exception,e:
                print traceback.format_exc()
                print 'Excute to the line %s' % str(mLen-1-i)
                print self.teamData[mLen-1-i]
                return
            # print '%d:%s|%s' % (i,self.teamData[mLen-1-i][-3],cornerdata)

            if corner_sum in cner:
                diff = tempTag - count
                odds = 2.75
                lastbet = 50 * (2 ** (diff-1))
                gain = lastbet * odds - (2*lastbet) + 50
                totalGain += gain
                if showDetl:
                    self.printStr += '%d && %s赔率%d个角球; %d 次最后投%d赚%d' % (count, odds,corner_sum,diff,lastbet,gain)
                    self.printStr += '\n'
                    self.writelines.append("%d && %s赔率%d个角球; %d 次最后投%d赚%d" % (count, odds,corner_sum,diff,lastbet,gain))
                tempTag = count
                bingotime += 1
                if diff > maxcycle:
                    maxcycle = diff
            count -= 1
        if tempTag > maxcycle + 1:
            maxcycle = tempTag
        self.printStr += '%s个角球球最大周期：%d轮' % ('-'.join([str(i) for i in cner]),maxcycle)
        self.printStr += '\n'
        self.printStr += '中的次数：%d' % bingotime
        self.printStr += '\n'
        self.printStr += '现在到达第%d轮' % (tempTag-1)
        self.printStr += '\n'
        self.printStr += "总利润%d" % totalGain
        self.printStr += '\n'
        self.writelines.append('%s个角球球最大周期：%d轮' % ('-'.join([str(i) for i in cner]),maxcycle))
        self.writelines.append('中的次数：%d' % bingotime)
        self.writelines.append('现在到达第%d轮' % (tempTag-1))
        self.writelines.append("总利润%d" % totalGain)
        
    def totalBall(self, num = [2], showDetl = True):
        if self.teamData == []:
            self.getTeamData()
        maxcycle = 0
        bingotime = 0
        mLen = len(self.teamData)
        count = mLen
        tempTag = mLen + 1;
        totalGain = 0
        pattern = r'(\d+ : \d+).*'

        for i in range(mLen):
            try:
                balldata = re.match(pattern,self.teamData[mLen-1-i][4]).group(1)
                ball_sum = sum([int(i) for i in balldata.split(':')])
            except Exception,e:
                print traceback.format_exc()
                print 'Excute to the line %s' % str(mLen-1-i)
                print self.teamData[mLen-1-i]
                return
            # print '%d:%s|%s' % (i,self.teamData[mLen-1-i][-3],cornerdata)

            if ball_sum in num:
                diff = tempTag - count
                odds = 2
                lastbet = 50 * (2 ** (diff-1))
                gain = lastbet * odds - (2*lastbet) + 50
                totalGain += gain
                if showDetl:
                    self.printStr += '%d && %s赔率%d个进球; %d 次最后投%d赚%d' % (count, odds,ball_sum,diff,lastbet,gain)
                    self.printStr += '\n'
                    self.writelines.append("%d && %s赔率%d个进球; %d 次最后投%d赚%d" % (count, odds,ball_sum,diff,lastbet,gain))
                tempTag = count
                bingotime += 1
                if diff > maxcycle:
                    maxcycle = diff
            count -= 1
        if tempTag > maxcycle + 1:
            maxcycle = tempTag
        self.printStr += '%s个进球最大周期：%d轮' % ('-'.join([str(i) for i in num]),maxcycle)
        self.printStr += '\n'
        self.printStr += '中的次数：%d' % bingotime
        self.printStr += '\n'
        self.printStr += '现在到达第%d轮' % (tempTag-1)
        self.printStr += '\n'
        self.printStr += "总利润%d" % totalGain
        self.printStr += '\n'
        self.writelines.append('%s个进球最大周期：%d轮' % ('-'.join([str(i) for i in num]),maxcycle))
        self.writelines.append('中的次数：%d' % bingotime)
        self.writelines.append('现在到达第%d轮' % (tempTag-1))
        self.writelines.append("总利润%d" % totalGain)

    def isDraw(self, num = range(0,51,2), showDetl = True):
        if self.teamData == []:
            self.getTeamData()
        maxcycle = 0
        bingotime = 0
        mLen = len(self.teamData)
        count = mLen
        tempTag = mLen + 1;
        totalGain = 0
        pattern = r'(\d+ : \d+).*'

        for i in range(mLen):
            try:
                balldata = re.match(pattern,self.teamData[mLen-1-i][4]).group(1)
                scores = [int(i) for i in balldata.split(':')]
                ball_sum = sum(scores)
            except Exception,e:
                print traceback.format_exc()
                print 'Excute to the line %s' % str(mLen-1-i)
                print self.teamData[mLen-1-i]
                return
            # print '%d:%s|%s' % (i,self.teamData[mLen-1-i][-3],cornerdata)

            if scores[0] == scores[1] and ball_sum in num:
                diff = tempTag - count
                odds = 2
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

    def isDiffBall(self, num = [1], showDetl = True):
        if self.teamData == []:
            self.getTeamData()
        maxcycle = 0
        bingotime = 0
        mLen = len(self.teamData)
        count = mLen
        tempTag = mLen + 1;
        totalGain = 0
        pattern = r'(\d+ : \d+).*'

        for i in range(mLen):
            try:
                # p1 = re.compile(r'^(\d )?(\d )?(\[\d+\] )?(.*)')
                # p2 = re.compile(r'^(\S*)?( \[\d+\])*( \d)?( \d)?$')
                homeName = self.teamData[mLen-1-i][3]
                awayName = self.teamData[mLen-1-i][5]
                # 获取全场进球，以及主客队进球
                balldata = re.match(pattern,self.teamData[mLen-1-i][4]).group(1)
                scores = [int(i) for i in balldata.split(':')]
                if homeName.find(self.teamname) > -1:
                    realDiff = scores[0] - scores[1]
                else:
                    realDiff = scores[1] - scores[0]

            except Exception,e:
                print traceback.format_exc()
                print 'Excute to the line %s' % str(mLen-1-i)
                print self.teamData[mLen-1-i]
                return
            # print '%d:%s|%s' % (i,self.teamData[mLen-1-i][-3],cornerdata)

            if realDiff in num:
                diff = tempTag - count
                odds = 2
                lastbet = 50 * (2 ** (diff-1))
                gain = lastbet * odds - (2*lastbet) + 50
                totalGain += gain
                if showDetl:
                    self.printStr += '%d && %s赔率%d个进球差值; %d 次最后投%d赚%d' % (count, odds,realDiff,diff,lastbet,gain)
                    self.printStr += '\n'
                tempTag = count
                bingotime += 1
                if diff > maxcycle:
                    maxcycle = diff
            count -= 1
        if tempTag > maxcycle + 1:
            maxcycle = tempTag
        self.printStr += '%s个进球差值最大周期：%d轮' % ('-'.join([str(i) for i in num]),maxcycle)
        self.printStr += '\n'
        self.printStr += '中的次数：%d' % bingotime
        self.printStr += '\n'
        self.printStr += '现在到达第%d轮' % (tempTag-1)
        self.printStr += '\n'
        self.printStr += "总利润%d" % totalGain
        self.printStr += '\n'

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

    def analysisTeamWLD(self, wld = 1):
        if self.rsp_json == '':
            self.getTeamData()
            
        if wld == 3:
            self.analysisWin()
        elif wld == 1:
            self.analysisDraw()
        else:
            pass
        
    def analysisDraw(self):
        if self.rsp_json == '':
            self.getTeamData()
        mLen = len(self.rsp_json['list'])
        count = mLen;
        tempTag = mLen + 1;
        totalGain = 0
        for i in range(mLen):
            if self.rsp_json['list'][mLen-1-i]['lpl_on'] == '平':
                diff = tempTag - count
                odds = 3.0
                if not self.rsp_json['list'][mLen-1-i]['DRAW'] == None:
                    odds = string.atof(self.rsp_json['list'][mLen-1-i]['DRAW'])
                lastbet = 50 * (2 ** (diff-1))
                gain = lastbet * odds - (2*lastbet) + 50
                totalGain += gain
                print "%d && %s; %d 次最后投%d赚%d" % (count, odds,diff,lastbet,gain)
                tempTag = count
            count -= 1
        print "总利润%d" % totalGain
        
    def analysisHalfDraw(self, showDetl = True):
        if self.rsp_json == '':
            self.getTeamData()
        mLen = len(self.rsp_json['list'])
        count = mLen;
        tempTag = mLen + 1;
        maxcycle = 0
        bingotime = 0
        totalGain = 0
        for i in range(mLen):
            htsce = self.rsp_json['list'][mLen-1-i]['HOMEHTSCORE']
            atsce = self.rsp_json['list'][mLen-1-i]['AWAYHTSCORE']
    
            if htsce == atsce:
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
    
    def writedown(self, mpath):

        filename = self.teamname + '.txt'
        wfile = open(mpath +  '\\' + filename, 'wb')
        
        for cont in self.writelines:
            wfile.write(cont+'\n')
        wfile.close()
        
if __name__ == '__main__':
    mTeam = TeamDS('6513')
    # mTeam.getTeamData()
    # for item in mTeam.teamData:
    #     print item
#     mTeam.TotalCorner(range(0,9))
#     mTeam.TotalCorner(range(9,12))
#     mTeam.TotalCorner(range(1,9))
    mTeam.isDiffBall([-1])
    print mTeam.printStr
#     mTeam.writedown('E:\个人\竞猜数据\DS足球')
#     mTeam.TotalCorner(range(9,12))
#     for item in mTeam.teamData:
#         print item
#     print mTeam.rsp_json['list'][97]['WIN']
#     mTeam.analysisTeamTotalBall(0)
    

