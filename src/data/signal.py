'''
Created on 26 maj 2015

@author: fragom
'''
import itertools
from __builtin__ import str

class Signal(object):
    '''
    classdocs, clase base trabaja con complejos
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        self.__samples= 0
        self.__signal = []
        self.__component= ''

    def get_csamples(self):
        ''' return the number of samples of the singal '''
        return self.__samples

    
    def get_signal(self):
        ''' return the signal in rectangular form '''
        return self.__signal
    
    def get_sampleTime(self):
        ''' returns an array with values of sample/time '''
        series= []
        for s,r,i in self.__signal:
            series.append(s)
        return series 
    
    def get_signalReal(self):
        ''' returns an array with real component of the signal'''
        series= []
        for s,r,i in self.__signal:
            series.append(r)
        return series    
        
    def get_signalImag(self):
        ''' returns an array with imaginary component of the signal '''
        series= []
        for s,r,i in self.__signal:
            series.append(i)
        return series    

    def get_ccomponent(self):
        ''' returns the name of the component which the signal belongs to '''
        return self.__component  


    def set_csamples(self, _value):
        ''' _value: input sample/time array '''
        self.__samples = len(_value)
      
    def set_signalRect(self, _samples, _valueR, _valueI):
        ''' create dictionary with real part of the complex signal
        _samples:
        _valueR: '''
        self.__signal= [(s,r,i) for s,r,i in zip(_samples, _valueR, _valueI)]
        self.__samples= len(self.__signal)


    def set_ccomponent(self, value):
        ''' set the name of the component which the signal belongs to '''
        self.__component = value


    def del_csamples(self):
        del self.__samples


    def del_signal(self):
        del self.__signal


    def del_ccomponent(self):
        del self.__component


    sampleTime= property(get_sampleTime)
    realValue= property(get_signalReal)
    imaginaryValue= property(get_signalImag)


    def __str__(self):
        estrin= self.__component+ " "+ str(self.__samples)+ " samples: "
        return estrin
    
    def __repr__(self):
        return self.__str__()
        
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

    
    def get_signal(self):
        ''' return the signal in rectangular form '''
        return self.csignalpmu
    
    def get_signalMag(self):
        ''' returns an array with magnitude component of the signal '''
        series= []
        for s,m,p in self.csignalpmu:
            series.append(m)
        return series    
        
    def get_signalPhase(self):
        ''' returns an array with phase component of the signal '''
        series= []
        for s,m,p in self.csignalpmu:
            series.append(p)
        return series    
    
    
    def set_signalPolar(self, _samples, _valueM, _valueP):
        ''' create dictionary with real part of the complex signal
        _samples:
        _valueR: '''
        self.csignalpmu= [(s,r,i) for s,r,i in zip(_samples, _valueM, _valueP)]
        self.__samples= len(self.csignalpmu)


    def del_signal(self):
        del self.csignalpmu
        
        
    signalPolar = property(get_signal, set_signalPolar, del_signal, "csignal_pol's docstring")


    def complex2Polar(self):
        pass
    
    def polar2Complex(self):
        pass    
    
