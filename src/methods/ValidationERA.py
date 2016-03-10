'''
Created on 20 jan 2016

@author: fragom
'''

import modred as mr
import numpy as np
from scipy import linalg

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
        
    signalOut = property(get_signal_out, set_signal_out, del_signal_out, "signalOut's docstring")
    signalRef = property(get_signal_ref, set_signal_ref, del_signal_ref, "signalRef's docstring")
    
    
class ValidationERA(QuantitativeAnalysis):
    '''
    classdocs
    '''
    __Aout= []
    __Bout= []
    __Cout= []
    __Aref= []
    __Bref= []
    __Cref= []
    __elambdaOut= []
    __vlambdaOut= []
    __elambdaRef= []
    __vlambdaRef= []


    def __init__(self, params):
        '''
        Constructor
        '''

    def calculate_eigenvalues(self):
        ''' eigenvalues and eigen vectors '''
        #first era method
        self.__Aout, self.__Bout, self.__Cout = mr.compute_ERA_model(self._signalOut, 3)
        # second, eigenvalues and eigenvectors
        self.__elambdaOut, self.__vlambdaOut = linalg.eig(self.__Aout)
        self.__Aref, self.__Bref, self.__Cref = mr.compute_ERA_model(self.signalRef, 3)
        # second, eigenvalues and eigenvectors
        self.__elambdaRef, self.__vlambdaRef = linalg.eig(self.__Aref)
    
    
    def get_elambda_out(self):
        return self.__elambdaOut

    def get_vlambda_out(self):
        return self.__vlambdaOut

    def get_elambda_ref(self):
        return self.__elambdaRef

    def get_vlambda_ref(self):
        return self.__vlambdaRef

    def set_elambda_out(self, value):
        self.__elambdaOut = value

    def set_vlambda_out(self, value):
        self.__vlambdaOut = value

    def set_elambda_ref(self, value):
        self.__elambdaRef = value

    def set_vlambda_ref(self, value):
        self.__vlambdaRef = value

    def del_elambda_out(self):
        del self.__elambdaOut

    def del_vlambda_out(self):
        del self.__vlambdaOut

    def del_elambda_ref(self):
        del self.__elambdaRef

    def del_vlambda_ref(self):
        del self.__vlambdaRef

    def get_aout(self):
        return self.__Aout

    def get_bout(self):
        return self.__Bout

    def get_cout(self):
        return self.__Cout

    def get_aref(self):
        return self.__Aref

    def get_bref(self):
        return self.__Bref

    def get_cref(self):
        return self.__Cref

    def set_aout(self, value):
        self.__Aout = value

    def set_bout(self, value):
        self.__Bout = value

    def set_cout(self, value):
        self.__Cout = value

    def set_aref(self, value):
        self.__Aref = value

    def set_bref(self, value):
        self.__Bref = value

    def set_cref(self, value):
        self.__Cref = value

    def del_aout(self):
        del self.__Aout

    def del_bout(self):
        del self.__Bout

    def del_cout(self):
        del self.__Cout

    def del_aref(self):
        del self.__Aref

    def del_bref(self):
        del self.__Bref

    def del_cref(self):
        del self.__Cref

        
    Aout = property(get_aout, set_aout, del_aout, "Aout's docstring")
    Bout = property(get_bout, set_bout, del_bout, "Bout's docstring")
    Cout = property(get_cout, set_cout, del_cout, "Cout's docstring")
    Aref = property(get_aref, set_aref, del_aref, "Aref's docstring")
    Bref = property(get_bref, set_bref, del_bref, "Bref's docstring")
    Cref = property(get_cref, set_cref, del_cref, "Cref's docstring")
    eigenValueOut = property(get_elambda_out, set_elambda_out, del_elambda_out, "elambdaOut's docstring")
    eigenVectorOut = property(get_vlambda_out, set_vlambda_out, del_vlambda_out, "vlambdaOut's docstring")
    eigenValueRef = property(get_elambda_ref, set_elambda_ref, del_elambda_ref, "elambdaRef's docstring")
    eigenVectorRef = property(get_vlambda_ref, set_vlambda_ref, del_vlambda_ref, "vlambdaRef's docstring")
        
