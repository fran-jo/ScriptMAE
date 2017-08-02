'''
Created on 7 apr 2015

@author: fragom
'''
import h5py as h5

class StreamCIMH5(object):
    '''
    _h5file file object with reference to the .h5 file
    _group object to keep in memory a group from the .h5 file
    cdataset objet to keep in memory the dataset of signals from the .h5 file
    '''
    __h5namefile= ''
    __h5file= None
    __dbfolder= ''
    __gmodel= None
    __gPowerSystemResource= None
    __ganalogMeasurement= None
    __danalogValue= None
    
    def __init__(self, dbpath= '', network= ''):
        '''
        Constructor
        dbpath= folder where to locate h5 files
        resFile= instances of a SimRes object with result file
        '''
        self.__dbfolder= dbpath
        self.__h5namefile= dbpath+ '/'+ network+ '.h5'
        
    def open(self, networkname= ''):
        ''' h5name is name of the model '''
        self.__h5file= h5.File(self.__h5namefile, 'a')
        if not networkname in self.__h5file:
            self.__gmodel= self.__h5file.create_group(networkname)
        else:
            self.__gmodel= self.__h5file[networkname]

    def close(self):
        pass
    
    def exist_PowerSystemResource(self, resource):
        if not resource in self.__gmodel:
            return True
        else:
            return False
            
    def select_PowerSystemResource(self):
        return self.__gPowerSystemResource
    
    def add_PowerSystemResource(self, resource):
        ''' resource is the name of the component '''
        self.__gPowerSystemResource= self.__gmodel.create_group(resource)
    
    def exist_AnalogMeasurement(self, variable):
        if not variable in self.__gPowerSystemResource:
            return True
        else:
            return False
    
    def select_AnalogMeasurement(self):
        return self.__ganalogMeasurement.name
    
    def add_AnalogMeasurement(self, variable, unisymb= 'unitSymbol', 
                              unitmultipl= 'unitMultiplier', measType= 'measurementType'):
        ''' resource is the name of the variable 
        add a new group and add attributes '''
        self.__ganalogMeasurement= self.__gmodel.create_group(variable)
        ''' TODO: Add attributes to the group '''
        self.__ganalogMeasurement['unitSymbol']= unisymb
        self.__ganalogMeasurement['unitMultiplier']= unitmultipl
        self.__ganalogMeasurement['measurementType']= measType
        
    def add_AnalogValue (self, sampleTime, measValues):
        self.__danalogValue= self.__ganalogMeasurement.create_dataset(
                'AnalogValues', (sampleTime,3), chunks=(100,3))
        ''' TODO: add values to the dataset '''
        self.__danalogValue[:,0]= sampleTime
        self.__danalogValue[:,1]= measValues
        
    
    def update_PowerSystemResource(self, resource, resourceNew):
        self.__gPowerSystemResource= self.__gmodel[resource]
        
    def update_AnalogMeasurement(self, variable, unisymb= 'unitSymbol', 
                              unitmultipl= 'unitMultiplier', measType= 'measurementType'):
        self.__ganalogMeasurement= self.__gPowerSystemResource[variable]
        ''' TODO: Add attributes to the group '''
        self.__ganalogMeasurement['unitSymbol']= unisymb
        self.__ganalogMeasurement['unitMultiplier']= unitmultipl
        self.__ganalogMeasurement['measurementType']= measType
        
    def update_AnalogValue(self, variable, sampleTime, measValues):
        self.__danalogValue= self.__ganalogMeasurement['AnalogValue']
        ''' TODO: add values to the dataset '''
        self.__danalogValue[:,0]= sampleTime
        self.__danalogValue[:,1]= measValues
