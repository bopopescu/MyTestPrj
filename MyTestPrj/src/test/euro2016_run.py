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


lgid = 3102
rnd = 1
mmatchid_list = []


#欧洲杯赔率脚本
def setPeilv_zc():
    zcMP.getMatchPinfo_nl(rnd)
    zcMP.getDXpeilv(zcMP.mmatchid_list)
    for i in range(len(zcMP.mmatdetl_list)):
        zcMP.mmatdetl_list[i].extend(zcMP.dapl_list[i])
        print zcMP.mmatdetl_list[i]
    
    fileName = u'欧洲杯-赔率_' + str(rnd) + u'轮.csv'
    mfile = open(fileName, 'wb')
    writer = csv.writer(mfile)
    writer.writerow('时间    主队    比分    客队    胜平负    胜    平    负    大球    小球'.encode('gbk').split('    '))
    for line in zcMP.mmatdetl_list:
        writer.writerow(line)
    mfile.close()

def setPreVsRd_zc():
    if len(zcMP.mmatchid_list) == 0:
        zcMP.getMatchPinfo_nl(rnd)
    zcMP.getPreviousRd(zcMP.mmatchid_list,rnd)
    
def setNbyret_zc():
    if len(zcMP.mmatchid_list) == 0:
        zcMP.getMatchPinfo_nl(rnd)
    zcMP.getNearbyResult(zcMP.teamdict)
    
if __name__ == '__main__':
    zcMP = MatchPage(lgid,rnd)
    setPeilv_zc()
    setPreVsRd_zc()
    setNbyret_zc()