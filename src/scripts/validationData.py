'''
Created on Sep 03, 2015

@author: ekj05
'''
import sys, os
from methods.ModeEstimation import ModeEstimation
from methods.ValidationERA import ValidationERA 
from methods.ValidationQA import StatisticalAnalysis
from inout.StreamCSVFile import InputCSVStream
from inout.StreamH5File import InputH5Stream
from inout.StreamOUTFile import InputOUTStream
import pandas as pd
import numpy
import matplotlib.pyplot as mplot 
from __builtin__ import None


class ValidationData():
    ''' class for validation, things to do
    TODO: pass the data read to the era method (both simulation and measurement)
    TODO: save the result in the same .h5 file of the simulation
    '''
    simulationSignal= []
    referenceSignal= []
    
    def __init__(self):
        ''' 
        Loading output variables of the model, their values will be stored in h5 and plotted
        '''
        PSSE_PATH= r'C:\\Program Files (x86)\\PTI\\PSSE33\\PSSBIN'
        sys.path.append(PSSE_PATH)
        os.environ['PATH']+= ';'+ PSSE_PATH
        
    def selectData(self, arrayQualquiera, mensaje):
        count= 0
        indexMapping={}
        for i, meas in enumerate(arrayQualquiera):
            print '[%d] %s' % (i, meas)
            indexMapping[count]= i
            count+= 1
        try:
            value= raw_input(mensaje)
            lindex = value.split()
        except ValueError:
            print "Mal! Mal! Mal! Verdadera mal! Por no decir borchenoso!" 
        values= []
        for idx in lindex:  
            idx= int(idx)
            values.append(arrayQualquiera[indexMapping[idx]])
        return values
    
    def load_sourcesCSV(self, sourceCSV):
        ''' 
        sourceCSV: .csv file, i.e. ./res/File_8.csv
        component: name of the component, for retrieving the h5.dataset
        signalComplex: array with pair name of signals [meas, angle] that refer to a complex signal
        '''
        iocsv= InputCSVStream(sourceCSV, ',')
        # TODO user must select which signal to load
#         select the signals according to variables
#         name is the representation of the measurement 
#         meas signals/variables that name the signal of a measurement
#         i.e: name KTHLAB:EMLAB; meas KTHLAB:EMLAB:Magnitude,KTHLAB:EMLAB:Angle 
#         i.e: name bus1.V; meas bus1.v,bus1.angle
        iocsv.load_csvValues(component, signalComplex[0], signalComplex[1])
        print 'Simulation Signal ', iocsv.get_senyal(component).__str__()
        self.referenceSignal= iocsv.get_senyal(component).__str__()  
            
    def load_sourcesOUT(self, sourceOUT):
        sourceout= InputOUTStream(sourceOUT)
        sourceout.load_outputData()
        selectedOutput= self.selectData(sourceout.ch_id, "Select the data in pairs:")
        sourceout.save_channelID(selectedOutput)
        sourceout.load_channelData()
        component= sourceout.signals.keys()
        self.referenceSignal= sourceout.signals[component[0]]
        
    def load_sourcesH5(self, sourceH5, isReference=False):
        ''' 
        sourceH5: .h5 file, i.e. './res/PMUdata_Bus1VA2VALoad9PQ.h5'
        _model: name of the model , for retrieving the h5.group
        _component: name of the component, for retrieving the h5.dataset
        '''
        ioh5= InputH5Stream(sourceH5)
        ioh5.open_h5()
        # TODO user must select which signal to load
        # TODO load model name (header of the h5 file)
        # TODO load component name (will load, sampletime, mag and angle, object signal)
        self.ioh5.load_h5(model, component)
        if (isReference):
            print 'Simulation Signal ', ioh5.get_senyal(component).__str__()
            self.referenceSignal= ioh5.get_senyal(component).get_signalReal()
        else:
            print 'Simulation Signal ', ioh5.get_senyal(component).__str__()
            self.simulationSignal= ioh5.get_senyal(component).get_signalReal()
        
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

    
    def analyze_ME(self):
        ''' TODO: create a subset of signals from original signal in object senyal
        call mode estimation method with each subset, inside a loop '''
        meEngine= ModeEstimation()
        value= raw_input("Order to apply: ")
        meEngine.set_order(value)
        ''' 1) mode Estimation with PMU signal '''
        if self.referenceSignal!= None:
            # TODO fix this method with new implementation of me
            meEngine.modeEstimationMat('C:/Users/fragom/PhD_CIM/PYTHON/ScriptMAE/lib/mes.jar', self.referenceSignal)
        ''' 2) mode Estimation with simulation signal '''
        if self.simulationSignal!= None:
            # TODO study the behavior of this implementation
            print len(self.simulationSignal)
            meEngine.modeEstimationPY(self.simulationSignal)
        ''' TODO: pass the whole signal to Vedran mode estimation '''
#         print 'Model Frequency ', meEngine.get_modeFrequency()
#         print 'Model Damping  ', meEngine.get_modeDamping()
        
    def analyze_ERA(self):
        '''
        _measSignal as output
        _simSignal as input
        '''
        self.engineERA= ValidationERA([])
        '''TODO: match sampletime from meas with sim '''
        self.engineERA.calculate_eigenvalues(numpy.array(self.referenceSignal))
        print 'Measurements: '
        print 'A= ', self.engineERA.A
        print 'B= ', self.engineERA.B
        print 'C= ', self.engineERA.C
        self.engineERA.calculate_eigenvalues(numpy.array(self.simulationSignal))
        print 'Simulation: '
        print 'A= ', self.engineERA.A
        print 'B= ', self.engineERA.B
        print 'C= ', self.engineERA.C

    def plot_outputERA(self):
        mplot.scatter(self.engineERA.eigenValue.real,self.engineERA.eigenValue.imag)
        limit_x= 1.1 # set limits for axis
        limit_y= 0.5 # set limits for axis
#         limit=np.max(np.ceil(np.absolute(self.engineERA.elambda))) # set limits for axis
        mplot.axis([-limit_x, limit_x, -limit_y, limit_y])
        mplot.title('Eigenvalues')
        mplot.ylabel('Imaginary')
        mplot.xlabel('Real')
        mplot.grid(True)
        mplot.show()

    def analyze_RMSE(self):
        # TODO adapt to scriptmae 
        qa= StatisticalAnalysis([self.simulationSignal, self.referenceSignal])
        # analysis results to report 
        arrayRMSE= qa.qaRMSE()
        self.lst_report.addItem("MSE= "+ str(arrayRMSE[0]))
        self.lst_report.addItem("RMSE= "+ str(arrayRMSE[1]))
        # analysis results to plot  
        signalError= qa.qaSignalError()
        mplot.plot(self.csvtree.sampleTime, signalError, 'r-')
        mplot.title('Error')
        mplot.ylabel('Time (s)')
        mplot.xlabel('Value')
        mplot.grid(True)
        mplot.show()
        
        
def main(argv):
    smith= ValidationData()
    # Selection of signals/variables to be analyzed
    options= ['dymola','openmodelica','psse','measurements']
    option= smith.selectData(options, "Select the source of the reference model: ")
    # TODO factory patern to select the proper method
    if (option[0]=='dymola') | (option[0]=='openmodelica'):
        smith.load_sourcesH5(sys.argv[1])
    if (option[0]=='psse'):
        smith.load_sourcesOUT(sys.argv[1])
    if (option[0]=='measurements'):
        smith.load_sourcesCSV(sys.argv[1])
    smith.load_sourcesH5(sys.argv[2])
    
    # Selection of validation/analysis method
    options= ['Mode Estimation','ERA','RMSE']
    option= smith.selectData(options, "Select the validation method: ")
    # TODO factory pattern for applying validation
    # smith.create_method(option)
    # smith.analyze()
    # smith.plot()
    if (option== 'Mode Estimation'):
        smith.analyze_ME()
    if (option== 'ERA'):
        smith.analyze_ERA()
        smith.plot_outputERA()
    if (option== 'RMSE'):
        smith.analyze_RMSE()

if __name__ == '__main__':
    main(sys.argv[1:])
    
