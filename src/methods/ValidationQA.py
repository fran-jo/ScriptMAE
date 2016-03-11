'''
Created on 12 feb 2016

@author: fragom
'''

import numpy as np
from data import signal
from validationMethod import ValidationMethod
        

class StatisticalAnalysis(ValidationMethod):
    '''
    classdocs
    '''
    def __init__(self, params):
        '''
        Constructor
        '''
        super(StatisticalAnalysis, self).__init__(params)
        
    def qaResampling(self):
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
            
    def compute_method(self, parametro):
        switcher = {
            'MAE': self.qaMAE,
            'MSE': self.qaMSE,
            'RMSE': self.qaRMSE,
        }
        # Get the function from switcher dictionary
        func = switcher[parametro]
        # Execute the function
        self._scalarOutput= func()
    
    def qaMAPE(self):
        arrayRef= np.array(self._signalRef.magnitude)
        arrayOut= np.array(self._signalOut.magnitude)
        mape= np.mean(np.divide(np.abs(np.subtract(arrayOut,arrayRef)), np.abs(arrayOut)))* 100
        arrayRef= arrayOut= None
        return mape
        
    def qaMAE(self):
        arrayRef= np.array(self._signalRef.magnitude)
        arrayOut= np.array(self._signalOut.magnitude)
        mae= np.mean(arrayOut - arrayRef)
        arrayRef= arrayOut= None
        return mae
    
    def qaMSE(self):
        arrayRef= np.array(self._signalRef.magnitude)
        arrayOut= np.array(self._signalOut.magnitude)
        mse= np.mean(np.power(arrayOut - arrayRef, 2))
        arrayRef= arrayOut= None
        return mse
    
    def qaRMSE(self): 
        arrayRef= np.array(self._signalRef.magnitude)
        arrayOut= np.array(self._signalOut.magnitude)
        rmse= np.sqrt(np.mean(np.power(arrayOut - arrayRef, 2)))
        arrayRef= arrayOut= None
        return rmse
    
    def qaSignalError(self):
        error= np.subtract(np.array(self._signalRef.magnitude), np.array(self._signalOut.magnitude))
        #TODO error signal must be a new object signal with own sampletime
        return error
    