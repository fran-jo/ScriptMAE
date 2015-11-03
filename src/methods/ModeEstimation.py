'''
Created on Sep 23, 2015

@author: fran_jo
'''
import numpy
from scipy import signal
# import win32com.client
from mlab.releases import latest_release as matlab
# import subprocess
# from pymatbridge import Matlab

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
#         if platform.system()== 'Windows':
#             self.win = __import__('win32com.client')
#             '''Opening MATLAB application'''
        
    def get_order(self):
        return self.order
      
    def set_order(self, _value):
        self.order= _value
         
    def get_modeFrequency(self):
        return self.mode_freq
    
    def get_modeDamping(self):
        return self.mode_damp
    
    def modeEstimationMat(self, _name, _signal):
#         # Using java jar
#         subprocess.call(['java','-jar', _name])
#         # Using pymatbridge
#         mlab = Matlab(matlab=u'C:/Program Files/MATLAB/R2012b/bin/matlab.exe')
#         mlab.start()
#         res= mlab.run('./res/mode_est_fcn.m', {'x': _signal.get_sampleTime(), 'y': _signal.get_signalMag(), 'order': 4})
#         print res['result']
#         # Stop the MATLAB server
#         mlab.stop()

        # Using mlabwrap
        x= numpy.array([_signal.get_signalMag(), _signal.get_sampleTime()])
        y= numpy.array([5,0,5,1])
        res= matlab.armax(x,y)

#         ''' 
#         _signal is instance of object src.data.signal
#         '''
#         magnitude= _signal.get_signalMag()
#         '''Opening MATLAB application'''
#         h = win32com.client.Dispatch('matlab.application')
#         h.Execute("cd C:/Users/fragom/PhD_CIM/PYTHON/ScriptMAE/res")
#         ''' Order of the mode estimation function from run configuration Arguments'''
#         h.Execute(self.order)       
#         '''Sending the selected signal i.e Magnitude of Voltage to MATLAB'''
#         h.Execute(magnitude)
#         '''Transposing the array inside the MATLAB'''
#         h.Execute("signal=ans.';")
#         '''performing mode estimation for the magnitude of signal Voltage of order(sys.argv[1])in MATLAB'''
#         '''TODO: Check that matlab is open in a correct way'''
#         h.Execute("[mode_freq, mode_damp]=mode_est_basic_fcn(transpose, order);")
#         self.mode_freq=h.Execute("disp([mode_freq])")
#         self.mode_damp=h.Execute("disp([mode_damp])")
#         
#         print 'mode_freq', self.mode_freq
#         print 'mode_damp', self.mode_damp
    
    def modeEstimationPY(self, _signal):
        '''TODO: Implement modeEstimation in python '''
        '''
        low pass filtering for mode estimation function 
        array must be declared and passed through the function 
        '''
        #pas 1 vedran, design filter
        ''' Wn= length-2 sequence giving the critical frequencies - Fp, Fst parameters from matlab fdesign.lowpass(Fp,Fst,Ap,Ast)
        rp: maximum ripple in the pass band. (dB) - Ap parameter from matlab fdesign.lowpass(Fp,Fst,Ap,Ast)
        rs:  minimum attenuation in the stop band. (dB) - Ast parameter from matlab fdesign.lowpass(Fp,Fst,Ap,Ast)
        '''
        b, a= signal.iirfilter(self.order, Wn=[2/25,2.5/25], rp=0.1, rs=50, btype='lowpass', 
                               analog=True, ftype='cheby2')
        #pas 2 vedran, apply filter
        senalFiltrada= signal.lfilter(b, a, _signal)
        #pas 3 vedran, downsample the signal
        senyal = signal.decimate(_signal, 10, ftype='iir')
        
        #pas 4 vedran, armax, _signal.real or signal.magnitude and signal.sampling data
        angularHz, responseHz = signal.freqs(b, a, senyal)
        
        print 'angular frequency ', angularHz
        print 'frequency response ', responseHz
    
    def dnsample(self,y,order):
        return y[::order];
    
    def transpose_data(self,y):
        return y[:,None];
    
    """ similar like find """
    def find_from_sample(self,y,find_what):
        return numpy.where(y==find_what)[0];
    