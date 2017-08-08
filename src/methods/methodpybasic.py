'''
Created on 3 aug. 2017

@author: fragom
'''
from inout.streammodeh5 import StreamModeH5
from scipy import signal
import statsmodels.api as smapi
from data.EigenValue import EigenValue

class MethodAmbientAnalysis(object):
    
    __simulationsSignal= []
    __measurementSignal= []
    __order= 0
    __simulationModes= []
    __measurementModes= []
    
    def __init__(self, simulationSignal, measurementSignal, order= 4, parent= None):
        self.__simulationsSignal= simulationSignal
        self.__measurementSignal= measurementSignal
        self.__order= order
       
    @property
    def simulationModes(self):
        return self.__simulationModes
    @property
    def measurementModes(self):
        return self.__measurementModes
#     @modes.setter
#     def modes(self, value):
#         self.__modes= value 
    @property
    def toolDir(self):
        return self.__toolDir
    @toolDir.setter
    def toolDir(self, value):
        self.__toolDir= value 
     
    def run(self):
        print 'log: Ambient Mode Analysis in Python'
        self.__method()

    def __method(self):
        # TODO Check CPU time
        '''
        low pass filtering for mode estimation function 
        array must be declared and passed through the function 
        '''
        # step 1 vedran, design filter
        ''' Wn= length-2 sequence giving the critical frequencies - Fp, Fst parameters from matlab fdesign.lowpass(Fp,Fst,Ap,Ast)
        rp: maximum ripple in the pass band. (dB) - Ap parameter from matlab fdesign.lowpass(Fp,Fst,Ap,Ast)
        rs:  minimum attenuation in the stop band. (dB) - Ast parameter from matlab fdesign.lowpass(Fp,Fst,Ap,Ast)
        '''
        b, a= signal.iirfilter(self.__order, Wn=[2/25,2.5/25], rp=0.1, rs=50, btype='lowpass', 
                               analog=True, ftype='cheby2')
        # step 2 vedran, apply filter
        simsignalFilter= signal.lfilter(b, a, self.__simulationsSignal)
        # step 3 vedran, downsample the signal
        simsignalsampled = signal.decimate(simsignalFilter, 10, ftype='iir')
        # step 4 with signal.freqs(b,a,y) we obtain frequency response of the signal
        freqHz, amplitude = signal.freqs(b, a, simsignalsampled)
        print 'angular frequency ', freqHz
        print 'amplitude response ', amplitude
        for vfreq, vdamp in zip(freqHz, amplitude):
            mode= EigenValue(vfreq,vdamp)
            self.__simulationModes.append(mode)
        # step 2 vedran, apply filter
        maessignalFilter= signal.lfilter(b, a, self.__measurementSignal)
        # step 3 vedran, downsample the signal
        maessignalsampled = signal.decimate(maessignalFilter, 10, ftype='iir')
        # step 4 with signal.freqs(b,a,y) we obtain frequency response of the signal
        freqHz, amplitude = signal.freqs(b, a, maessignalsampled)
        print 'angular frequency ', freqHz
        print 'amplitude response ', amplitude
        for vfreq, vdamp in zip(freqHz, amplitude):
            mode= EigenValue(vfreq,vdamp)
            self.__simulationModes.append(mode)
        # step 4 vedran, armax, _signal.real or signal.magnitude and signal.sampling data
        sys_ident= smapi.tsa.ARMA(simsignalsampled, order=(self.__order,self.__order)).fit()
        print sys_ident
        sys_ident= smapi.tsa.ARMA(maessignalsampled, order=(self.__order,self.__order)).fit()
        print sys_ident
        # sys_ident contains poles of the system and frequency related to this poles (modes), so we can apply 
        # definition of Natural Frequency -> Omega_n= abs(pole) and Damping ratio -> -cos(angle(pole))

