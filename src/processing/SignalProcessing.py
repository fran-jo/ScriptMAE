'''
Created on 5 apr. 2017

@author: fragom
'''

import PyCIM
import CIM15.IEC61970.Meas as meas

class SignalProcessing(object):
    '''
    classdocs
    '''
    _signalSimulation= None
    _signalMeasurement= None

    def __init__(self, params):
        '''
        Constructor
        '''
        self._signalSimulation= params[0]
        self._signalMeasurement= params[1]
        
    def resampling(self):
        '''
        basic resampling, based on the signal having less samples, assuming same sample time for each signal
        TODO: apply resampling method
        '''
        signaltemp= signal.Signal()
        if self._signalOut.samples< self._signalRef.samples:
            samplelen= self._signalOut.samples
            signaltemp.set_signal(self._signalRef.sampletime[0:samplelen], 
                                  self._signalRef.magnitude[0:samplelen],
                                  self._signalRef.phase[0:samplelen])
            self._signalRef= signaltemp
        if self._signalOut.samples> self._signalRef.samples:
            samplelen= self._signalRef.samples
            signaltemp.set_signal(self._signalOut.sampletime[0:samplelen], 
                                  self._signalOut.magnitude[0:samplelen],
                                  self._signalOut.phase[0:samplelen])
            self._signalOut= signaltemp
        
        signaltemp= None
        
    def _interpolation(self):
        #pass   