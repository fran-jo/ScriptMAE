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
    _senyal= None
    _matfile= None
    h5file= None
    group= None
    dataset= None
#     phasor= None

    def __init__(self, params):
        '''
        Constructor
        params[0] = nom del fitxer .mat resultant de simulacio
        params[1] = outPath
        '''
#         if os.name!= 'posix':
#             print 'not posix', mat, dbFolder
#             mat= params[0].replace('\\','/')
#             dbFolder= params[1].replace('\\','/')
#             print 'not posix', mat, dbFolder
#             self.matfile= SimRes(mat)
#             os.chdir(dbFolder)
#         else:
#             self.matfile= SimRes(params[0])
#             os.chdir(params[1])
        self._matfile= SimRes(params[0])
        os.chdir(params[1])
        self._senyal= signal.Signal('complex')
#         self.phasor= PhasorMeasurement()
#         print params
        self._matfile= SimRes(params[0])
        # create/open the h5 file and append file
        
#         fileName= time.strftime("%H_%M_%S")+ 'SimulationOutputs.h5'
        self.fileName= 'SimulationOutputs.h5'
        
        
    def get_signal(self):
        return self._senyal

    def get_h5file(self):
        return self.h5file

    def set_signal(self, _signalR, _signalI):
        self._senyal= signal.SignalPMU()
        self._senyal.set_complexSignal(self._matfile[_signalR], self._matfile[_signalI])

    def set_h5file(self, value):
        self.h5file = value

    def del_signal(self):
        del self._senyal

    def del_unit(self):
        del self.source

    def del_h5file(self):
        del self.h5file

    senyal = property(get_signal, set_signal, del_signal, "signal's docstring")
    h5file = property(get_h5file, set_h5file, del_h5file, "h5file's docstring")
    
    def calc_phasorSignal(self):
        magnitude= []
        fase= []
        for fasor in self._senyal.get_complexSignal():
            magnitude.append(absolute(fasor[0]+fasor[1]))
            fase.append(angle(fasor[0]+fasor[1], deg=True))
        self._senyal.set_polarSignal(magnitude,fase)
        
    def create_h5(self, _bus):
        self.h5file= h5.File(self.fileName, 'a')
        # create group, for each component, with attribute
        if not _bus in self.h5file:
            self.group= self.h5file.create_group(_bus)
        else:
            self.group= self.h5file[_bus]
    
    def open_h5(self):
        self.h5file= h5.File(self.fileName, 'r')
        
    def save_h5(self, _component, _llistaSenyals):
        # create datasets, llistaSenyals contains els objects Signal que cal guardar per un component concret
        if not _component in self.group:
            self.dataset= self.group.create_dataset(_component, (3, 10000))
        else:
            self.dataset= self.group[_component]
        attr_string= 'polar'
        self.dataset.attrs['signalType']= attr_string
        # store datasets in file
        self.dataset[0,:]= self._senyal.get_sampletime()
        fila= 1
        for s in _llistaSenyals:
            ''' senyals tenen dos components, complex or polar, es guarden valors per parelles '''
            if isinstance(s, signal.Signal):
                self.dataset[fila,:]= s.get_realSignal()
                fila+= 1
                self.dataset[fila,:]= s.get_imagSignal()
                fila+= 1
            if isinstance(s, signal.SignalPMU):
                self.dataset[fila,:]= s.get_magSignal()
                fila+= 1
                self.dataset[fila,:]= s.get_angSignal()
                fila+= 1
        # guardar en attributes els noms de les variables dels components
        # close file
        self.h5file.close()
        
    def load_h5(self, _bus, _component):
        # load data into internal dataset
        self.group= self.h5file[_bus]
        self.dataset= self.group[_component]