'''
Created on Sep 23, 2015

@author: fran_jo
'''
import os, platform
import numpy as np
from scipy import signal

class ModeEstimation(object):
    '''
    classdocs
    '''
    order= 0
    mode_freq= []
    mode_damp= []
    
    def __init__(self):
        '''
        Constructor
        '''
        if platform.system()== 'Windows':
            self.win = __import__('win32com.client')
            '''Opening MATLAB application'''
        
    def get_order(self):
        return self.order
      
    def set_order(self, _value):
        self.order= _value
         
    def get_modeFrequency(self):
        return self.mode_freq
    
    def get_modeDamping(self):
        return self.mode_damp
    
    def modeEstimationMat(self, _signal):
        ''' 
        _signal is instance of object src.data.signal
        '''
        magnitude= _signal.get_signalMag()
        '''Opening MATLAB application'''
        h = self.win.Dispatch('matlab.application')
        ''' Order of the mode estimation function from run configuration Arguments'''
        h.Execute(self.order)       
        '''Sending the selected signal i.e Magnitude of Voltage to MATLAB'''
        h.Execute(magnitude)
        '''Transposing the array inside the MATLAB'''
        h.Execute("transpose=ans.';")
        '''performing mode estimation for the magnitude of signal Voltage of order(sys.argv[1])in MATLAB'''
        h.Execute("[mode_freq, mode_damp]=mode_est_basic_fcn(transpose, order);")
        self.mode_freq=h.Execute("disp([mode_freq])")
        self.mode_damp=h.Execute("disp([mode_damp])")
        
        print 'mode_freq', self.mode_freq
        print 'mode_damp', self.mode_damp
    
    
    def modeEstimationPY(self, _signal):
        '''
        low pass filtering for mode estimation function 
        array must be declared and passed through the function 
        '''
        b,a= signal.iirfilter(17, Wn=0.1, rp=0.1, rs=50, btype='lowpass', analog=True, ftype='cheby2')
        senalFiltrada= signal.lfilter(b,a, _signal)
        angularHz, self.model_freq= signal.freqs(b, a, senalFiltrada)
        
        print 'mode_freq', self.mode_freq
    
    def dnsample(self,y,order):
        return y[::order];
    
    def transpose_data(self,y):
        return y[:,None];
    
    """ similar like find """
    def find_from_sample(self,y,find_what):
        return np.where(y==find_what)[0];
    