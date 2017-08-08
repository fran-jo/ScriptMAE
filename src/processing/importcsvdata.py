'''
Created on 4 Aug 2017

@author: fran_jo
'''
from inout import InputCSVStream
from inout import StreamCIMH5

class PMUData(object):
    '''
    classdocs
    '''
    __header= []
    __sourcecsv= None
    __dbh5api= None
    __measurement= {}
    
    def __init__(self, csvFile='.csv', delimiter= ','):
        '''
        Constructor
        '''
        self.__sourcecsv= InputCSVStream(csvFile, delimiter)
        self.__h5fileName= csvFile.split('/')[-1].split('.')[0]
        self.__dbh5api= StreamCIMH5('./db/measurements', str(self.__h5fileName))
        
    @property
    def measurements(self):
        return self.__header
    
    def load_Measurements(self):
        self.__sourcecsv.load_csvHeader()   
        self.__header= self.__sourcecsv.get_header()     
        
    def __load_MeasurementValues(self, measname):
        self.__measurement= self.__sourcecsv.load_csvValues(measname)
    
    def store_Measurements(self, listMeas, separator=':'):
        self.__dbh5api.open(self.__h5fileName, 'a')
        for meas in listMeas:
            goodMeasname= str(meas)
            self.__load_MeasurementValues(goodMeasname)
            resource= goodMeasname.split(separator)[0]
            variable= goodMeasname.split(separator)[1]
            if self.__dbh5api.exist_PowerSystemResource(resource):
                self.__dbh5api.update_PowerSystemResource(resource, resource)
            else:
                self.__dbh5api.add_PowerSystemResource(resource)
            if self.__dbh5api.exist_AnalogMeasurement(variable):
                self.__dbh5api.update_AnalogMeasurement(variable)
                self.__dbh5api.update_AnalogValue(variable, 
                                                  self.__sourcecsv.timestamp2sample(self.__measurement['sampletime']), 
                                                  self.__measurement['magnitude'])
            else:
                self.__dbh5api.add_AnalogMeasurement(variable)
                self.__dbh5api.add_AnalogValue(self.__sourcecsv.timestamp2sample(self.__measurement['sampletime']), 
                                           self.__measurement['magnitude'])
        self.__dbh5api.close()
    
    def __store_MeasurementValue(self, meas):
        pass
    
