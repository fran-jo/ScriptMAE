'''
Created on 12 feb 2016

@author: fragom
'''

import numpy as np
from data import signal

class QuantitativeAnalysis(object):
    '''
    classdocs
    '''
    _signalOut= None
    _signalRef= None
    
    def __init__(self):
        '''
        Constructor
        '''

    def get_signal_out(self):
        return self._signalOut

    def get_signal_ref(self):
        return self._signalRef

    def set_signal_out(self, value):
        self._signalOut = value
        
    def set_signal_ref(self, value):
        self._signalRef = value

    def del_signal_out(self):
        del self._signalOut

    def del_signal_ref(self):
        del self._signalRef

    signalOut = property(get_signal_out, set_signal_out, del_signal_out, "signalOut's docstring")
    signalRef = property(get_signal_ref, set_signal_ref, del_signal_ref, "signalRef's docstring")
        

class StatisticalAnalysis(QuantitativeAnalysis):
    '''
    classdocs
    '''
    
    def qaResampling(self):
        '''
        basic resampling, based on the signal having less samples, assuming same sample time for each signal
        TODO: apply resampling method
        '''
        signaltemp= signal.Signal()
        if self._signalOut.get_samples()< self._signalRef.get_samples():
            samplelen= self._signalOut.get_samples()
            signaltemp.set_signal(self._signalRef.get_sampleTime()[0:samplelen], 
                                  self._signalRef.get_signalMag()[0:samplelen],
                                  self._signalRef.get_signalPhase()[0:samplelen])
            self._signalRef= signaltemp
        if self._signalOut.get_samples()> self._signalRef.get_samples():
            samplelen= self._signalRef.get_samples()
            signaltemp.set_signal(self._signalOut.get_sampleTime()[0:samplelen], 
                                  self._signalOut.get_signalReal()[0:samplelen],
                                  self._signalOut.get_signalImag()[0:samplelen])
            self._signalOut= signaltemp
        
        signaltemp= None
           
    def qaMAPE(self):
        arrayRef= np.array(self._signalRef.get_signalReal())
        arrayOut= np.array(self._signalOut.get_signalReal())
        mape= np.mean(np.divide(np.abs(np.subtract(arrayOut,arrayRef)), np.abs(arrayOut)))* 100
        return mape
        
    def qaErrorValidation(self):
        arrayRef= np.array(self._signalRef.get_signalReal())
        arrayOut= np.array(self._signalOut.get_signalReal())
        mae= np.mean(arrayOut - arrayRef)
        mse= np.mean(np.power(arrayOut - arrayRef, 2))
        rmse= np.sqrt(np.mean(np.power(arrayOut - arrayRef, 2)))
        return mae, mse, rmse
    
    def qaSignalError(self):
        error= np.subtract(np.array(self._signalRef.get_signalReal()), np.array(self._signalOut.get_signalReal()))
        #TODO error signal must be a new object signal with own sampletime
        return error
    
    ''' TODO: MAPE, MASE, sMAPE, GRMSE '''
    ''' this statistics offer interpretation for forecasting / prediction. RMSE, MSE and MAE are suitable for comparison of signals'''
    