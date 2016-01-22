'''
Created on 7 apr 2015

@author: fragom
'''
from modelicares import SimRes
from numpy import angle,absolute
import os
import h5py as h5
from data import signal

class StreamH5File(object):
    '''
    _ch5file file object with reference to the .h5 file
    _datasetValues object to keep in memory a group from the .h5 file
    _datasetNames objet to keep in memory the dataset of signals from the .h5 file
    '''
    _ch5file= None
    _group= None
    _ch5file= None
    _datasetNames= None

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
        self.cfileName= params[1]
        print params[0]
        print params[1]
        if (len(params)> 2):
            self.cmatfile= SimRes(params[2])
#         fileName= time.strftime("%H_%M_%S")+ 'SimulationOutputs.h5'
        ''' a '''
        self.dsenyal= {}
        self.compiler= compiler

    def get_cgroup(self):
        return self._group

    def get_cdataSetValues(self):
        return self._datasetValues
    
    def get_cdataSetNames(self):
        return self._datasetNames

    def set_cgroup(self, value):
        self._group = value


    def set_cdataSetValues(self, value):
        self._datasetValues = value
        
    def set_cdataSetNames(self, value):
        self._datasetNames = value

    def del_cgroup(self):
        del self._group
        
    def del_cdataSetNames(self):
        del self._datasetNames
        
    def del_cdataSetValues(self):
        del self._datasetValues

        
    def get_senyal(self, _variable):
        ''' return signal object '''
        return self.dsenyal[_variable]

    def set_senyalRect(self, _variable, _nameR, _nameI):
        ''' set a signal in complex form, real+imaginary '''
        if self.compiler== 'omc': 
            nameVarTime= 'time' 
        else: 
            nameVarTime= "Time"
        csenyal= signal.Signal()
        if (_nameI != []):
            csenyal.set_signalRect(self.cmatfile[nameVarTime], self.cmatfile[_nameR], self.cmatfile[_nameI])
        else:
            ''' array of 0 of the same length as samples '''
            emptyarray= [-1 for x in self.cmatfile[nameVarTime]]
            csenyal.set_signalRect(self.cmatfile[nameVarTime], self.cmatfile[_nameR], emptyarray)
            
        self.dsenyal[_variable]= csenyal
        
    def set_senyalPolar(self, _variable, _nameM, _nameP):
        ''' set a signal in polar form, magnitude + angle '''
        if self.compiler== 'omc': 
            nameVarTime= 'time' 
        else: 
            nameVarTime= "Time"
        csenyal= signal.SignalPMU()
        if (_nameP != []):
            csenyal.set_signalPolar(self.cmatfile[nameVarTime], self.cmatfile[_nameM], self.cmatfile[_nameP])
        else:
            ''' array of 0 of the same length as samples '''
            emptyarray= [-1 for x in self.cmatfile[nameVarTime]]
            csenyal.set_signalPolar(self.cmatfile[nameVarTime], self.cmatfile[_nameM], emptyarray)
        self.dsenyal[_variable]= csenyal
        
    def set_senyal(self, componame, senyal):
        ''' from a signal already loaded from a CSV file '''
        self.dsenyal[componame]= senyal
        
    def del_senyal(self):
        del self.csenyal
    
    
    group = property(get_cgroup, set_cgroup, del_cgroup, "_group's docstring")
    datasetValues = property(get_cdataSetValues, set_cdataSetValues, del_cdataSetValues, "cdataset's docstring")
    datasetNames = property(get_cdataSetNames, set_cdataSetNames, del_cdataSetNames, "cdataset's docstring")
    senyalCmp = property(get_senyal, set_senyalRect, del_senyal, "signalold's docstring")
    senyalPol = property(get_senyal, set_senyalPolar, del_senyal, "signalold's docstring")
    
    
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
    def __init__(self, _source):
        super(InputH5Stream, self).__init__(['',_source],'')

    def open_h5(self):
        ''' Opens and existing .h5 file in reading mode '''
        self._ch5file= h5.File(self.cfileName, 'r')
        
    def open_exth5(self, _sourceH5):
        ''' Opens and existing .h5 file in reading mode '''
        self._ch5file= h5.File(_sourceH5, 'r')
         
    def load_h5(self, _network, _component):
        ''' 
        Loads signal data from a specific variable form a specific component 
        _network name of the entire network model or area inside the model
        _component is the name of the component we are working with
        _variable is the name of the variable that contains signal data, from the specified component 
        '''
        # load data into internal dataset
        self._group= self._ch5file[_network]
        self._datasetValues= self._group[_component+'_values']
        self._datasetNames= self._group[_component+'_items']
        idx= 1
        for item in self._datasetNames:
            print idx, item
#             if (item == _variable):
#             if self._datasetValues.attrs['coord']== 'polar':
#                 print 'polar'
#                 csenyal= signal.SignalPMU()
#                 csenyal.set_signalPolar(self._datasetValues[:,0], self._datasetValues[:,idx], self._datasetValues[:,idx+1])
#             else:
#                 print 'complex'
            csenyal= signal.Signal()
            csenyal.set_signalRect(self._datasetValues[:,0], self._datasetValues[:,idx], self._datasetValues[:,idx+1])
            csenyal.set_ccomponent(_component)
            self.dsenyal[_component]= csenyal
            idx+= 2
    
    def load_h5SignalGroup(self):
        self._group= self._ch5file[self._ch5file.keys()[0]]
        self.datasetList= []
        for name in self._group:
            if (name.find("_values") != -1):
                self.datasetList.append(name)
                
    def load_h5Group(self):
        self._group= self._ch5file[self._ch5file.keys()[0]]
        self.datasetList= []
        for name in self._group:
                self.datasetList.append(name)
    
    def load_h5SignalData(self, _name):
        ''' get signal data from a specific dataset '''
        self.csignal= signal.Signal()
        for x, y, z, in self._group.get(_name):
            self.sampleTime.append(x)
            self.magnitude.append(y)
            self.angle.append(z)
        self.csignal.set_signalRect(self.sampleTime, self.magnitude, self.angle)
    
    def get_h5signal(self):
        ''' array with sampletime, magnitude and angle '''
        return self.sampleTime, self.magnitude, self.angle
    
    def get_h5Data(self, datasetName):
        return self._group[datasetName][:]
    
    def del_h5signal(self):
        self.sampleTime= []
        self.magnitude= []
        self.angle= []
          
    def close_h5(self):
        self._ch5file.close()
        
        

class OutputH5Stream(StreamH5File):
    '''
    Writes data into a hdf5 file. The structure must have 
    1) dataset to store signal names
    2) dataset to store signal values, per pairs, column 1: re/mag; column2: im/pol 
    '''
    def __init__(self, _params, _compiler):
        super(OutputH5Stream, self).__init__(_params, _compiler)
        
    def open_h5(self, _network):
        ''' Opens the h5 file in append mode '''
        self._ch5file= h5.File(self.cfileName, 'a')
        if not _network in self._ch5file:
            self._group= self._ch5file.create_group(_network)
        else:
            self._group= self._ch5file[_network]
            
    def save_h5Values(self, component):
        ''' Creates the .h5, in append mode, with an internal structure for signal values.
        Saves signal data from a specific model. It creates an internal dataset, into the current 
        group of the current .h5, with the name of the component parameter
        component indicates the name of component where the data is collected from '''
        # create datasets
        if not component+'_values' in self._group:
#             self._datasetValues= self._group.create_dataset(_component+'_values', 
#                                                       (self.dsenyal[_component].get_csamples(),len(self.dsenyal)*2+1),
#                                                       chunks=(100,3))
            self._datasetValues= self._group.create_dataset(component+'_values', 
                                                      (self.dsenyal[component].get_csamples(),3),
                                                      chunks=(250,3))
        else:
            self._datasetValues= self._group[component+'_values']
        column= 1
        ''' signals can store two type of data, complex or polar, values are saved per pairs '''
#         for lasenyal in self.dsenyal[_component]:
        lasenyal= self.dsenyal[component]
        self._datasetValues[:,0]= lasenyal.get_sampleTime()
        if isinstance(lasenyal, signal.SignalPMU):  
            self._datasetValues[:,column]= lasenyal.get_signalMag()
            column+= 1
            self._datasetValues[:,column]= lasenyal.get_signalPhase()
        else: 
            self._datasetValues[:,column]= lasenyal.get_signalReal()
            column+= 1
            self._datasetValues[:,column]= lasenyal.get_signalImag()
#             column+= 1
    
    def save_h5Names(self, component, senyales):
        ''' Creates the .h5, in append mode, with an internal structure for signal names.
        Saves signal names from a specific model. It creates an internal dataset into the current
        group of the current .h5. 
        component indicates the name of component where the data is collected from 
        senyales list of signal names from the _component'''
#         print 'len ', len(_variable)+ 1
        dt = h5.special_dtype(vlen=unicode)
        if not component+'_items' in self._group:
            self._datasetNames= self._group.create_dataset(component+'_items', (1,len(senyales)), dtype=dt)
        else:
            self._datasetNames= self._group[component+'_items']
        #print "Dataset dataspace is", self.datasetNames.shape
#         metaSignal= [u"sampletime", u"s", u"int"]
#         self.datasetNames[:,0]= metaSignal
        row= 0
        for name in senyales:   
            self._datasetNames[:,row]= str(name)
            row+= 1
            
    def close_h5(self):
        # close file
        self._ch5file.close()
        