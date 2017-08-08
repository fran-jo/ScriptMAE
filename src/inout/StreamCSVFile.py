'''
Created on 7 apr 2015

@author: fragom
'''
from datetime import datetime
import pandas as panda

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
    
    def load_csvHeader(self):
        self._header= list(self._csvFile.columns.values)
    
    def load_csvHeaderIdx(self, variable):
        return self._header.index(variable)
    
    def load_csvValues(self, nameSenyal):
        ''' Loads signal data from a specific variable form a specific component
        senyal: variable name of the signal, column name
        '''
        senyal= {}
        senyal['sampletime']= self._csvFile['Timestamp'].values
        senyal['magnitude']= self._csvFile[nameSenyal].values
        return senyal
    
    def timestamp2sample(self, timeSenyal):
        '''converts the timestamp value from pmu measurement into sample value as sample time 
        senyal is the corresponding Timestamp array from the pmu measurements
        '''
        tiempos= [datetime.strptime(x,"%Y/%m/%d %H:%M:%S.%f") 
                  for x in timeSenyal]
        sampletime= [(t- tiempos[0]).total_seconds()*1000 for t in tiempos]
        return sampletime
    
    def close_csv(self):
        self._csvFile.close()
        
