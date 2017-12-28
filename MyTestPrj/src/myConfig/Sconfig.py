# *-* coding:UTF-8 *-*
'''
Created on 2016年6月27日

@author: Administrator
'''
import os
import sys

class Sconfig(object):
    '''
    classdocs
    '''
    srcPath = ''

    def __init__(self):
        '''
        Constructor
        '''
        self.srcPath = os.getcwd()
        self.set_srcpath()
    
    @staticmethod
    def set_srcpath():
        return sys.path[0]
        
if __name__ == '__main__':
    print os.path.join(os.path.dirname(__file__), os.pardir)