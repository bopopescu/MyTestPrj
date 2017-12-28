# *-* coding:GBK *-*

'''
Created on 2015-12-3

@author: kingbiwu
'''

from bs4 import BeautifulSoup
import urllib2 

urldomain = "http://liansai.500.com/"
leagueId = '3749'
mDict = {}
def getTeamid(leagueid):
    url_ = urldomain + "zuqiu-" + leagueid + "/"
    
    rsp = urllib2.urlopen(url_)
    mSoup = BeautifulSoup(rsp)
    trs = mSoup.body.find(attrs={'class':'lbox_bd'}).find_all('tr')

    
    for tr in trs:
        if len(tr.find_all('td')) > 0:
            mA = tr.find_all('td')[1].find('a')
#             print mA.get('href').split('/')[2] + " " + mA.string.encode('raw-unicode-escape')
            mDict.setdefault(mA.get('href').split('/')[2], mA.string.encode('raw-unicode-escape'))
            


if __name__ == '__main__':
    getTeamid(leagueId)