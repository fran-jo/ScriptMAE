'''
Created on 24 Aug 2017

@author: fran_jo
'''

import h5py as h5

'''TODO: use of PyCIM classes and method write ''' 
class StreamH5CIM(object):
    '''
    classdocs
    '''
    '''TODO: check namespaces to write CIM file '''

    def __init__(self, params):
        '''
        Constructor
        '''
    
    def open(self, networkname= '', mode= 'r'):
        ''' h5name is name of the model '''
        if '.' in networkname:
            networkname= networkname.split('.')[0]
        self.__h5file= h5.File(self.__h5namefile, mode)
        if networkname in self.__h5file:
            self.__gmodel= self.__h5file[networkname]

    def close(self):
        self.__h5file.close()
        
    def exist_PowerSystemResource(self, resource):
        if not resource in self.__gmodel:
            return False
        else:
            return True
            
    def select_PowerSystemResource(self, resource):
        ''' TODO: PyCIM classes for PowerSystemsResource '''
        gPowerSystemResource= self.__gmodel[resource]
        return gPowerSystemResource.name
    
    def exist_AnalogMeasurement(self, variable):
        if not variable in self.__gPowerSystemResource:
            return False
        else:
            return True
    
    def select_AnalogMeasurement(self, variable):
        '''TODO: use PyCIM classes for Analog and AnalogValue '''
        senyal= {}
        self.__ganalogMeasurement= self.__gPowerSystemResource[variable]
#         senyal['unitSymbol']= self.__ganalogMeasurement['unitSymbol']
#         senyal['unitMultiplier']= self.__ganalogMeasurement['unitMultiplier']
#         senyal['measurementType']= self.__ganalogMeasurement['measurementType']
        senyal['sampleTime']= self.__ganalogMeasurement['AnalogValues'][:,0]
        senyal['magnitude']= self.__ganalogMeasurement['AnalogValues'][:,1]
        return senyal