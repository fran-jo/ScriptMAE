'''
Created on 7 apr 2015

@author: fragom
'''
from modelicares import SimRes
import itertools
from numpy import rad2deg,angle,absolute
import os, time
import h5py as h5
from data import signalold

class PhasorMeasH5(object):
    '''
    classdocs
    '''
    _senyal= None
    _matfile= None
    _h5file= None
    group= None
    dataset= None

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
        self._senyal= signalold.Signal('complex')
#         fileName= time.strftime("%H_%M_%S")+ 'SimulationOutputs.h5'
        self._fileName= 'SimulationOutputs.h5'
        
        
    def get_signal(self):
        return self._senyal

    def set_signal(self, _nameR, _nameI):
        self._senyal= signalold.Signal('complex')
        self._senyal.set_sampletime(self._matfile.get_values('Time'))
        self._senyal.set_complexSignal(self._matfile[_nameR], self._matfile[_nameI])

    def del_signal(self):
        del self._senyal


    senyal = property(get_signal, set_signal, del_signal, "signalold's docstring")
#     h5file = property(get_h5file, set_h5file, del_h5file, "h5file's docstring")
    
    def calc_phasorSignal(self):
        ''' copia de objeto Signal a SignalPMU '''
        magnitude= []
        fase= []
        for fasor in self._senyal.get_complexSignal():
            magnitude.append(absolute(fasor[0]+fasor[1]))
            fase.append(angle(fasor[0]+fasor[1], deg=True))
        self._senyal.set_polarSignal(magnitude,fase)
        print 'FDP', len(self._senyal.get_polarSignal())
        
    def create_h5(self, _component):
        self._h5file= h5.File(self._fileName, 'a')
        # create group, for each component, with attribute
        if not _component in self._h5file:
            self.group= self._h5file.create_group(_component)
        else:
            self.group= self._h5file[_component]
    
    def open_h5(self):
        self._h5file= h5.File(self.fileName, 'r')
        
    def save_h5(self, _variable):
        # create datasets, llistaSenyals contains els objects Signal que cal guardar per un component concret
        if not _variable in self.group:
            self.dataset= self.group.create_dataset(_variable, (3, self._senyal.get_samples()), chunks=(3, 100))
        else:
            self.dataset= self.group[_variable]
#         attr_string= 'polar'
#         self.dataset.attrs['signalType']= attr_string
        # store datasets in file
        self.dataset[0,:]= self._senyal.get_sampletime()
        fila= 1
        ''' senyals tenen dos components, complex or polar, es guarden valors per parelles '''
        if isinstance(self._senyal, signalold.SignalPMU):
            print self._senyal.get_magSignal()
            self.dataset[fila,:]= self._senyal.get_magSignal()
            fila+= 1
            self.dataset[fila,:]= self._senyal.get_angSignal()
        else:
            self.dataset[fila,:]= self._senyal.get_realSignal()
            fila+= 1
            self.dataset[fila,:]= self._senyal.get_imagSignal()
        # guardar en attributes els noms de les variables dels components
        # close file
        self.h5file.close()
        
    def load_h5(self, _bus, _component):
        # load data into internal dataset
        self.group= self.h5file[_bus]
        self.dataset= self.group[_component]