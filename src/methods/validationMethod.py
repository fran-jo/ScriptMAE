'''
Created on 11 mar 2016

@author: fragom
'''

import numpy as np

class ValidationMethod(object):
    '''
    classdocs
    '''
    _signalOut= []
    _signalRef= []
    _scalarOutput= 0
    _vectorOutput= []
    
    def __init__(self, params):
        self._signalOut= params[0]
        self._signalRef= params[1]

    def get_scalar_output(self):
        return self._scalarOutput

    def get_vector_output(self):
        return self._vectorOutput

    def set_scalar_output(self, value):
        self._scalarOutput = value

    def set_vector_output(self, value):
        self._vectorOutput = value

    def del_scalar_output(self):
        del self._scalarOutput

    def del_vector_output(self):
        del self._vectorOutput


    def get_signal_out(self):
        return self._signalOut

    def get_signal_ref(self):
        return self._signalRef

    def set_signal_out(self, value):
        self._signalOut = np.array(value)

    def set_signal_ref(self, value):
        self._signalRef = np.array(value)

    def del_signal_out(self):
        del self._signalOut

    def del_signal_ref(self):
        del self._signalRef
        
    def compute_method(self, parametro= None):
        pass
        
    signalOut = property(get_signal_out, set_signal_out, del_signal_out, "signalOut's docstring")
    signalRef = property(get_signal_ref, set_signal_ref, del_signal_ref, "signalRef's docstring")
    scalarOutput = property(get_scalar_output, set_scalar_output, del_scalar_output, "scalarOutput's docstring")
    vectorOutput = property(get_vector_output, set_vector_output, del_vector_output, "vectorOutput's docstring")
