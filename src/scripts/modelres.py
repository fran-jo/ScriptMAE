'''
Created on Sep 03, 2015

@author: ekj05
'''
import numpy as np
import ast
import sys
import win32com.client
from data.signal import SignalPMU
# from classes import PhasorMeasH5, PhasorMeasCSV
from classes.StreamCSVFile import InputCSVStream
from classes.OutputModelVar import OutputModelVar
import modred as MR
import h5py
import time
import pandas as pd

class Validation():
    ''' class for validation, things to do
    TODO: StreamCSVFile read columns according to variable name, (only signal data)
    TODO: StreamH5file read data according to variable name
    TODO: pass the data read to the era method (both simulation and measurement)
    TODO: save the result in the same .h5 file of the simulation
    TODO: use SignalPMU for data coming from CSV file
    '''
    def __init__(self, argv):
        ''' Loading output variables of the model, their values will be stored in h5 and plotted
        argv[0]: file with variable names from the model'''
        
        self.outputs= OutputModelVar(sys.argv[1])
        self.outputs.load_varList()
        
    def load_csvMeas(self, _sourceCSV):
        ''' argv[0]: source file (.h5 or .csv) '''
        
        self.iocsv= InputCSVStream([_sourceCSV, ','])
        for meas, var in self.outputs.get_varList():
            modelSignal.append(var.split(','))
        ''' emulate usecols=(1,2,3,4,5,6) but with variable/measurement names '''
        iocsv.load_csv(modelSignal)
    
    def load_h5Meas(self, _sourceh5):
        pass
    
    t=time.time()
         
    io = pd.read_csv('./res/PMUdata_Bus1VA2VALoad9PQ.csv',sep=",",usecols=(1,2,3,4,5,6))
      
    print io 
    f2=io.to_hdf('PMUdata_Bus1VA2Venam1.h5','df', complib='zlib', complevel=9)


if __name__ == '__main__':
    
    
    
    """ opening the h5 file """
    #File1=h5py.File('Simu.h5','r')
    File1= h5py.File('PMUdata_Bus1VA2Venam1.h5','r')
    
    """ getting the data set from the h5 file """     
    #d1=File1[u'subgroup']
    d1=File1[u'df']
    """ selecting the vector or array from the h5 file """
    #d2=d1['highVoltage']
    d2=d1['block0_values']
    d3=d2[:,1]
    #print d3[0:100]
    a,b,c =MR.compute_ERA_model(d3[0:5000],3)
    """a,b,c =MR.compute_ERA_model(array,5) here 2 is the matrix size of A, B, C  """
    
    print 'printing a matrix'
    #print 'printing matrix a with dimensation ', a.shape
    print a
    print 'printing b matrix'
 
    print b
    print 'printing c matrix'
    print c
    """ creating the file to write the ERA results """
    File2 = h5py.File('noisesignal.h5','w')# 
    
    
    dset3 = File2.create_dataset("ERA_A", data=a)
    dset4 = File2.create_dataset("ERA_B", data=b)
    dset5 = File2.create_dataset("ERA_C", data=c)
    
