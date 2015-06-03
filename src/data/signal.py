'''
Created on 26 maj 2015

@author: fragom
'''
import itertools

class Signal(object):
    '''
    classdocs, clase base trabaja con complejos
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        self.csamples= 0
        self.csignal_r = {}
        self.csignal_i = {}
        self.ccomponent= ''

    def get_csamples(self):
        return self.csamples

    def get_sampleTime(self):
        ''' returns an array with values of sample/time '''
        return self.csignal_r.keys()
    
    def get_csignal_r(self):
        return self.csignal_r.values()


    def get_csignal_i(self):
        return self.csignal_i.values()


    def get_ccomponent(self):
        return self.ccomponent


    def set_csamples(self, _value):
        ''' _value: input sample/time array '''
        self.csamples = len(_value)


    def set_csignal_r(self, _samples, _valueR):
        ''' create dictionary with real part of the complex signal
        _samples:
        _valueR: '''
        self.csignal_r = dict(zip(_samples,_valueR))
        self.csamples= len(_samples)


    def set_csignal_i(self, _samples, _valueI):
        ''' create dictionary with imaginary part of the complex signal
        _samples:
        _valueR: '''
        self.csignal_i = dict(zip(_samples,_valueI))


    def set_ccomponent(self, value):
        self.ccomponent = value


    def del_csamples(self):
        del self.csamples


    def del_csignal_r(self):
        del self.csignal_r


    def del_csignal_i(self):
        del self.csignal_i


    def del_ccomponent(self):
        del self.ccomponent

    samples = property(get_csamples, set_csamples, del_csamples, "csamples's docstring")
    signal_r = property(get_csignal_r, set_csignal_r, del_csignal_r, "csignal_a's docstring")
    signal_i = property(get_csignal_i, set_csignal_i, del_csignal_i, "csignal_b's docstring")
    component = property(get_ccomponent, set_ccomponent, del_ccomponent, "ccomponent's docstring")

        
from math import sqrt
from numpy import arctan2, abs, sin, cos

class SignalPMU(Signal):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor, clase que trabaja con representacion polar'''
        ''' oye, convierte las arrays en dictionarios, el key value siempre must be el tiempo, so
        self.signal = {(magnitude, angle)}
        '''
        Signal.__init__(self)
        self.csignal_m = {}
        self.csignal_p = {}

    def get_csignal_m(self):
        return self.csignal_m.values()


    def get_csignal_p(self):
        return self.csignal_p.values()
    

    def set_csignal_m(self, _samples, _valueM):
        ''' create dictionary with magnitude part of the complex signal
        _samples:
        _valueM: '''
        self.csignal_m = dict(zip(_samples,_valueM))
        self.csamples= len(_samples)


    def set_csignal_p(self, _samples, _valueP):
        ''' create dictionary with magnitude part of the complex signal
        _samples:
        _valueP: '''
        self.csignal_p = dict(zip(_samples,_valueP))


    def del_csignal_m(self):
        del self.csignal_m


    def del_csignal_p(self):
        del self.csignal_p

    signal_m = property(get_csignal_m, set_csignal_m, del_csignal_m, "csignal_m's docstring")
    signal_p = property(get_csignal_p, set_csignal_p, del_csignal_p, "csignal_p's docstring")


    def complex2Polar(self):
        pass
    
    def polar2Complex(self):
        pass    
    
