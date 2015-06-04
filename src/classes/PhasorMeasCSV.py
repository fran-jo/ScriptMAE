'''
Created on 7 apr 2015

@author: fragom
'''
import csv

class PhasorMeasCSV(object):
    '''
    classdocs
    '''
    ccsvRead= None
    cheader= []
    
    def __init__(self, pcsvFile, pdelimiter=','):
        '''
        Constructor
        Params 0: .csv source dir;
        Params 1: separator , ; or tab
        '''
        self.ccsvRead= csv.reader(open(pcsvFile, 'rb'), delimiter=pdelimiter)
        
    def load_header(self):
        self.cheader= self.ccsvRead.next()
        print 'return', self.cheader 
        return self.cheader
    
    def load_column(self, _variable):
        ''' with the name of a varible, get the values of the corresponding column 
        _variable is 1..n '''
        
        pass