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
    ch5file file object with reference to the .h5 file
    cgroup object to keep in memory a group from the .h5 file
    cdataset objet to keep in memory the dataset of signals from the .h5 file
    '''
    ch5file= None
    cgroup= None
    cdatasetValues= None
    cdatasetNames= None

    def __init__(self, _params, _compiler='omc'):
        '''
        Constructor
        _compiler: omc, dymola or jm
        Params 0: output dir; 
        Params 1: .h5 file path;
        Params 2: .mat file path;
        '''
        if (_params[0]!= ''):
            os.chdir(_params[0])
        self.cfileName= _params[1]
        if (len(_params)> 2):
            self.cmatfile= SimRes(_params[2])
#         fileName= time.strftime("%H_%M_%S")+ 'SimulationOutputs.h5'
        ''' a '''
        self.dsenyal= {}
        self.compiler= _compiler

    def get_cgroup(self):
        return self.cgroup

    def get_cdataSetValues(self):
        return self.cdatasetValues
    
    def get_cdataSetNames(self):
        return self.cdatasetNames

    def set_cgroup(self, value):
        self.cgroup = value


    def set_cdataSetValues(self, value):
        self.cdatasetValues = value
        
    def set_cdataSetNames(self, value):
        self.cdatasetNames = value

    def del_cgroup(self):
        del self.cgroup
        
    def del_cdataSetNames(self):
        del self.cdatasetNames
        
    def del_cdataSetValues(self):
        del self.cdatasetValues

        
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
        
    def del_senyal(self):
        del self.csenyal
    
    
    group = property(get_cgroup, set_cgroup, del_cgroup, "cgroup's docstring")
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
        self.ch5file= h5.File(self.cfileName, 'r')
        
    def open_exth5(self, _sourceH5):
        ''' Opens and existing .h5 file in reading mode '''
        self.ch5file= h5.File(_sourceH5, 'r')
         
    def load_h5(self, _network, _component):
        ''' 
        Loads signal data from a specific variable form a specific component 
        _network name of the entire network model or area inside the model
        _component is the name of the component we are working with
        _variable is the name of the variable that contains signal data, from the specified component 
        '''
        # load data into internal dataset
        self.cgroup= self.ch5file[_network]
        self.cdatasetValues= self.cgroup[_component+'_values']
        self.cdatasetNames= self.cgroup[_component+'_items']
        idx= 1
        for item in self.cdatasetNames:
            print idx, item
#             if (item == _variable):
#             if self.cdatasetValues.attrs['coord']== 'polar':
#                 print 'polar'
#                 csenyal= signal.SignalPMU()
#                 csenyal.set_signalPolar(self.cdatasetValues[:,0], self.cdatasetValues[:,idx], self.cdatasetValues[:,idx+1])
#             else:
#                 print 'complex'
            csenyal= signal.Signal()
            csenyal.set_signalRect(self.cdatasetValues[:,0], self.cdatasetValues[:,idx], self.cdatasetValues[:,idx+1])
            csenyal.set_ccomponent(_component)
            self.dsenyal[_component]= csenyal
            idx+= 2
            
    def close_h5(self):
        self.ch5file.close()
        

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
        self.ch5file= h5.File(self.cfileName, 'a')
        if not _network in self.ch5file:
            self.cgroup= self.ch5file.create_group(_network)
        else:
            self.cgroup= self.ch5file[_network]
            
    def save_h5Values(self, _component, _variable):
        ''' Creates the .h5, in append mode, with an internal structure for signal values.
        Saves signal data from a specific model. It creates an internal dataset, into the current 
        group of the current .h5, with the name of the _component parameter
        _component indicates the name of component where the data is collected from 
        _variable is the name of the signal to be saved '''
        # create datasets
        if not _component+'_values' in self.cgroup:
            ''' TODO: dataset size according to signals of the component '''
#             self.cdatasetValues= self.cgroup.create_dataset(_component+'_values', 
#                                                       (self.dsenyal[_component].get_csamples(),len(self.dsenyal)*2+1),
#                                                       chunks=(100,3))
            self.cdatasetValues= self.cgroup.create_dataset(_component+'_values', 
                                                      (self.dsenyal[_component].get_csamples(),3),
                                                      chunks=(100,3))
        else:
            self.cdatasetValues= self.cgroup[_component+'_values']
        column= 1
        ''' signals can store two type of data, complex or polar, values are saved per pairs '''
#         for lasenyal in self.dsenyal[_component]:
        lasenyal= self.dsenyal[_component]
        self.cdatasetValues[:,0]= lasenyal.get_sampleTime()
        if isinstance(lasenyal, signal.SignalPMU):  
            self.cdatasetValues[:,column]= lasenyal.get_signalMag()
            column+= 1
            self.cdatasetValues[:,column]= lasenyal.get_signalPhase()
        else: 
            self.cdatasetValues[:,column]= lasenyal.get_signalReal()
            column+= 1
            self.cdatasetValues[:,column]= lasenyal.get_signalImag()
#             column+= 1
    
    def save_h5Names(self, _component, _variable):
        ''' Creates the .h5, in append mode, with an internal structure for signal names.
        Saves signal names from a specific model. It creates an internal dataset into the current
        group of the current .h5. 
        _component indicates the name of component where the data is collected from 
        _variable list of signal names from the _component'''
#         print 'len ', len(_variable)+ 1
        dt = h5.special_dtype(vlen=unicode)
        if not _component+'_items' in self.cgroup:
            ''' TODO: dataset size according to signals of the component '''
            self.datasetNames= self.cgroup.create_dataset(_component+'_items', (3,len(_variable)+1), dtype=dt)
        else:
            self.datasetNames= self.cgroup[_component+'_items']
        #print "Dataset dataspace is", self.cdatasetNames.shape
        metaSignal= [u"sampletime", u"s", u"int"]
        self.datasetNames[:,0]= metaSignal
        row= 1
        for name in _variable:
#             print row, ' ', str(name)
#             metaSignal= [str(name), u"p.u.", u"polar"]
#             if isinstance(self.dsenyal[name], signal.SignalPMU):
#                 metaSignal= [str(name), u"p.u.", u"polar"]
#             else:
#                 metaSignal= [str(name), u"p.u.", u"complex"]   
            self.cdatasetNames[:,row]= str(name)
            row+= 1
            
    def close_h5(self):
        # close file
        self.ch5file.close()
        