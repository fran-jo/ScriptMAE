'''
Created on Sep 03, 2015

@author: ekj05
'''
import sys
from methods.ModeEstimation import ModeEstimation
from methods.ValidationERA import ValidationERA 
from inout.StreamCSVFile import InputCSVStream
from inout.StreamH5File import InputH5Stream
from inout.OutputModelVar import OutputModelVar
import pandas as pd
import numpy
import matplotlib.pyplot as mplot 


class Validation():
    ''' class for validation, things to do
    TODO: pass the data read to the era method (both simulation and measurement)
    TODO: save the result in the same .h5 file of the simulation
    '''
    def __init__(self, variables):
        ''' Loading output variables of the model, their values will be stored in h5 and plotted
        argv[0]: file with variable names from the model
        '''
        self.outputs= OutputModelVar(variables)
        self.outputs.load_varList()
        print self.outputs.get_varList()
        self.measurements= []
        self.eraEngine= ValidationERA([]) 
        
    def load_sourcesCSV(self, sourceCSV, component, signalComplex):
        ''' 
        sourceCSV: .csv file, i.e. ./res/File_8.csv
        component: name of the component, for retrieving the h5.dataset
        signalComplex: array with pair name of signals [meas, angle] that refer to a complex signal
        '''
        if (sourceCSV != ''):
            self.iocsv= InputCSVStream(sourceCSV, ',')
            ''' select the signals according to variables '''
            ''' name is the representation of the measurement 
            meas signals/variables that name the signal of a measurement
            i.e: name KTHLAB:EMLAB; meas KTHLAB:EMLAB:Magnitude,KTHLAB:EMLAB:Angle 
            i.e: name bus1.V; meas bus1.v,bus1.angle '''
            self.iocsv.load_csvValues(component, signalComplex[0], signalComplex[1])
            print 'PMU Signal ', self.iocsv.get_senyal(component).__str__()

    def load_sourcesH5(self, sourceH5, model, component):
        ''' 
        sourceH5: .h5 file, i.e. './res/PMUdata_Bus1VA2VALoad9PQ.h5'
        _model: name of the model , for retrieving the h5.group
        _component: name of the component, for retrieving the h5.dataset
        '''
        if (sourceH5 != ''):
            self.ioh5= InputH5Stream(sourceH5)
            self.ioh5.open_h5()
            self.ioh5.load_h5(model, component)
            print 'Simulation Signal ', self.ioh5.get_senyal(component).__str__()
        
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

    def get_sources(self, measurement, component):
        ''' _measurement> 'KTHLAB:EMLAB'
        _component> 'block0'
        '''
        return [self.iocsv.get_senyal(measurement), self.ioh5.get_senyal(component)]
    
    def method_ME(self, measSignal, simSignal, order):
        ''' TODO: create a subset of signals from original signal in object senyal
        call mode estimation method with each subset, inside a loop '''
        meEngine= ModeEstimation()
        meEngine.set_order(order)
        ''' 1) mode Estimation with PMU signal '''
        if measSignal!= None:
            # TODO fix this method with new implementation of me
            meEngine.modeEstimationMat('C:/Users/fragom/PhD_CIM/PYTHON/ScriptMAE/lib/mes.jar',measSignal)
        ''' 2) mode Estimation with simulation signal '''
        if simSignal!= None:
            # TODO study the behavior of this implementation
            print len(simSignal.get_signalReal())
            meEngine.modeEstimationPY(simSignal.get_signalReal())
        ''' TODO: pass the whole signal to Vedran mode estimation '''
#         print 'Model Frequency ', meEngine.get_modeFrequency()
#         print 'Model Damping  ', meEngine.get_modeDamping()
        
    def method_ERA(self, _measSignal, _simSignal):
        '''
        _measSignal as output
        _simSignal as input
        '''
        '''TODO: match sampletime from meas with sim '''
#         if (_measSignal.get_sampleTime()!= _simSignal.get_sampleTime()):
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
        self.eraEngine.calculate_eigenvalues(numpy.array(outSignal[0:1000]))
        print 'Measurements: '
        print 'A= ', self.eraEngine.A
        print 'B= ', self.eraEngine.B
        print 'C= ', self.eraEngine.C
        self.eraEngine.calculate_eigenvalues(numpy.array(inSignal))
        print 'Simulation: '
        print 'A= ', self.eraEngine.A
        print 'B= ', self.eraEngine.B
        print 'C= ', self.eraEngine.C

    def plot_outputERA(self):
        mplot.scatter(self.eraEngine.eigenValue.real,self.eraEngine.eigenValue.imag)
        limit_x= 1.1 # set limits for axis
        limit_y= 0.5 # set limits for axis
#         limit=np.max(np.ceil(np.absolute(eraEngine.elambda))) # set limits for axis
        mplot.axis([-limit_x, limit_x, -limit_y, limit_y])
        mplot.title('Eigenvalues')
        mplot.ylabel('Imaginary')
        mplot.xlabel('Real')
        mplot.grid(True)
        mplot.show()

def main(argv):
    smith= Validation(sys.argv[3])
    ''' TODO: load_sources parameters should come from GUI / manually, when scritping '''
    smith.load_sourcesCSV(sys.argv[1], 'pmu1', ['bus1.v','bus1.anglev'])
    smith.load_sourcesH5(sys.argv[2], 'WhiteNoiseModel', 'bus1')
    [measurement, simulation]= smith.get_sources('pmu1', 'bus1')
    if (sys.argv[4]== '-me'):
        smith.method_ME(None, simulation, 26)
    if (sys.argv[4]== '-era'):
        smith.method_ERA(None, simulation)
        smith.plot_outputERA()
    ''' TODO: how to indicate the method to use? input parameter'''

if __name__ == '__main__':
    main(sys.argv[1:])
    
