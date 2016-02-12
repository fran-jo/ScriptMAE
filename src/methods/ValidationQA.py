'''
Created on 12 feb 2016

@author: fragom
'''

import numpy as np

class QuantitativeAnalysis(object):
    '''
    classdocs
    '''
    _signalOut= []
    _signalRef= []
    
    def __init__(self, params):
        '''
        Constructor
        '''
        self._signalOut= params[0]
        self._signalRef= params[1]


    def get_signal_out(self):
        return self.__signalOut

    def get_signal_ref(self):
        return self.__signalRef

    def set_signal_out(self, value):
        self.__signalOut = value

    def set_signal_ref(self, value):
        self.__signalRef = value

    def del_signal_out(self):
        del self.__signalOut

    def del_signal_ref(self):
        del self.__signalRef

    signalOut = property(get_signal_out, set_signal_out, del_signal_out, "signalOut's docstring")
    signalRef = property(get_signal_ref, set_signal_ref, del_signal_ref, "signalRef's docstring")
        

class StatisticalAnalysis(QuantitativeAnalysis):
    
    def qaRMSE(self):
        arrayRef= np.array(self._signalRef)
        arrayOut= np.array(self._signalOut)
        mse= np.mean(np.power(arrayRef - arrayOut, 2))
        rmse= np.sqrt(np.mean(np.power(arrayRef - arrayOut, 2)))
        return mse, rmse
    
    def qaSignalError(self):
        error= np.subtract(np.array(self._signalRef), np.array(self._signalOut))
        return error
    