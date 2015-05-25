'''
Created on 7 apr 2015

@author: fragom
'''
from modelicares import SimRes
import itertools
from numpy import rad2deg,angle
import os, time
import h5py as h5

from classes.PhasorMeasurement import PhasorMeasurement

class PhasorMeasH5(object):
    '''
    classdocs
    '''
    _signal= []
    _source= ''
    _matfile= None
    _h5file= None
    _phasor= None

    def __init__(self, params):
        '''
        Constructor
        '''
        self._phasor= PhasorMeasurement()
#         print params
        self._matfile= SimRes(params)
        
        
    def get_signal(self):
        return self._signal


    def get_source(self):
        return self._source


    def get_h5file(self):
        return self._h5file


    def get_phasor(self):
        return self._phasor


    def set_signal(self, realvalue, imagvalue):
        vr= self._matfile[realvalue]
        vi= self._matfile[imagvalue]
        #calculate phasor from signal
        self._signal= []
        for r,im in itertools.izip_longest(vr,vi):
            self._signal.append(complex(r,im)) 
    #     print rad2deg(angle(phasor[1]))
    ''' TODO: save time either from OpenModelica Results and Dymola result '''
#         self._phasor.set_time(self._matfile.get_description('Time'))

    def set_source(self, value):
        self._source = value


    def set_h5file(self, value):
        self._h5file = value


    def set_phasor(self, value):
        self._phasor = value


    def del_signal(self):
        del self._signal


    def del_source(self):
        del self._source
        

    def del_h5file(self):
        del self._h5file


    def del_phasor(self):
        del self._phasor
        
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
        self._phasor.set_angle(phase)
        self._phasor.set_magnitude(magnitude)
        self._phasor.set_source(self._source)
        self._phasor.set_unit(self._source)
        
    def save_h5(self, outPath):
        # create the h5 file and append file
        dbFolder= outPath.replace('\\','/')
        os.chdir(dbFolder)
        fileName= time.strftime("%H_%M_%S")+ 'SimulationOutputs.h5'
#         fileName= 'SimulationOutputs.h5'
        self._h5file= h5.File(fileName, 'a')
        # create datasets
        samples= len(self._phasor.get_angle())
        phasorSet= self._h5file.create_dataset(self._phasor.get_source(), (2,samples))
        # store datasets in file
#         phasorSet[0,:]= self._phasor.get_time()
        phasorSet[0,:]= self._phasor.get_magnitude()
        phasorSet[1,:]= self._phasor.get_angle()
        # close file
        self._h5file.close()