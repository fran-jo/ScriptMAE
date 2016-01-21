'''
Created on Sep 23, 2015

@author: fran_jo
'''
import numpy
from scipy import signal
# import win32com.client
# from mlab.releases import latest_release as matlab
import subprocess, os
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
        os.chdir('C:/Users/fragom/PhD_CIM/PYTHON/ScriptMAE/res/matlab')
        scriptme= []
        ''' modify the script with the data to be processed '''
        ''' h5file and dataset '''
        scriptme.append("clc; close all; clear;\n")
        scriptme.append("data= h5read('"+ str(self.h5simoutput)+ "', '"+  str(self.groupName)+ "/"+ str(self.datasetName)+"');\n")
        scriptme.append("do= data(2,:);\n")
        scriptme.append("Y= do.';\n")
        scriptme.append("order= "+ str(self.line_Order.text())+ ";\n")
        scriptme.append("[mode_freq, mode_damp]=mode_est_basic_fcn(Y, order);\n")
        scriptme.append("hdf5write('mode_estimation.h5','/mode_estimation/freq', mode_freq,'/mode_estimation/damp', mode_damp);\n")
        scriptme.append("exit\n")
        filefile = open('./run_mode_estimation.m', 'w') #os.chdir('C:/Users/fragom/PhD_CIM/PYTHON/SimuGUI/res/matlab/') before
        filefile.writelines(scriptme)
        subprocess.call("matlab -r run_mode_estimation")
    
    def modeEstimationPY(self, _signal):
        '''TODO: Implement modeEstimation in python '''
        '''
        low pass filtering for mode estimation function 
        array must be declared and passed through the function 
        '''
        # step 1 vedran, design filter
        ''' Wn= length-2 sequence giving the critical frequencies - Fp, Fst parameters from matlab fdesign.lowpass(Fp,Fst,Ap,Ast)
        rp: maximum ripple in the pass band. (dB) - Ap parameter from matlab fdesign.lowpass(Fp,Fst,Ap,Ast)
        rs:  minimum attenuation in the stop band. (dB) - Ast parameter from matlab fdesign.lowpass(Fp,Fst,Ap,Ast)
        '''
        b, a= signal.iirfilter(self.order, Wn=[2/25,2.5/25], rp=0.1, rs=50, btype='lowpass', 
                               analog=True, ftype='cheby2')
        # step 2 vedran, apply filter
        senalFiltrada= signal.lfilter(b, a, _signal)
        # step 3 vedran, downsample the signal
        senyal = signal.decimate(_signal, 10, ftype='iir')
        
        # step 4 vedran, armax, _signal.real or signal.magnitude and signal.sampling data
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
    