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
    cdataset= None

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

    def get_cdataset(self):
        return self.cdataset

    def set_cgroup(self, value):
        self.cgroup = value


    def set_cdataset(self, value):
        self.cdataset = value

    def del_cgroup(self):
        del self.cgroup
        
    def del_cdataset(self):
        del self.cdataset

        
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
            emptyarray= [0 for x in self.cmatfile[nameVarTime]]
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
            emptyarray= [0 for x in self.cmatfile[nameVarTime]]
            csenyal.set_signalPolar(self.cmatfile[nameVarTime], self.cmatfile[_nameM], emptyarray)
        self.dsenyal[_variable]= csenyal
        
    def del_senyal(self):
        del self.csenyal
    
    
    group = property(get_cgroup, set_cgroup, del_cgroup, "cgroup's docstring")
    dataset = property(get_cdataset, set_cdataset, del_cdataset, "cdataset's docstring")
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
         
    def load_h5(self, _network, _component, _variable):
        ''' 
        Loads signal data from a specific variable form a specific component 
        _network name of the entire network model or area inside the model
        _component is the name of the component we are working with
        _variable is the name of the variable that contains signal data, from the specified component 
        '''
        # load data into internal dataset
        self.cgroup= self.ch5file[_network]
        self.cdataset= self.cgroup[_component+'_values']
        self.cdatasetNames= self.cgroup[_component+'_items']
        idx= 1
        for item in self.cdatasetNames:
            print idx, item
            if (item == _variable):
                if self.cdataset.attrs['coord']== 'polar':
                    print 'polar'
                    csenyal= signal.SignalPMU()
                    csenyal.set_signalPolar(self.cdataset[:,0], self.cdataset[:,idx], self.cdataset[:,idx+1])
                else:
                    print 'complex'
                    csenyal= signal.Signal()
                    csenyal.set_signalRect(self.cdataset[:,0], self.cdataset[:,idx], self.cdataset[:,idx+1])
                self.dsenyal[_component]= csenyal
            idx+= 1
            
    def close_h5(self):
        self.ch5file.close()
        