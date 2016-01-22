'''
Created on 7 apr 2015

@author: fragom
'''
from datetime import datetime
import pandas as panda
from data import signal

class StreamCSVFile(object):
    '''
    Class observer for PMU data, in .csv file format from PMU 
    TODO: handle saving/loading data from the simulation engine 
    ccsvFile file object with reference to the .csv file
    cgroup object to keep in memory a group from the .h5 file
    cdataset objet to keep in memory the dataset of signals from the .h5 file
    '''
    ccsvFile= None
    cheader= []
    dsenyal= {}

    def __init__(self, _sourceFile, _delimiter=','):
        '''
        Constructor
        _sourceFile: .csv file path
        _delimiter: delimiter of fields
        '''
        self.ccsvFile= panda.read_csv(_sourceFile, sep=_delimiter)
        
    def get_fileName(self):
        return self.ccsvFile
    
    def get_senyal(self, componame):
        ''' return signal object '''
        return self.dsenyal[componame]
        
    def del_senyal(self):
        del self.csenyal
        
    def timestamp2sample(self, _variable):
        tiempos= [datetime.strptime(x,"%Y/%m/%d %H:%M:%S.%f") for x in self.dsenyal[_variable].get_sampleTime()]
        sampletime= [(t- tiempos[0]).microseconds/1000 for t in tiempos]
#         print sampletime
        return sampletime

    def pmu_from_cmp(self, a_instance):
        '''Given an instance of A, return a new instance of B.'''
        return signal.SignalPMU(a_instance.field)  
            
            
class InputCSVStream(StreamCSVFile):
    '''
    Class observer for PMU data, in .csv file format
    Header format: 
    '''
    def __init__(self, _sourceFile, _delimiter=','):
        super(InputCSVStream, self).__init__(_sourceFile, _delimiter)

    def open_csv(self):
        ''' Opens and existing csv file in reading mode '''
        pass
         
    def load_csvValues(self, componame, senyalR, senyalI):
        ''' Loads signal data from a specific variable form a specific component
        senyal: variable name of the signal, column name
        senyalR: name of the real,magnitude signal
        senyalI: name of the imaginary,phase signal 
        '''
        csenyal= signal.SignalPMU()
        if (senyalI != []):
            csenyal.set_signalPolar(list(self.ccsvFile['Time']), 
                                    list(self.ccsvFile[senyalR]), list(self.ccsvFile[senyalI]))
        else:
            ''' array of 0 of the same length as samples '''
            emptyarray= [-1 for x in self.ccsvFile['Time']]
            csenyal.set_signalPolar(list(self.ccsvFile['Time']), 
                                    list(self.ccsvFile[senyalR]), emptyarray)
        csenyal.set_ccomponent(componame)    
        self.dsenyal[componame]= csenyal
    
    def timestamp2sample(self, componame):
        '''converts the timestamp value from pmu measurement into sample value as sample time 
        _variable name of the measurement to get the signal from 
        '''
        tiempos= [datetime.strptime(x,"%Y/%m/%d %H:%M:%S.%f") 
                  for x in self.dsenyal[componame].get_sampleTime()]
        sampletime= [(t- tiempos[0]).microseconds/1000 for t in tiempos]
        self.dsenyal[componame].set_sampleTime(sampletime)
        csenyal= signal.SignalPMU()
        csenyal.set_signalPolar(sampletime, self.dsenyal[componame].get_signalMag(), 
                                self.dsenyal[componame].get_signalPolar())
        self.dsenyal[componame]= csenyal
    
    def load_csvHeader(self):
        self.cheader= list(self.ccsvFile.columns.values)
    
    def load_csvHeaderIdx(self, _variable):
        return self.cheader.index(_variable)
    
    def close_csv(self):
        self.ccsvfile.close()
        
