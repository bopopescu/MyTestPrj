# -*- coding=utf-8 -*-
'''
Created on 2015-12-24

@author: kingbiwu
'''
import csv
import os
import string
import re
import sys


class NBATeam(object):
    MAXCYCLELIMIT = 100

    def __init__(self, teamname = '', tpath='', lgid=366):
        self.printStr = ''
        self.teamname = teamname
        self.tpath = tpath
        self.data = []
        self.getData(self.tpath)
        self.lgid = lgid

    #   总分分差分析
    def difscore(self, diftuple=(0, 5), showDetl=True):
        fdata = self.data[1:]
        mLen = len(fdata)
        bingotime = 0
        count = 0
        maxcount = 1
        totalGain = 0
        odds = 3.0
        self.printStr = ''
        if mLen < 1:
            return

        for i in range(mLen):
            if maxcount > self.MAXCYCLELIMIT:
                break
            count += 1
            if abs(string.atof(fdata[-1 - i][10])) <= diftuple[1] and abs(string.atof(fdata[-1 - i][10])) >= diftuple[0]:
                # lst_ret.append((lst[-1-i][10],count))
                lastbet = 50 * (2 ** (count - 1))
                gain = lastbet * odds - (2 * lastbet) + 50
                totalGain += gain
                if showDetl:
                    self.printStr += "%d && %s; %d 次最后投%d赚%d\n" % (i + 1, odds, count, lastbet, gain)
                if count > maxcount:
                    maxcount = count
                count = 0
                bingotime += 1
        if count > maxcount:
            maxcount = count

        self.printStr += '分差%s分最大周期：%s轮' % (diftuple, maxcount) + '\n'
        self.printStr += '中的次数：%d' % bingotime + '\n'
        self.printStr += '现在到达第%d轮' % count + '\n'
        if maxcount <= self.MAXCYCLELIMIT:
            print self.printStr

    # 总分最大
    def totalpast(self, pt=8.0, showDetl=True):
        fdata = self.data[1:]
        mLen = len(fdata)
        mLen = len(fdata)
        bingotime = 0
        count = 0
        maxcount = 1
        totalGain = 0
        odds = 3.0
        self.printStr = ''

        for i in range(mLen):
            if maxcount > self.MAXCYCLELIMIT:
                break
            count += 1
            if string.atof(fdata[-1 - i][12]) > pt:

                lastbet = 50 * (2 ** (count - 1))
                gain = lastbet * odds - (2 * lastbet) + 50
                totalGain += gain
                if showDetl:
                    self.printStr += "%d && %s; %d 次最后投%d赚%d\n" % (i + 1, odds, count, lastbet, gain)

                if count > maxcount:
                    maxcount = count
                count = 0
                bingotime += 1
        if count > maxcount:
            maxcount = count

        self.printStr += '%0.1f分最大周期：%d轮' % (pt, maxcount) + '\n'
        self.printStr += '中的次数：%d' % bingotime + '\n'
        self.printStr += '现在到达第%d轮' % count + '\n'
        print self.printStr

    # 总分小
    def totalless(self, pt = -8.0, showDetl=True):
        fdata = self.data[1:]
        mLen = len(fdata)
        mLen = len(fdata)
        bingotime = 0
        count = 0
        maxcount = 1
        totalGain = 0
        odds = 3.0
        self.printStr = ''

        for i in range(mLen):
            if maxcount > self.MAXCYCLELIMIT:
                break
            count += 1
            if string.atof(fdata[-1 - i][12]) < pt:

                lastbet = 50 * (2 ** (count - 1))
                gain = lastbet * odds - (2 * lastbet) + 50
                totalGain += gain
                if showDetl:
                    self.printStr += "%d && %s; %d 次最后投%d赚%d\n" % (i + 1, odds, count, lastbet, gain)

                if count > maxcount:
                    maxcount = count
                count = 0
                bingotime += 1
        if count > maxcount:
            maxcount = count

        self.printStr += '%0.1f分最大周期：%d轮' % (pt, maxcount) + '\n'
        self.printStr += '中的次数：%d' % bingotime + '\n'
        self.printStr += '现在到达第%d轮' % count + '\n'
        print self.printStr



    # 单节总分最大
    def subTotal(self, pt=1, showDetl=True):
        fdata = self.data[1:]
        mLen = len(fdata)
        bingotime = 0
        count = 0
        maxcount = 1
        totalGain = 0
        odds = 3.0
        self.printStr = ''


        # for i in range(mLen):
        #     myindexs = []
        #     sce1 = sum([string.atoi(x) for x in fdata[-1 - i][13].strip().split('-')])
        #     sce2 = sum([string.atoi(x) for x in fdata[-1 - i][14].strip().split('-')])
        #     sce3 = sum([string.atoi(x) for x in fdata[-1 - i][15].strip().split('-')])
        #     sce4 = sum([string.atoi(x) for x in fdata[-1 - i][16].strip().split('-')])
        #     for index,item in list(enumerate([sce1,sce2,sce3,sce4],start=1)):
        #         if max([sce1,sce2,sce3,sce4]) == item:
        #             myindexs.append(index)
        #
        #     print '%d/%d/%d/%d 最大：第%s节'%(sce1,sce2,sce3,sce4,myindexs)

        for i in range(mLen):
            if maxcount > self.MAXCYCLELIMIT:
                break
            count += 1
            myindexs = []
            sceList = []
            for x in range(4):
                if fdata[-1 - i][13+x] == ' -':
                    # print fdata[-1 - i][0]
                    sceList.append(0)
                else:
                    sceList.append(sum([string.atoi(y) for y in fdata[-1 - i][13+x].strip().split('-')]))

            # self.printStr += '%d/%d/%d/%d \n' % tuple(sceList)
            if max(sceList) == sceList[pt-1]:

                lastbet = 50 * (2 ** (count - 1))
                gain = lastbet * odds - (2 * lastbet) + 50
                totalGain += gain
                if showDetl:
                    self.printStr += "%d && %s; %d 次最后投%d赚%d\n" % (i + 1, odds, count, lastbet, gain)

                if count > maxcount:
                    maxcount = count
                count = 0
                bingotime += 1
        if count > maxcount:
            maxcount = count

        self.printStr += '%d节最高得分最大周期：%d轮' % (pt, maxcount) + '\n'
        self.printStr += '中的次数：%d' % bingotime + '\n'
        self.printStr += '现在到达第%d轮' % count + '\n'
        print self.printStr

    # 主队分差
    def teamdifscore(self, diftuple = (0,5), showDetl=True):
        fdata = self.data[1:]
        mLen = len(fdata)
        bingotime = 0
        count = 0
        maxcount = 1
        totalGain = 0
        odds = 3.0
        self.printStr = ''
        if mLen < 1:
            return

        for i in range(mLen):
            isBingo = False
            if maxcount > self.MAXCYCLELIMIT:
                break
            count += 1
            if abs(string.atof(fdata[-1 - i][10])) <= diftuple[1] and abs(string.atof(fdata[-1 - i][10])) >= diftuple[
                0]:

                # 主队匹配到
                if fdata[-1-i][5].decode('gbk').find(self.teamname) > -1:
                    difsce = string.atof(fdata[-1-i][10])
                    if difsce >= diftuple[0] and difsce <= diftuple[1]:
                        isBingo = True
                # 客队匹配到
                else:
                    difsce = string.atof(fdata[-1 - i][10]) * -1
                    if difsce >= diftuple[0] and difsce <= diftuple[1]:
                        isBingo = True
                if isBingo == False:
                    continue
                # lst_ret.append((lst[-1-i][10],count))
                lastbet = 50 * (2 ** (count - 1))
                gain = lastbet * odds - (2 * lastbet) + 50
                totalGain += gain
                if showDetl:
                    self.printStr += "%d && %s; %d 次最后投%d赚%d\n" % (i + 1, odds, count, lastbet, gain)
                if count > maxcount:
                    maxcount = count
                count = 0
                bingotime += 1
        if count > maxcount:
            maxcount = count

        self.printStr += '胜%s分最大周期：%s轮' % (diftuple, maxcount) + '\n'
        self.printStr += '中的次数：%d' % bingotime + '\n'
        self.printStr += '现在到达第%d轮' % count + '\n'
        if maxcount <= self.MAXCYCLELIMIT:
            print self.printStr


    # 负胜——3
    def halfWhole(lst, type, tname):
        count = 0
        role = 0 #0为客，1为主
        maxcount = 0
        bingotime = 0
        lst_ret = []
        if len(lst) > 0:
            for i in range(len(lst)):
                count += 1
                hdif = string.atoi(lst[-1-i][6].split('-')[1]) - string.atoi(lst[-1-i][6].split('-')[0])
                #type = 3
                if lst[-1-i][3].find(tname) > 0:
                    role = 0
                else:
                    role = 1
                if role == 0:
                    if hdif > 0 and string.atof(lst[-1-i][10]) < 0:
                        lst_ret.append((lst[-1-i][6],count))
                        if count > maxcount:
                            maxcount = count
                        count = 0
                        bingotime += 1
                if role == 1:
                    if hdif < 0 and string.atof(lst[-1-i][10]) > 0:
                        lst_ret.append((lst[-1-i][6],count))
                        if count > maxcount:
                            maxcount = count
                        count = 0
                        bingotime += 1
        if count > maxcount:
                        maxcount = count
        ret_str = '半全场负胜最大周期：%s轮' % maxcount + '\n'
        ret_str += '中的次数：%d' % bingotime + '\n'
        ret_str += '现在到达第%d轮' % count + '\n'
        ret_str += str(lst_ret) + '\n\n'
        print ret_str
        # writer.write(ret_str)

    def getData(self, tgtpath = ''):

        if tgtpath == '':
            cpath = os.getcwd()
            mypathdir = os.path.join(cpath, '%s%s' % ('2016_2017', u'美国男子职业篮球联赛'))
            mypath = ''
            filelist = os.listdir(mypathdir)
            #     print filelist
            for fname in filelist:
                if fname.find(self.teamname) > -1 and fname.find('csv') > -1:
                    # print fname
                    tgtpath = mypathdir + '/' + fname


        lines = []
        dn,fn = os.path.split(tgtpath)
        mreg = re.match('(.+)\d{4}_\d{4}.csv',fn)
        print fn

        self.teamname = mreg.group(1)
        mfile = file(tgtpath, 'r')
        mreader = csv.reader(mfile)

        # line: NBA 常规赛 04-14 10:30 犹他爵士 96-101 洛杉矶湖人 57-42 6.5 输 193.5 5.0 197.0 3.5
        for line in mreader:
            self.data.append(line)
        mfile.close()
        print tgtpath
    
if __name__ == '__main__':

    objTeam = NBATeam(u'雷霆')
    # objTeam.totalless(-4)
    # objTeam.totalpast(8.0)
    # objTeam.subTotal(2,True)
    objTeam.difscore((11,20))
    # teamdifscore(lines, (6,10), teamname)
#     totalpast(lines, 8)
#     totalless(lines, 8)
#     totalless(lines, 6)
#     difscore(lines,(0,5))
#     difscore(lines,(6,10))
#     difscore(lines,(11,15))
#     difscore(lines,(16,20))
#     difscore(lines,(21,25))
#     difscore(lines,(26,30))
#     difscore(lines,(31,100))
#     writer.close()