'''
Created on Jun 18, 2015
This script test the use of the Mode estimate function inside python environment

@author: ekj05
'''
import numpy as np
import ast
import sys
import win32com.client
from data.signal import SignalPMU
from ctrl import PhasorMeasH5, PhasorMeasCSV
from data.Mode import Mode

if __name__ == '__main__':
    
    '''Opening MATLAB application'''
    h = win32com.client.Dispatch('matlab.application')
    ''' Order of the mode estimation function from run configuration Arguments'''
    h.Execute(sys.argv[1])
    '''load data from h5 File '''
    File1= PhasorMeasH5.PhasorMeasH5(sys.argv[4:])
    File1.open_h5()
    '''(sys.argv[2], sys.argv[3]) is the pwLine4 and its Voltage V respectively given in the arguments'''
    #File1.load_h5('pwLine4', 'V')
    File1.load_h5(sys.argv[2], sys.argv[3])
    '''getting the specified signal'''
    objectsignal= File1.get_senyal()#h5pmu.get_senyal()
    Mag= objectsignal.get_signalMag()
    #print Mag
    Rel= objectsignal.get_signalReal()
    #print Rel
    '''Sending the selected signal i.e Magnitude of Voltage to MATLAB'''
    h.Execute(Mag)
    '''Transposing the array inside the MATLAB'''
    h.Execute("transpose=ans.';")
    '''performing mode estimation for the magnitude of signal Voltage of order(sys.argv[1])in MATLAB'''
    h.Execute("[mode_freq, mode_damp]=mode_est_basic_fcn(transpose, order);")
    mode_freq=h.Execute("disp([mode_freq])")
    mode_damp=h.Execute("disp([mode_damp])")
    
    ''' printing mode_freq and mode_damp output to present in Python console'''
    
    print 'mode_freq'
    print mode_freq
    print 'mode_damp'
    print mode_damp
    

    '''splitting the string outputs coming from MATLAB Mode estimation function'''
    mode_freq_for_Mod=mode_freq.split()
    mode_damp_for_Mod=mode_damp.split()
    
    
    '''calling Mode class to store the mode estimation output'''
    C = Mode()
    ''' using setter and getters of Mode class'''
    C.set_mode_freq(mode_freq_for_Mod)
    C.set_mode_damp(mode_damp_for_Mod)
    savingSignal_test1=C.get_mode_freq()
    savingSignal_test2=C.get_mode_freq()
    ''' printing a single output from Mode class for each array of frequency and Damp'''
    print 'freq:'+savingSignal_test1[1]
    print 'damp:'+savingSignal_test2[1]

    
''' csvpmu= PhasorMeasCSV.PhasorMeasCSV(sys.argv[1],',') '''
#     1) load data from .csv or .h5 (format of the data? engineering value? p.u.?
#     2) if necessary, process data from sources to the format for the Mode estimate functions
#     3) call the Mode estimate function
#     4) store outputs from Mode estimate functions into Mode class
#     5) print results
    
