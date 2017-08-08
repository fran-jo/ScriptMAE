'''
Created on 7 apr 2015

@author: fragom
'''
import h5py as h5
import collections

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
        if '.' in network:
            self.__h5namefile= dbpath+ '/'+ network
        else:
            self.__h5namefile= dbpath+ '/'+ network+ '.h5'
        
    def open(self, networkname= '', mode= 'r'):
        ''' h5name is name of the model '''
        if '.' in networkname:
            networkname= networkname.split('.')[0]
        self.__h5file= h5.File(self.__h5namefile, mode)
        if not networkname in self.__h5file:
            self.__gmodel= self.__h5file.create_group(networkname)
        else:
            self.__gmodel= self.__h5file[networkname]

    def close(self):
        self.__h5file.close()
    
    def select_AllGroup(self, networkname):
        ''' build a dictionary with the name of the groups '''
        arbol = {}
        senyals= []
        for psres in self.__gmodel.keys():
            self.__gPowerSystemResource= self.__gmodel[psres]
            for meas in self.__gPowerSystemResource.keys():
                senyals.append(meas)
            arbol[psres]= senyals
            senyals= []
#         self.__select_iGroups(self.__gmodel, raiz_element, arbol)
        arbol= collections.OrderedDict(sorted(arbol.items()))
        return arbol

    def select_Model(self):
        return self.__gmodel.name
    
    def exist_PowerSystemResource(self, resource):
        if not resource in self.__gmodel:
            return False
        else:
            return True
            
    def select_PowerSystemResource(self, resource):
        self.__gPowerSystemResource= self.__gmodel[resource]
        return self.__gPowerSystemResource.name
    
    def exist_AnalogMeasurement(self, variable):
        if not variable in self.__gPowerSystemResource:
            return False
        else:
            return True
    
    def select_AnalogMeasurement(self, variable):
        ''' TODO use PyCIM classes for Analog and AnalogValue '''
        senyal= {}
        self.__ganalogMeasurement= self.__gPowerSystemResource[variable]
#         senyal['unitSymbol']= self.__ganalogMeasurement['unitSymbol']
#         senyal['unitMultiplier']= self.__ganalogMeasurement['unitMultiplier']
#         senyal['measurementType']= self.__ganalogMeasurement['measurementType']
        senyal['sampleTime']= self.__ganalogMeasurement['AnalogValue'][:,0]
        senyal['magnitude']= self.__ganalogMeasurement['AnalogValue'][:,1]
        return senyal
    
    def add_PowerSystemResource(self, resource):
        ''' resource is the name of the component '''
        self.__gPowerSystemResource= self.__gmodel.create_group(resource)
    
    
    def add_AnalogMeasurement(self, variable, unisymb= 'unit', 
                              unitmultipl= 'multiplier', measType= 'Analog Measurement'):
        ''' resource is the name of the variable 
        add a new group and add attributes '''
        self.__ganalogMeasurement= self.__gPowerSystemResource.create_group(variable)
        self.__ganalogMeasurement.attrs['unitSymbol']= unisymb
        self.__ganalogMeasurement.attrs['unitMultiplier']= unitmultipl
        self.__ganalogMeasurement.attrs['measurementType']= measType
        
    def add_AnalogValue (self, sampleTime, measValues):
        self.__danalogValue= self.__ganalogMeasurement.create_dataset('AnalogValue', 
                                    (len(sampleTime),2), chunks=(100,2))
        self.__danalogValue[:,0]= sampleTime
        self.__danalogValue[:,1]= measValues
        
    
    def update_PowerSystemResource(self, resource, resourceNew):
        self.__gPowerSystemResource= self.__gmodel[resource]
        
    def update_AnalogMeasurement(self, variable, unisymb= 'unitSymbol', 
                              unitmultipl= 'unitMultiplier', measType= 'measurementType'):
        self.__ganalogMeasurement= self.__gPowerSystemResource[variable]
        self.__ganalogMeasurement.attrs['unitSymbol']= unisymb
        self.__ganalogMeasurement.attrs['unitMultiplier']= unitmultipl
        self.__ganalogMeasurement.attrs['measurementType']= measType
        
    def update_AnalogValue(self, variable, sampleTime, measValues):
        self.__danalogValue= self.__ganalogMeasurement['AnalogValue']
        self.__danalogValue[:,0]= sampleTime
        self.__danalogValue[:,1]= measValues
