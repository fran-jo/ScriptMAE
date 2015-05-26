'''
Created on 7 apr 2015

@author: fragom
'''
from modelicares import SimRes
import itertools
from numpy import rad2deg,angle
import os, time
import h5py as h5
from data import signal

from classes.PhasorMeasurement import PhasorMeasurement

class PhasorMeasH5(object):
    '''
    classdocs
    '''
    signal= None
    mode= []
    signaltype= ''
    source= ''
    matfile= None
    h5file= None
#     phasor= None

    def __init__(self, params):
        '''
        Constructor
        params[0] = nom del fitxer .mat resultant de simulació
        params[1] = outPath
        '''
        self.signal = signal.Signal('complex')
#         self.phasor= PhasorMeasurement()
#         print params
        self.matfile= SimRes(params[0])
        # create/open the h5 file and append file
        dbFolder= params[1].replace('\\','/')
        os.chdir(dbFolder)
#         fileName= time.strftime("%H_%M_%S")+ 'SimulationOutputs.h5'
        fileName= 'SimulationOutputs.h5'
        self.h5file= h5.File(fileName, 'a')
        
        
    def get_signal(self):
        return self.signal


    def get_source(self):
        return self.source


    def get_h5file(self):
        return self.h5file


    def get_phasor(self):
        return self.phasor


    def set_signal(self, realvalue, imagvalue):
        vr= self.matfile[realvalue]
        vi= self.matfile[imagvalue]
        #calculate phasor from signal
        self.signal= []
        for r,im in itertools.izip_longest(vr,vi):
            self.signal.append(complex(r,im)) 
    #     print rad2deg(angle(phasor[1]))
    ''' TODO: save time either from OpenModelica Results and Dymola result '''
#         self._phasor.set_time(self._matfile.get_description('Time'))

    def set_mode(self, realvalue):
        pass
    
    def set_source(self, value):
        self.source = value

    def set_h5file(self, value):
        self.h5file = value

    def set_phasor(self, value):
        self.phasor = value

    def del_signal(self):
        del self.signal

    def del_source(self):
        del self.source

    def del_h5file(self):
        del self.h5file

    def del_phasor(self):
        del self.phasor
        
    signal = property(get_signal, set_signal, del_signal, "signal's docstring")
    source = property(get_source, set_source, del_source, "source's docstring")
    h5file = property(get_h5file, set_h5file, del_h5file, "h5file's docstring")
    phasor = property(get_phasor, set_phasor, del_phasor, "phasor's docstring")
    
    def calc_phasorSignal(self):
        magnitude= []
        phase= []
        for fasor in self._signal:
            magnitude.append(abs(fasor));
            phase.append(rad2deg(angle(fasor)))
        self.phasor.set_angle(phase)
        self.phasor.set_magnitude(magnitude)
        self.phasor.set_source(self._source)
        self.phasor.set_unit(self._source)
        
    def save_h5(self, _component, _variable):
        
        # create group, for each component
        if not _component in self.h5file:
            comp= self.h5file.create_group(_component)
        # create datasets
        samples= len(self.phasor.get_angle())
        signalSet= comp.create_dataset(_variable, (3, samples))
#         dset = self.h5file.create_dataset(self._phasor.get_source(), (2,samples))
        # store datasets in file
#         phasorSet[0,:]= self._phasor.get_time()
        signalSet[0,:]= self.signal.get_sampletime()
        signalSet[1,:]= self.signal.get1stValueSignal()
        signalSet[2,:]= self.signal.get2ndValueSignal()
        # close file
        self.h5file.close()