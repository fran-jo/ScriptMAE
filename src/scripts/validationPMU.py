'''
Created on Sep 03, 2015

@author: ekj05
'''
import sys
from methods.ModeEstimation import ModeEstimation
from methods.ERAMethod import ERAMethod
from data.signal import SignalPMU
from ctrl.StreamCSVFile import InputCSVStream
from ctrl.StreamH5File import InputH5Stream
from ctrl.OutputModelVar import OutputModelVar
import modred as mr
import pandas as pd
import numpy

class Validation():
    ''' class for validation, things to do
    TODO: pass the data read to the era method (both simulation and measurement)
    TODO: save the result in the same .h5 file of the simulation
    '''
    def __init__(self, _variables):
        ''' Loading output variables of the model, their values will be stored in h5 and plotted
        argv[0]: file with variable names from the model
        '''
        self.outputs= OutputModelVar(_variables)
        self.outputs.load_varList()
        print self.outputs.get_varList()
        self.measurements= []
        
    def load_sourcesCSV(self, _sourceCSV, _component, _signalComplex):
        ''' 
        _sourceCSV: .csv file, i.e. ./res/File_8.csv
        _sourceH5: .h5 file, i.e. './res/PMUdata_Bus1VA2VALoad9PQ.h5'
        _model: name of the model , for retrieving the h5.group
        _component: name of the component, for retrieving the h5.dataset
        _name: name of the signal, for retrieving the signal values from the h5.dataset and 
        signal values from the .csv file
        '''
        if (_sourceCSV != ''):
            self.iocsv= InputCSVStream(_sourceCSV, ',')
            ''' select the signals according to variables '''
            ''' name is the representation of the measurement 
            meas signals/variables that name the signal of a measurement
            i.e: name KTHLAB:EMLAB; meas KTHLAB:EMLAB:Magnitude,KTHLAB:EMLAB:Angle 
            i.e: name bus1.V; meas bus1.v,bus1.angle '''
            self.iocsv.load_csvValues(_component, _signalComplex[0], _signalComplex[1])
            print 'PMU Signal ', self.iocsv.get_senyal(_component).__str__()

    def load_sourcesH5(self, _sourceH5, _model, _component):
        ''' 
        _sourceH5: .h5 file, i.e. './res/PMUdata_Bus1VA2VALoad9PQ.h5'
        _model: name of the model , for retrieving the h5.group
        _component: name of the component, for retrieving the h5.dataset
        '''
        if (_sourceH5 != ''):
            self.ioh5= InputH5Stream(_sourceH5)
            self.ioh5.open_h5()
            self.ioh5.load_h5(_model, _component)
            print 'Simulation Signal ', self.ioh5.get_senyal(_component).__str__()
        
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
    
    def method_ME(self, _measSignal, _simSignal, _order):
        ''' TODO: create a subset of signals from original signal in object senyal
        call mode estimation method with each subset, inside a loop '''
        meEngine= ModeEstimation()
        meEngine.set_order(_order)
        ''' 1) mode Estimation with PMU signal '''
        if _measSignal!= None:
            meEngine.modeEstimationMat('C:/Users/fragom/PhD_CIM/PYTHON/ScriptMAE/lib/mes.jar',_measSignal)
#             meEngine.modeEstimationPY(_measSignal)
        ''' 2) mode Estimation with simulation signal '''
        if _simSignal!= None:
#             meEngine.modeEstimationMat(_simSignal)
            meEngine.modeEstimationPY(_measSignal)
        ''' TODO: pass the whole signal to Vedran mode estimation '''
        print 'Model Frequency ', meEngine.get_modeFrequency()
        print 'Model Damping  ', meEngine.get_modeDamping()
        
    def method_ERA(self, _measSignal, _simSignal):
        '''
        _measSignal as output
        _simSignal as input
        '''
        '''TODO: match sampletime from meas with sim '''
#         if (_measSignal.get_sampleTime()!= _simSignal.get_sampleTime()):
        timeSignal= _measSignal.get_sampleTime()
        if _measSignal!= None and _simSignal!= None:
            outSignal= _measSignal.get_signalMag()
            inSignal= _simSignal.get_signalReal()
        else:
            if _measSignal!= None:
                outSignal= _measSignal.get_signalMag()
                inSignal= _measSignal.get_signalMag()
            if _simSignal!= None:
                outSignal= _simSignal.get_signalReal()
                inSignal= _simSignal.get_signalReal()
        num_states = 2
#         a,b,c = mr.compute_ERA_model([timeSignal,outSignal,inSignal], num_states)
        a,b,c = mr.compute_ERA_model(numpy.array(outSignal[0:1000]), num_states)
        print 'Measurements: '
        print 'A= ', a
        print 'B= ', b
        print 'C= ', c
        a,b,c = mr.compute_ERA_model(numpy.array(inSignal), num_states)
        print 'Simulation: '
        print 'A= ', a
        print 'B= ', b
        print 'C= ', c

def main(argv):
    smith= Validation(sys.argv[3])
    ''' TODO: load_sources parameters should come from GUI / manually, when scritping '''
    smith.load_sourcesCSV(sys.argv[1], 'pmu9', ['bus9.v','bus9.anglev'])
    smith.load_sourcesH5(sys.argv[2], 'IEEENetworks2.IEEE_9Bus', 'pmu9')
    [measurement, simulation]= smith.get_sources('pmu9', 'pmu9')
    if (sys.argv[4]== '-me'):
        smith.method_ME(simulation, None, 10)
    if (sys.argv[4]== '-era'):
        smith.method_ERA(measurement, simulation)
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
    
