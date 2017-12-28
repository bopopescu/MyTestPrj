# *-* coding:UTF-8 *-*
'''
Created on 2015-12-23

@author: kingbiwu
'''
from pyquery import PyQuery as pyq
import urllib
import os
import csv
import re
import json
from matchTest import MatchPage


lgid = 3773
<<<<<<< .mine
rnd = 18
||||||| .r6105
rnd = 17
=======
rnd = 2
>>>>>>> .r6137
mmatchid_list = []


def checkErrData(mmatdetl_list):
    for item in mmatdetl_list:
        if item[5] == None or item[6] == None or item[7] == None or item[8] == '1' or item[9] == '1':
            print ' '.join(map(str,item))
                
            return True


#中超赔率脚本
def setPeilv_zc(rnd):
    if os.path.exists(os.path.join(os.getcwd(),'zhongchao')):
        targetdir = os.path.join(os.getcwd(),'zhongchao')
    else:
        os.mkdir(os.path.join(os.getcwd(),'zhongchao'))
    if os.path.isfile(os.path.join(targetdir,u'中超联赛-赔率_' + str(rnd) + u'轮.csv')):
        return
        
    zcMP.getMatchPinfo_nl(rnd)
    zcMP.getDXpeilv(zcMP.mmatchid_list)
   
    for i in range(len(zcMP.mmatdetl_list)):
        zcMP.mmatdetl_list[i].extend(zcMP.dapl_list[i])
#         print zcMP.mmatdetl_list[i]
    if checkErrData(zcMP.mmatdetl_list):
        return 
    
    
        
    zcMP.teamName_list = []
    fileName = os.path.join(targetdir,u'中超联赛-赔率_' + str(rnd) + u'轮.csv')
    mfile = open(fileName, 'wb')
    writer = csv.writer(mfile)
    writer.writerow('时间    主队    比分    客队    胜平负    胜    平    负    大球    小球'.encode('gbk').split('    '))
    for line in zcMP.mmatdetl_list:
        if line[1].find('辽宁盘锦宏运') >= 0:
            line[1] = '辽宁宏运'
#         print line[1].decode('gbk')
        if line[3].find('辽宁盘锦宏运') >= 0:
            line[3] = '辽宁宏运'
        if line[1] not in zcMP.teamName_list:
            zcMP.teamName_list.append(line[1])
        if line[3] not in zcMP.teamName_list:
            zcMP.teamName_list.append(line[3])
#         print line[3].decode('gbk')
        for i in range(len(line)):
            if isinstance(line[i], unicode):
                line[i] = line[i].encode('gbk')
        writer.writerow(line)
    mfile.close()

def setPreVsRd_zc():
    if len(zcMP.mmatchid_list) == 0:
        zcMP.getMatchid_nl(lgid, rnd)
    zcMP.getPreviousRd(zcMP.mmatchid_list)
    zcMP.writePreviousRd()
    
def setNbyret_zc():
    if len(zcMP.mmatchid_list) == 0:
        zcMP.getMatchid_nl(lgid, rnd)
    zcMP.getNearbyResult(zcMP.teamdict)
    zcMP.writeNearbyResult()
    
if __name__ == '__main__':
    zcMP = MatchPage(lgid)
    for i in range(1,zcMP.countRnd+1):
        setPeilv_zc(i)

    setPreVsRd_zc()
    setNbyret_zc()