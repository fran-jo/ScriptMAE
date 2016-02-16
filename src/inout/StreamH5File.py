'''
Created on 7 apr 2015

@author: fragom
'''
import os
from modelicares import SimRes
from numpy import angle, absolute
from data import signal
import h5py as h5


class StreamH5File(object):
    '''
    _h5file file object with reference to the .h5 file
    _group object to keep in memory a group from the .h5 file
    cdataset objet to keep in memory the dataset of signals from the .h5 file
    '''
    _fileName= ''
    _h5file= None
    _group= None
    _dsetnames= None
    _dsetvalues= None
    _signals= {}
    
    def __init__(self, params, compiler='omc'):
        '''
        Constructor
        _compiler: omc, dymola or jm
        Params 0: output dir; 
        Params 1: .h5 file path;
        Params 2: .mat file path;
        '''
        if (params[0]!= ''):
            os.chdir(params[0])
        self._fileName= params[1]
        if (len(params)> 2):
            self._matfile= SimRes(params[2])
#         fileName= time.strftime("%H_%M_%S")+ 'SimulationOutputs.h5'
        ''' a '''
        self.compiler= compiler

    def get_signals(self):
        return self._signals

    def set_signals(self, value):
        self._signals = value

    def del_signals(self):
        del self._signals

    def get_group(self):
        return self._group

    def get_dsetvalues(self):
        return self._dsetvalues

    def get_dsetnames(self):
        return self._dsetnames

    def set_group(self, value):
        self._group = value

    def set_dsetvalues(self, value):
        self._dsetvalues = value

    def set_dsetnames(self, value):
        self._dsetnames = value

    def del_group(self):
        del self._group

    def del_dsetvalues(self):
        del self._dsetvalues

    def del_dsetnames(self):
        del self._dsetnames
    
    group = property(get_group, set_group, del_group, "group's docstring")
    dsetvalues = property(get_dsetvalues, set_dsetvalues, del_dsetvalues, "dsetvalues's docstring")
    dsetnames = property(get_dsetnames, set_dsetnames, del_dsetnames, "dsetnames's docstring")
    signals = property(get_signals, set_signals, del_signals, "signals's docstring")
    
    def get_senyal(self, measurement):
        ''' return signal object '''
        return self._signals[measurement]

    def set_senyalRect(self, _measurement, _nameR, _nameI):
        ''' set a signal in complex form, real+imaginary '''
        if self.compiler== 'omc': 
            nameVarTime= 'time' 
        else: 
            nameVarTime= "Time"
        senyal= signal.Signal()
        if (_nameI != []):
            senyal.set_signalRect(self._matfile[nameVarTime], self._matfile[_nameR], self._matfile[_nameI])
            print self._matfile[nameVarTime]
            print self._matfile[_nameR]
            print self._matfile[_nameI]
        else:
            ''' array of 0 of the same length as samples '''
            emptyarray= [0 for x in self._matfile[nameVarTime]]
            senyal.set_signalRect(self._matfile[nameVarTime], self._matfile[_nameR], emptyarray)
            
        self._signals[_measurement]= senyal
        
    def set_senyalPolar(self, _measurement, _nameM, _nameP):
        ''' set a signal in polar form, magnitude + angle '''
        if self.compiler== 'omc': 
            nameVarTime= 'time' 
        else: 
            nameVarTime= "Time"
        senyal= signal.SignalPMU()
        if (_nameP != []):
            senyal.set_signalPolar(self._matfile[nameVarTime], self._matfile[_nameM], self._matfile[_nameP])
        else:
            ''' array of 0 of the same length as samples '''
            emptyarray= [0 for x in self._matfile[nameVarTime]]
            senyal.set_signalPolar(self._matfile[nameVarTime], self._matfile[_nameM], emptyarray)
        self._signals[_measurement]= senyal
        
    
    def pmu_from_cmp(self, a_instance):
        '''Given an instance of A, return a new instance of B.'''
        return signal.SignalPMU(a_instance.field)
    
    def calc_phasorSignal(self):
        ''' function that converts the internal complex signal into polar form '''
        magnitud= []
        fase= []
        for re,im in zip(self.csenyal.get_signalReal(), self.csenyal.get_signalReal()):
            magnitud.append(absolute(re+im))
            fase.append(angle(re+im,deg=True))
        self.csenyal.set_signalPolar(self.get_senyal().get_sampleTime(), magnitud, fase)
    
    
                   
class InputH5Stream(StreamH5File):
    '''
    classdocs
    '''
    __datasetList= []
    

    def __init__(self, sourceH5):
        super(InputH5Stream, self).__init__(['',sourceH5])

    def get_dataset_list(self):
        return self.__datasetList

    def set_dataset_list(self, value):
        self.__datasetList = value

    def del_dataset_list(self):
        del self.__datasetList


    def open_h5(self):
        ''' Opens and existing .h5 file in reading mode '''
        self._h5file= h5.File(self._fileName, 'r')
         
    def load_h5Group(self):
        self._group= self._h5file[self._h5file.keys()[0]]
        self.__datasetList= []
        for name in self._group:
            if (name.find("_values") != -1):
                self.__datasetList.append(name)
                
    def load_h5(self, network, component):
        ''' 
        Loads signal data from a specific variable form a specific component 
        network name of the entire network model or area inside the model
        component is the name of the component we are working with 
        '''
        # load data into internal dataset
        self._group= self._h5file[network]
        self._dsetValues= self._group[component+'_values']
        self._dsetnames= self._group[component+'_items']
        idx= 1
        for item in self._dsetnames:
#             print idx, item
            senyal= signal.Signal()
            senyal.set_signal(self._dsetValues[:,0], self._dsetValues[:,idx], self._dsetValues[:,idx+1])
            senyal.set_component(component)
            self._signals[component]= senyal
            idx+= 2
            
    def close_h5(self):
        self._h5file.close()
        
        
    datasetList = property(get_dataset_list, set_dataset_list, del_dataset_list, "datasetList's docstring")

        
        
class OutputH5Stream(StreamH5File):
    '''
    Writes data into a hdf5 file. The structure must have 
    1) dataset to store signal names
    2) dataset to store signal values, per pairs, column 1: re/mag; column2: im/pol 
    '''
    
    __senyales= {}
    
    def __init__(self, params, compiler):
        super(OutputH5Stream, self).__init__(params, compiler)

    def get_senyales(self):
        return self.__senyales

    def set_senyales(self, value):
        self.__senyales = value

    def del_senyales(self):
        del self.__senyales

        
    def open_h5(self, network):
        ''' Opens the h5 file in append mode 
        _network is the name of the model simulated. Is used to create the main group of this .h5'''
        self._h5file= h5.File(self._fileName, 'a')
        if not network in self._h5file:
            self._group= self._h5file.create_group(network)
        else:
            self._group= self._h5file[network]
            
    def save_h5Values(self, component, signalvalues):
        ''' Creates the .h5, in append mode, with an internal structure for signal values.
        Saves signal data from a specific model. It creates an internal dataset, into the current 
        group of the current .h5, with the name of the component parameter
        component indicates the name of component where the data is collected from 
        signalvalues
        '''
        # create datasets
        if not component+'_values' in self._group:
#             self._dsetvalues= self._group.create_dataset(component+'_values', 
#                                                       (self._signals[component].get_csamples(),len(self._signals)*2+1),
#                                                       chunks=(100,3))
            self.__dsetvalues= self._group.create_dataset(component+'_values', 
                                                      (signalvalues.get_samples(),3),
                                                      chunks=(100,3))
        else:
            self.__dsetvalues= self._group[component+'_values']
        column= 1
        ''' signals can store two type of data, complex or polar, values are saved per pairs '''
        lasenyal= signalvalues
        self.__dsetvalues[:,0]= lasenyal.get_sampleTime()
        if isinstance(lasenyal, signal.SignalPMU):  
            self.__dsetvalues[:,column]= lasenyal.get_signalMag()
            column+= 1
            self.__dsetvalues[:,column]= lasenyal.get_signalPhase()
        else: 
            self.__dsetvalues[:,column]= lasenyal.get_signalReal()
            column+= 1
            self.__dsetvalues[:,column]= lasenyal.get_signalImag()
    
    def save_h5Names(self, component, signalnames):
        ''' Creates the .h5, in append mode, with an internal structure for signal names.
        Saves signal names from a specific model. It creates an internal dataset into the current
        group of the current .h5. 
        component indicates the name of component where the data is collected from 
        signalnames list of signal names from the component
        '''
        dt = h5.special_dtype(vlen=unicode)
        if not component+'_items' in self._group:
            self.__dsetnames= self._group.create_dataset(component+'_items', (1,len(signalnames)+1), dtype=dt)
        else:
            self.__dsetnames= self._group[component+'_items']
#         metaSignal= [u"sampletime", u"s", u"int"]
        self.__dsetnames[:,0]= u"sampletime"
        row= 1
        for senya in signalnames:
            self.__dsetnames[:,row]= str(senya)
            row+= 1
            
    def close_h5(self):
        self._h5file.close()
        
    senyales = property(get_senyales, set_senyales, del_senyales, "senyales's docstring")
