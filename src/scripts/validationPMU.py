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
from classes.StreamH5File import InputH5Stream
from classes.OutputModelVar import OutputModelVar
import modred as MR
import h5py
import time
import pandas as pd

class Validation():
    ''' class for validation, things to do
    TODO: pass the data read to the era method (both simulation and measurement)
    TODO: save the result in the same .h5 file of the simulation
    TODO: use SignalPMU for data coming from CSV file
    '''
    def __init__(self, _variables):
        ''' Loading output variables of the model, their values will be stored in h5 and plotted
        argv[0]: file with variable names from the model
        '''
        self.outputs= OutputModelVar(_variables)
        self.outputs.load_varList()
        self.measurements= []
        
        
    def load_sources(self, _sourceCSV, _sourceH5, _model, _component, _name):
        ''' 
        _sourceCSV: .csv file, i.e. ./res/File_8.csv
        _sourceH5: .h5 file, i.e. './res/PMUdata_Bus1VA2VALoad9PQ.h5'
        '''
        if (_sourceCSV != ''):
            self.iocsv= InputCSVStream(_sourceCSV, ',')
            ''' select the signals according to variables '''
            ''' name is the representation of the measurement 
            meas signals/variables that name the signal of a measurement
            i.e: name KTHLAB:EMLAB; meas KTHLAB:EMLAB:Magnitude,KTHLAB:EMLAB:Angle 
            i.e: name bus1.V; meas bus1.v,bus1.angle '''
            for name, meas in self.outputs.get_varList():
                self.measurements.append(name)
                measSignals= meas.split(',')
#                 print measSignals[0], ' - ', measSignals[1]
                self.iocsv.load_csvValues(name, measSignals[0], measSignals[1])
            self.iocsv.timestamp2sample(name)
#             print self.iocsv.get_senyal(name)
        if (_sourceH5 != ''):
            self.ioh5= InputH5Stream(_sourceH5)
            self.ioh5.open_h5()
            self.ioh5.load_h5(_model, _component, _name)
#             print self.ioh5.get_senyal('block0')
        
    def load_pandaSource(self, _sourceCSV, _sourceH5, _modelName, _component, _variable):
        '''
        _sourceCSV: something like './res/PMUdata_Bus1VA2VALoad9PQ.csv'
        _sourceH5: something like 'PMUdata_Bus1VA2Venam1.h5'
        '''
        csvData = pd.read_csv(_sourceCSV,sep=",",usecols=(1,2,3,4,5,6))
        csvData.to_hdf(_sourceH5,'df', complib='zlib', complevel=9)  
        self.ioh5.open_exth5(_sourceH5)
        self.ioh5.open_load_h5(_modelName, _component, _variable)
#         return self.iocsv.get_senyal('KTHLAB:EMLAB'), self.ioh5.get_senyal('block0')
#         return (csvData, self.ioh5.get_senyal('block0'))

    def get_sources(self, _measurement, _component):
        ''' _measurement> 'KTHLAB:EMLAB'
        _component> 'block0'
        '''
        return [self.iocsv.get_senyal(_measurement), self.ioh5.get_senyal(_component)]
    
    def method_ME(self, _measSignal, _simSignal):
        ''' TODO: create a subset of signals from original signal in object senyal
        call mode estimation method with each subset, inside a loop '''
        ''' TODO: pass the whole signal to Vedran mode estimation '''
        pass
        
    def method_ERA(self, _measSignal, _simSignal, _winSamples):
        """ opening the h5 file """
        #File1=h5py.File('Simu.h5','r')
        ''' using solution from load_pandaSource '''
#         h5Data= h5py.File(_sourceH5,'r')
        senyal = self.ioh5.get_senyal('block0')
        ''' format of the signal (sampletime, real/magnintude, imag/polar) '''
        """ getting the data set from the h5 file """     
        #d1=File1[u'subgroup']
#         d1= h5Data[u'df']
        """ selecting the vector or array from the h5 file """
        #d2=d1['highVoltage']
#         d2=d1['block0_values']
#         d3=d2[:,1]
        #print d3[0:100]
        ''' TODO: create a subset of signals from original signal in object senyal
        call era method with each subset, inside a loop '''
        a,b,c =MR.compute_ERA_model(d3[0:5000],3)
#         while ()
#             a,b,c =MR.compute_ERA_model(d3[0:_winSamples],3)
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
    
#     def method_whatever(self):
#         pass    

def main(argv):
    smith= Validation(sys.argv[3])
    ''' model> 'df', 
    component> 'block0', 
    signal> 'bus9.v'
    '''
#     smith.load_sources(sys.argv[1], sys.argv[2], 'model', 'component', 'signal')
    smith.load_pandaSource(sys.argv[1], sys.argv[2], 'df', 'block0', 'bus9.v')
    [measurement, simulation]= smith.get_sources('KTHLAB:EMLAB', 'block0')
    ''' TODO: function for each method '''
    smith.method_ME(measurement, simulation)
    ''' TODO: how to indicate the method to use? input parameter'''

if __name__ == '__main__':
    main(sys.argv[1:])
    
#     """ opening the h5 file """
#     #File1=h5py.File('Simu.h5','r')
#     File1= h5py.File('PMUdata_Bus1VA2Venam1.h5','r')
#     
#     """ getting the data set from the h5 file """     
#     #d1=File1[u'subgroup']
#     d1=File1[u'df']
#     """ selecting the vector or array from the h5 file """
#     #d2=d1['highVoltage']
#     d2=d1['block0_values']
#     d3=d2[:,1]
#     #print d3[0:100]
#     a,b,c =MR.compute_ERA_model(d3[0:5000],3)
#     """a,b,c =MR.compute_ERA_model(array,5) here 2 is the matrix size of A, B, C  """
#     
#     print 'printing a matrix'
#     #print 'printing matrix a with dimensation ', a.shape
#     print a
#     print 'printing b matrix'
#  
#     print b
#     print 'printing c matrix'
#     print c
#     """ creating the file to write the ERA results """
#     File2 = h5py.File('noisesignal.h5','w')# 
#     
#     
#     dset3 = File2.create_dataset("ERA_A", data=a)
#     dset4 = File2.create_dataset("ERA_B", data=b)
#     dset5 = File2.create_dataset("ERA_C", data=c)
    
