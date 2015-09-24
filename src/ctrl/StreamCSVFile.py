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
        
    def get_senyal(self, _variable):
        ''' return signal object '''
        return self.dsenyal[_variable]

    def set_senyalRect(self, _variable, _nameR, _nameI):
        ''' set a signal in complex form, real+imaginary '''
        pass
        
    def set_senyalPolar(self, _variable, _nameM, _nameP):
        ''' set a signal in polar form, magnitude + angle '''
        csenyal= signal.SignalPMU()
        if (_nameP != []):
            csenyal.set_signalPolar(self.ccsvFile['Timestamp'], 
                                    list(self.ccsvFile[_nameM]), list(self.ccsvFile[_nameP]))
        else:
            ''' array of 0 of the same length as samples '''
            emptyarray= [-1 for x in self.ccsvFile['Timestamp']]
            csenyal.set_signalPolar(self.ccsvFile['Timestamp'], 
                                    list(self.ccsvFile[_nameM]), emptyarray)
        csenyal.set_ccomponent(_variable)    
        self.dsenyal[_variable]= csenyal
        
    def del_senyal(self):
        del self.csenyal
    
    senyalCmp = property(get_senyal, set_senyalRect, del_senyal, "signalold's docstring")
    senyalPol = property(get_senyal, set_senyalPolar, del_senyal, "signalold's docstring")
    
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
         
    def load_csvValues(self, _variable, _nameM, _nameP):
        ''' Loads signal data from a specific variable form a specific component
        _variable: variable name of the signal, column name
        _nameM: name of the magnitude signal
        _nameP: name of the phase signal 
        '''
        csenyal= signal.SignalPMU()
        if (_nameP != []):
            csenyal.set_signalPolar(self.ccsvFile['Time'], 
                                    list(self.ccsvFile[_nameM]), list(self.ccsvFile[_nameP]))
        else:
            ''' array of 0 of the same length as samples '''
            emptyarray= [-1 for x in self.ccsvFile['Time']]
            csenyal.set_signalPolar(self.ccsvFile['Time'], 
                                    list(self.ccsvFile[_nameM]), emptyarray)
        csenyal.set_ccomponent(_variable)    
        self.dsenyal[_variable]= csenyal
    
    def timestamp2sample(self, _variable):
        '''converts the timestamp value from pmu measurement into sample value as sample time 
        _variable name of the measurement to get the signal from 
        '''
        tiempos= [datetime.strptime(x,"%Y/%m/%d %H:%M:%S.%f") 
                  for x in self.dsenyal[_variable].get_sampleTime()]
        sampletime= [(t- tiempos[0]).microseconds/1000 for t in tiempos]
        self.dsenyal[_variable].set_sampleTime(sampletime)
        csenyal= signal.SignalPMU()
        csenyal.set_signalPolar(sampletime, self.dsenyal[_variable].get_signalMag(), 
                                self.dsenyal[_variable].get_signalPolar())
        self.dsenyal[_variable]= csenyal
    
    def load_csvHeader(self):
        self.cheader= list(self.ccsvFile.columns.values)
        return self.cheader
    
    def load_csvHeaderIdx(self, _variable):
        return self.cheader.index(_variable)
    
    def close_csv(self):
        self.ccsvfile.close()
        
