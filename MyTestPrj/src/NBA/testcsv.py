# -*- coding=utf-8 -*-
'''
Created on 2015-12-24

@author: kingbiwu
'''
import csv
import os
import string
import math
from logging import codecs


writer = None
MAXCYCLELIMIT = 10

def totalpast(lst, pt = 8.0):
    count = 0
    maxcount = 0
    bingotime = 0
    lst_ret = []
    if len(lst) > 0:
        for i in range(len(lst)):
            count += 1
            if string.atof(lst[-1-i][12]) > pt:
                lst_ret.append((lst[-1-i][12],count))
                if count > maxcount:
                    maxcount = count
                count = 0
                bingotime += 1
    if count > maxcount:
                    maxcount = count
    print '%0.1f分最大周期：%d轮' % (pt,maxcount)
    print '中的次数：%d' % bingotime
    print '现在到达第%d轮' % count
    print lst_ret
    print ''
    ret_str = '%0.1f分最大周期：%d轮' % (pt,maxcount) + '\n'
    ret_str += '中的次数：%d' % bingotime + '\n'
    ret_str += '现在到达第%d轮' % count + '\n'
    ret_str += str(lst_ret) + '\n\n'
    writer.write(ret_str)
    
def totalless(lst, pt = 8.0):
    count = 0
    maxcount = 0
    bingotime = 0
    lst_ret = []
    if len(lst) > 0:
        for i in range(len(lst)):
            count += 1
            if string.atof(lst[-1-i][12]) + pt < 0:
                lst_ret.append((lst[-1-i][12],count))
                if count > maxcount:
                    maxcount = count
                count = 0
                bingotime += 1
    if count > maxcount:
                    maxcount = count
    # print '%0.1f分最大周期：%d轮' % (pt,maxcount)
    # print '中的次数：%d' % bingotime
    # print '现在到达第%d轮' % count
    # print lst_ret
    # print ''
    ret_str = '-%0.1f分最大周期：%d轮' % (pt,maxcount) + '\n'
    ret_str += '中的次数：%d' % bingotime + '\n'
    ret_str += '现在到达第%d轮' % count + '\n'
    ret_str += str(lst_ret) + '\n\n'
    writer.write(ret_str)

def difscore(lst, diftuple = (0,5), showDetl = True):
    mLen = len(lst)
    printStr = ''
    maxcycle = 0
    bingotime = 0
    count = 0
    maxcount = 1
    totalGain = 0
    odds = 3.0
    lst_ret = []

    if mLen < 1:
        return

    for i in range(mLen-1):
        if maxcycle > MAXCYCLELIMIT:
            break
        count += 1
        if abs(string.atof(lst[-1-i][10])) <= diftuple[1] and abs(string.atof(lst[-1-i][10])) >= diftuple[0]:
            # lst_ret.append((lst[-1-i][10],count))
            lastbet = 50 * (2 ** (count - 1))
            gain = lastbet * odds - (2 * lastbet) + 50
            totalGain += gain
            if showDetl:
                printStr += "%d && %s; %d 次最后投%d赚%d\n" % (i+1, odds, count, lastbet, gain)
            if count > maxcount:
                maxcount = count
            count = 0
            bingotime += 1
    if count > maxcount:
        maxcount = count
    
    # print '分差%s分最大周期：%s轮' % (diftuple,maxcount)
    # print '中的次数：%d' % bingotime
    # print '现在到达第%d轮' % count
    # print lst_ret
    # print ''
    printStr += '分差%s分最大周期：%s轮' % (diftuple,maxcount) + '\n'
    printStr += '中的次数：%d' % bingotime + '\n'
    printStr += '现在到达第%d轮' % count + '\n'
    print printStr
    # writer.write(ret_str)
    
def teamdifscore(lst, diftuple = (0,5), tname = ''):
    count = 0
    maxcount = 0
    bingotime = 0
    lst_ret = []
    if len(lst) > 0:
        for i in range(len(lst)):
            count += 1
            if abs(string.atof(lst[-1-i][10])) <= diftuple[1] and abs(string.atof(lst[-1-i][10])) >= diftuple[0]:
                if lst[-1-i][3].find(tname) > 0 and string.atof(lst[-1-i][10]) < 0:
                    lst_ret.append((lst[-1-i][10],count))
                    if count > maxcount:
                        maxcount = count
                    count = 0
                    bingotime += 1
                elif lst[-1-i][3].find(tname) < 0 and string.atof(lst[-1-i][10]) > 0:
                    lst_ret.append((lst[-1-i][10],count))
                    if count > maxcount:
                        maxcount = count
                    count = 0
                    bingotime += 1 
                
    if count > maxcount:
                    maxcount = count
    
    print '分差%s分最大周期：%s轮' % (diftuple,maxcount)
    print '中的次数：%d' % bingotime
    print '现在到达第%d轮' % count
    print lst_ret
    print ''
    ret_str = '分差%s分最大周期：%s轮' % (diftuple,maxcount) + '\n'
    ret_str += '中的次数：%d' % bingotime + '\n'
    ret_str += '现在到达第%d轮' % count + '\n'
    ret_str += str(lst_ret) + '\n\n'
    # writer.write(ret_str)
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
    
def analysis(mpath):
    pass
    
if __name__ == '__main__':
    teamname = u'爵士'
    lines = []
    cpath = os.getcwd()
    mypath = os.path.join(cpath, '%s%s' % ('2015_2016', u'美国男子职业篮球联赛'))
    myfname = ''
    filelist = os.listdir(mypath)
#     print filelist
    for fname in filelist:
        if fname.find(teamname) > 0 and fname.find('csv') > 0:
            print fname
            myfname = mypath + '/' + fname
    print myfname
    mfile = file(myfname, 'r')
    mreader = csv.reader(mfile)
    # writer = open(myfname.split('.')[0] + 'result.txt', 'wb')
    # writer.write(myfname + u'\n')
    # line: NBA 常规赛 04-14 10:30 犹他爵士 96-101 洛杉矶湖人 57-42 6.5 输 193.5 5.0 197.0 3.5
    for line in mreader:
        lines.append(line)
    mfile.close()
    

    difscore(lines, (6,10))
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