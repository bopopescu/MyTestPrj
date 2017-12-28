# *-* coding:UTF-8 *-*
'''
Created on 2015-12-23

@author: kingbiwu
'''
import urllib2
import urllib
from pyquery import PyQuery as pyq
import csv
import string
import os
from model.gzipHandle import gzdecode

class NBALeague():
    mhost = 'http://liansai.500.com'
    
    def __init__(self, lgid=366):
        self.lgid = lgid
        self.teamidlist = []
        self.datalist_rf = []
        self.datalist_zf = []
        
    def loadData_zf(self, teamid = 1):
        url_zf = self.mhost + '/lq/' + str(self.lgid) + '/team/' + str(teamid) + '/zongfen/'
        print url_zf
        data = urllib2.urlopen(url_zf).read()
        mpyq = pyq(data)
        
        pgtitle = mpyq('h2.title').text().split('-')[0]#2016/2017 美国男子职业篮球联赛
        tname = mpyq('h2.title').text().split('-')[1]#洛杉矶湖人
        title = pgtitle.replace(" ", "").replace("/","_").replace("-","_")#2016_2017美国男子职业篮球联赛
        
        print title
        
        zftrs = mpyq('table.tb tr')
#       阶段 赛事 时间 客队 比分 主队 半场 总分盘 盘路 分析
        for i in range(1,zftrs.length):
            print zftrs.eq(i).text() #NBA 季前赛 10-22 10:00 菲尼克斯太阳 98-94 洛杉矶湖人 51-43 -2.5 输 析 亚 欧
            line = zftrs.eq(i).text().split(' ')
            line[2] = ' '.join([line[2],line[3]])
            line.pop(3)
            self.datalist_zf.append(line[:9])
    
    def loadData_rf(self, teamid = 1):
        url_rf = self.mhost + '/lq/' + str(self.lgid) + '/team/' + str(teamid) + '/rangfen/'
        print url_rf
        data = urllib2.urlopen(url_rf).read()
        mpyq = pyq(data)
        
        pgtitle = mpyq('h2.title').text().split('-')[0]#2016/2017 美国男子职业篮球联赛
        tname = mpyq('h2.title').text().split('-')[1]#洛杉矶湖人
        title = pgtitle.replace(" ", "").replace("/","_").replace("-","_")#2016_2017美国男子职业篮球联赛
        
        print title
        
        rftrs = mpyq('table.tb tr')

        for i in range(1,rftrs.length):
            print rftrs.eq(i).text() #NBA 季前赛 10-22 10:00 菲尼克斯太阳 98-94 洛杉矶湖人 51-43 -2.5 输 析 亚 欧
            line = rftrs.eq(i).text().split(' ')
            line[2] = ' '.join([line[2],line[3]])
            line.pop(3)
            self.datalist_rf.append(line[:8])
            
    def mergedata(self):
        for i in range(1,len(self.datalist_zf)):
            print i


def getStat(mid):
    import gzip
    import StringIO
    url_stat = "http://odds.500.com/lq/stat.php?id=" + mid
    request = urllib2.Request(url_stat)
    request.add_header('Accept-encoding','gzip')
    opener = urllib2.build_opener()
    mFile = opener.open(request)
    isGzip = mFile.headers.get('Content-Encoding')
    if isGzip == 'gzip':
        compresseddata = mFile.read()
        compressedstream = StringIO.StringIO(compresseddata)
        gzipper = gzip.GzipFile(fileobj=compressedstream)
        stat_rsp = gzipper.read()
    else:
        stat_rsp = mFile.read()

    stpyq = pyq(stat_rsp)

    subSceList = []

    # 后面两个tr才是单节比分项
    tr_a = stpyq('tr#bf_away')
    tr_h = stpyq('tr#bf_home')
    tds_a = tr_a.find('td')
    tds_h = tr_h.find('td')

    # td项去头去尾
    for i in range(tds_a.length-2):
        tmpSubSce = ' %s-%s'%(tds_a.eq(i+1).text(),tds_h.eq(i+1).text())
        subSceList.append(tmpSubSce)
        # print tmpSubSce
    return subSceList

def loadlqData(year = 301, team = 22):
    year = str(year)
    team = str(team)
    url_rangfen = "http://liansai.500.com/lq/" + year + "/team/" + team + "/rangfen/"
    url_zongfen = "http://liansai.500.com/lq/" + year + "/team/" + team + "/zongfen/"

    print url_rangfen
#     rsp = urllib2.urlopen(url_rangfen)
#     rsp_ = urllib2.urlopen(url_zongfen)
    rf_rsp = urllib.urlopen(url_rangfen).read()
    zf_rsp = urllib.urlopen(url_zongfen).read()
    
    head_str = []
    content_str = []
    list_txt_str = []
    list_content = []
    list_content_ = []
    
    title = ''
    score_list = []
    
#     rf_rsp = rf_rsp.decode('gbk')
    rfpyq = pyq(rf_rsp)
    zfpyq = pyq(zf_rsp)
    # print rf_rsp.decode('gbk')


    title = rfpyq('h2.title').text().split('-')[0]
    tname = rfpyq('h2.title').text().split('-')[1]
    title = title.replace(" ", "").replace("/","_").replace("-","_")



    rftrs = rfpyq('table.tb tr')
    zftrs = zfpyq('table.tb tr')
      
    head_str.extend(rftrs.eq(0).text().split(' '))
#     print ' '.join(head_str)
    for i in range(rftrs.length-1):
 
        tmplist = []
        tds = rftrs.eq(i+1).find('td')
        # 比赛对应分析url
        shuju_url = tds.eq(-1).find('a').eq(0).attr['href']
        stat_url = shuju_url.replace('shuju','stat')

        for j in range(tds.length-1):
            tmplist.append(tds.eq(j).text().encode('gbk'))
        tmplist[0] = stat_url
        list_content.append(tmplist)
     
 
    for i in range(zftrs.length-1):
 
        tmplist = []
        tds = zftrs.eq(i+1).find('td')
 
        for j in range(tds.length-1):
            tmplist.append(tds.eq(j).text().encode('gbk'))
        list_content_.append(tmplist)   
     
    head_str.pop(-1)
    head_addlist = [u'总分盘', u'主客分差', u'总分', u'总分总分盘差']
    head_str.extend(head_addlist)#.append(u'分差')#.append(u'总分').append(u'总分-总分盘')
#     
    zongfen_data = []
    for item in list_content_:
        zongfen_data.append(item[7])
      
    for i in range(len(list_content)):
        list_content[i].append(zongfen_data[i])
#        subdata
        away = string.atof(list_content[i][4].split('-')[0])
        home = string.atof(list_content[i][4].split('-')[1])
        total = away + home
        dif = home - away
          
        if zongfen_data[i] == '-':
            total_dif = total - 0
        else:
            total_dif = total - string.atof(zongfen_data[i])

        import re

        mid = re.match('.*id=([\d]+)',list_content[i][0]).group(1)
        tmpSubSceList = getStat(mid)

        list_content[i].append(dif)
        list_content[i].append(total)
        list_content[i].append(total_dif)
        list_content[i].extend(tmpSubSceList)
# 
    dirname = title
#     mfileName = 'd:/' + dirname
    mfileName = dirname
 
#     print mfileName.decode('gbk')
    if os.path.exists(mfileName) == False:
        os.mkdir(mfileName)
    filename = mfileName + '/' + tname + title[0:9] + '.csv'
    print filename
    csvfile = open(filename, 'wb')
    writer = csv.writer(csvfile)
    for i in range(len(head_str)):
        head_str[i] = head_str[i].encode('gbk')
    writer.writerow(head_str)
    for cont in list_content:
        writer.writerow(cont)
    csvfile.close()

if __name__ == '__main__':
    #215,301,366
    for i in range(30):
        loadlqData(418,team = i+1)
        # print i
    # loadlqData(418,1)
    # print getStat('103058')
    # mlg = NBALeague()
    # mlg.loadData_zf(1)
    # mlg.mergedata()
#     mlg.loadData_rf(1)