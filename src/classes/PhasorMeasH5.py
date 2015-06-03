'''
Created on 7 apr 2015

@author: fragom
'''
from modelicares import SimRes
import itertools
from numpy import rad2deg,angle,absolute
import os, time
import h5py as h5
from data import signal

class PhasorMeasH5(object):
    '''
    classdocs
    '''
    ch5file= None
    cgroup= None
    cdataset= None

    def __init__(self, params):
        '''
        Constructor
        params[0] = nom del fitxer .mat resultant de simulacio
        params[1] = outPath
        '''
        self.cmatfile= SimRes(params[0])
        os.chdir(params[1])
#         fileName= time.strftime("%H_%M_%S")+ 'SimulationOutputs.h5'
        self.cfileName= 'SimulationOutputs.h5'
        ''' a '''
        self.csenyal= signal.SignalPMU()
        
    def get_csenyal(self):
        return self.csenyal

    def set_csenyal_cmp(self, _nameR, _nameI):
        self.csenyal.set_csignal_r(self.cmatfile['Time'], self.cmatfile[_nameR])
        self.csenyal.set_csignal_i(self.cmatfile['Time'], self.cmatfile[_nameI])
        print 'hdpcmp', self.csenyal.get_csamples()
        
    def set_csenyal_pol(self, _nameM, _nameP):
        self.csenyal.set_csignal_m(self.cmatfile['Time'], self.cmatfile[_nameM])
        self.csenyal.set_csignal_p(self.cmatfile['Time'], self.cmatfile[_nameP])
        print 'hdppol', self.csenyal.get_csamples()

    def del_csenyal(self):
        del self.csenyal
        
    
    senyalCmp = property(get_csenyal, set_csenyal_cmp, del_csenyal, "signalold's docstring")
    senyalPol = property(get_csenyal, set_csenyal_pol, del_csenyal, "signalold's docstring")
    
    
    def pmu_from_cmp(self, a_instance):
        '''Given an instance of A, return a new instance of B.'''
        return signal.SignalPMU(a_instance.field)
    
    def calc_phasorSignal(self):
        pass
        
    def create_h5(self, _component):
        self.ch5file= h5.File(self.cfileName, 'a')
        # create group, for each component, with attribute
        if not _component in self.ch5file:
            self.cgroup= self.ch5file.create_group(_component)
        else:
            self.cgroup= self.ch5file[_component]
    
    def open_h5(self):
        self.ch5file= h5.File(self.cfileName, 'r')
        
    def save_h5(self, _variable):
        # create datasets, llistaSenyals contains els objects Signal que cal guardar per un component concret
        if not _variable in self.cgroup:
            print 'suputamadre', self.csenyal.get_csamples()
            self.cdataset= self.cgroup.create_dataset(_variable, (3, self.csenyal.get_csamples()), chunks=(3, 100))
        else:
            self.cdataset= self.cgroup[_variable]
#         attr_string= 'polar'
#         self.dataset.attrs['signalType']= attr_string
        # store datasets in file
        self.cdataset[0,:]= self.csenyal.get_sampleTime()
        fila= 1
        ''' senyals tenen dos components, complex or polar, es guarden valors per parelles '''
        if isinstance(self.csenyal, signal.SignalPMU):
            print 'mecaguentuputamadre', self.csenyal.get_csignal_m()
            self.cdataset[fila,:]= self.csenyal.get_csignal_m()
            fila+= 1
            self.cdataset[fila,:]= self.csenyal.get_csignal_p()
        else:
            print 'mecaguentuputamadre', self.csenyal.get_csignal_r()
            self.cdataset[fila,:]= self.csenyal.get_csignal_r()
            fila+= 1
            self.cdataset[fila,:]= self.csenyal.get_csignal_i()
        # guardar en attributes els noms de les variables dels components
        # close file
        self.ch5file.close()
        
    def load_h5(self, _bus, _component):
        # load data into internal dataset
        self.group= self.h5file[_bus]
        self.dataset= self.group[_component]