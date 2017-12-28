# -*- coding=utf-8 -*-
'''
Created on 2016-1-3

@author: kingbiwu
'''
import testcsv
import os
import csv

from NBA.NBATeam import NBATeam


def analysis(fname):
    lines = []
    tname = fname.split('_')[-1].split('.')[0]
    mfile = file(fname, 'r')
    mreader = csv.reader(mfile)
    testcsv.writer = open( fname.split('.')[0] + 'result.txt', 'wb')
    testcsv.writer.write(fname + '\n')
    for line in mreader:
        lines.append(line)
    mfile.close()
    print fname
    print len(lines)
    
    lines = lines[1:]
    
    testcsv.totalpast(lines, 8)
    testcsv.totalless(lines, 8)
    testcsv.totalless(lines, 6)
    testcsv.halfWhole(lines, 3, tname)

    testcsv.difscore(lines,(0,5))
    testcsv.difscore(lines,(6,10))
    testcsv.difscore(lines,(11,15))
    testcsv.difscore(lines,(16,20))
    testcsv.difscore(lines,(21,25))
    testcsv.difscore(lines,(26,30))
    testcsv.difscore(lines,(31,100))
    
    testcsv.writer.close()
    
if __name__ == '__main__':
    teamname = ''
    mfilelist = []
    cpath = os.getcwd()
    mypaths = []
    filelists = []
    mypath1 = os.path.join(cpath, '%s%s' % ('2014_2015', u'美国男子职业篮球联赛'))
    mypath2 = os.path.join(cpath,'%s%s'%('2015_2016',u'美国男子职业篮球联赛'))
    mypath3 = os.path.join(cpath,'%s%s'%('2016_2017',u'美国男子职业篮球联赛'))
    mypath4 = os.path.join(cpath, '%s%s' % ('2017_2018', u'美国男子职业篮球联赛'))
    # mypaths.append(mypath1)
    # mypaths.append(mypath2)
    mypaths.append(mypath3)
    mypaths.append(mypath4)

    for i in range(len(mypaths)):
        filelists.append(os.listdir(mypaths[i]))

    myfname1 = ''
    myfname2 = ''

    for inx in range(len(filelists[0])):
        for jnx in range(len(mypaths)):
            tmppath = os.path.join(mypaths[jnx],filelists[jnx][inx])
            tmpObj = NBATeam(tpath=tmppath)
            # tmpObj.totalpast(8,False)
            # tmpObj.totalless(-8,False)
            # tmpObj.subTotal(2,False)
            tmpObj.difscore((6,10),False)
            # tmpObj.teamdifscore((-1,-5),False)
        print '--------------------------------------------'
        # tmppath1 = os.path.join(mypath1,filelist1[mcsv])
        # tmppath2 = os.path.join(mypath2,filelist2[mcsv])
        # tmpObj1 = NBATeam(tpath=tmppath1)
        # tmpObj2 = NBATeam(tpath=tmppath2)
        # tmpObj.difscore((6, 10))
        # tmpObj.difscore((11,20))
        # tmpObj1.totalpast(4,False)
        # tmpObj2.totalpast(4,False)
    # for i in range(len(filelist)):
    #     if filelist[i].find('csv') > -1:
    #         mfilelist.append(filelist[i])
    # for fname in mfilelist:
    #     # analysis(mypath + '/' + fname)
    #     tarpath = mypath + '/' + fname