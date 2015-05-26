'''
Created on 26 maj 2015

@author: fragom
'''
from math import sqrt
from numpy import arctan2, abs, sin, cos

class Signal(object):
    '''
    classdocs
    '''

    sampletime = []
    signal = []
    valueType = ''
    
    def __init__(self, _valueType):
        '''
        Constructor
        '''
        self.value= _valueType

    def append(self, real, imag):
        valor= (real,imag)
        self.signal.append(valor)
        
        
    def get_value(self):
        return self.__value


    def set_value(self, value):
        self.__value = value


    def del_value(self):
        del self.__value
        

    def get_sampletime(self):
        return self.__sampletime


    def get_signal(self):
        return self.__signal

    def get1stValueSignal(self):
        value1st= []
        for valor in self.__signal:
            value1st.append(valor[0])
        print value1st
        return value1st

    def get2ndValueSignal(self):
        value2nd= []
        for valor in self.__signal:
            value2nd.append(valor[1])
        print value2nd
        return value2nd
    
    def set_sampletime(self, value):
        self.__sampletime = value


    def set_signal(self, value):
        self.__signal = value
        
        
    def del_sampletime(self):
        del self.__sampletime


    def del_signal(self):
        del self.__signal

    sampletime = property(get_sampletime, set_sampletime, del_sampletime, "sampletime's docstring")
    signal = property(get_signal, set_signal, del_signal, "signal's docstring")
    value = property(get_value, set_value, del_value, "value's docstring")
    
    def complex2Polar(self):
        polar= Signal('polar')
        polar.set_sampletime(self.sampletime)
        for valor in self.signal:
            magnitude= abs(sqrt(valor[0]^2+ valor[1]^2))
            angle= arctan2(valor[1], valor[0])
            polar.append(magnitude, angle)
        return polar
    
    def polar2Complex(self):
        complecs= Signal('complex')
        complecs.set_sampletime(self.sampletime)
        for valor in self.signal:
            real= valor[0]* cos(valor[1])
            imag= valor[0]* sin(valor[1])
            complecs.append(real, imag)
        return complecs