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
    _csvFile file object with reference to the .csv file
    cgroup object to keep in memory a group from the .h5 file
    cdataset objet to keep in memory the dataset of signals from the .h5 file
    '''
    _csvFile= None
    _header= []
    _senyales= {}

    def __init__(self, sourceFile, delimiter=','):
        '''
        Constructor
        _sourceFile: .csv file path
        _delimiter: delimiter of fields
        '''
        # TODO solve the issue of signal length
        self._csvFile= panda.read_csv(sourceFile, sep=delimiter, nrows=1000)

    def get_csv_file(self):
        return self._csvFile

    def get_header(self):
        return self._header

    def set_csv_file(self, value):
        self._csvFile = value

    def set_header(self, value):
        self._header = value

    def del_csv_file(self):
        del self._csvFile

    def del_header(self):
        del self._header
        
    def get_senyal(self, componame):
        ''' return signal object '''
        return self._senyales[componame]
       
        
    def timestamp2sample(self, variable):
        tiempos= [datetime.strptime(x,"%Y/%m/%d %H:%M:%S.%f") for x in self._senyales[variable].get_sampleTime()]
        sampletime= [(t- tiempos[0]).microseconds/1000 for t in tiempos]
#         print sampletime
        return sampletime 
    
    csvFile = property(get_csv_file, set_csv_file, del_csv_file, "csvFile's docstring")
    header = property(get_header, set_header, del_header, "header's docstring")
            
            
class InputCSVStream(StreamCSVFile):
    '''
    Class observer for PMU data, in .csv file format
    Header format: 
    '''
    def __init__(self, sourceFile, delimiter=','):
        super(InputCSVStream, self).__init__(sourceFile, delimiter)

    def get_senyales(self):
        return self._senyales

    def set_senyales(self, value):
        self._senyales = value

    def del_senyales(self):
        del self._senyales


    def open_csv(self):
        ''' Opens and existing csv file in reading mode '''
        pass
        
    def load_csvHeader(self):
        self._header= list(self._csvFile.columns.values)
    
    def load_csvHeaderIdx(self, variable):
        return self._header.index(variable)
    
    def load_csvValues(self, componame, senyalR, senyalI):
        ''' Loads signal data from a specific variable form a specific component
        senyal: variable name of the signal, column name
        senyalR: name of the real,magnitude signal
        senyalI: name of the imaginary,phase signal 
        '''
        senyal= signal.Signal()
        if (senyalI != []):
            senyal.set_signal(list(self._csvFile['Timestamp']), 
                                    list(self._csvFile[senyalR]), list(self._csvFile[senyalI]))
        else:
            ''' array of 0 of the same length as samples '''
            emptyarray= [-1 for x in self._csvFile['Timestamp']]
            senyal.set_signal(list(self._csvFile['Timestamp']), 
                                    list(self._csvFile[senyalR]), emptyarray)
        senyal.set_component(componame)    
        self._senyales[componame]= senyal
    
    def timestamp2sample(self, componame):
        '''converts the timestamp value from pmu measurement into sample value as sample time 
        _variable name of the measurement to get the signal from 
        '''
        tiempos= [datetime.strptime(x,"%Y/%m/%d %H:%M:%S.%f") 
                  for x in self._senyales[componame].sampletime]
        sampletime= [(t- tiempos[0]).microseconds/1000 for t in tiempos]
        senyal= signal.Signal()
        senyal.set_signal(sampletime, self._senyales[componame].magnitude, 
                                self._senyales[componame].phase)
        senyal.set_component(componame)
        self._senyales[componame]= None
        self._senyales[componame]= senyal
    
    def close_csv(self):
        self._csvFile.close()
        
        
    senyales = property(get_senyales, set_senyales, del_senyales, "senyales's docstring")
        
