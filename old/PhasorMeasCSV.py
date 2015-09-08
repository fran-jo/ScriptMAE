'''
Created on 7 apr 2015

@author: fragom
'''
import csv
from datetime import datetime

class PhasorMeasCSV(object):
    '''
    classdocs
    '''
    ccsvRead= None
    cheader= []
    csignal= {}
    
    def __init__(self, pcsvFile, pdelimiter=','):
        '''
        Constructor
        Params 0: .csv source dir/file;
        Params 1: separator , ; or tab
        '''
        self.ccsvRead= csv.reader(open(pcsvFile, 'rb'), delimiter=pdelimiter)
        
    def load_header(self):
        self.cheader= self.ccsvRead.next()
        print 'return', self.cheader 
        return self.cheader
    
    def load_column(self, _variable):
        ''' with the name of a variable, get the values of the corresponding column 
        _variable is 1..n '''
        print _variable in self.cheader
        column= self.cheader.index(_variable)
        print column
        senyal= []
        for row in self.ccsvRead:
            senyal.append(row[column])
        self.csignal[_variable]= senyal
        
    def get_signal(self, _variable):
        ''' process the data to retrieve float-value array '''
        senyal= [float(x) for x in self.csignal[_variable]]
        return senyal
    
    def get_sampletime(self, _variable):
        ''' process data to generate a vector with long values '''
        tiempos= [datetime.strptime(x,"%Y/%m/%d %H:%M:%S.%f") for x in self.csignal[_variable]]
        sampletime= [(t- tiempos[0]).microseconds/1000 for t in tiempos]
        return sampletime