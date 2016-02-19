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
# import pandas as pd
# import numpy
import matplotlib.pyplot as mplot 


class ValidationData():
    ''' class for validation, things to do
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
        print '\n'
        for i, meas in enumerate(arrayQualquiera):
            print '[%d] %s' % (i, meas)
            indexMapping[count]= i
            count+= 1
        try:
            value= raw_input(mensaje)
            lindex = value.split()
        except ValueError:
            print "Wrong choice...!" 
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
        iocsv.load_csvHeader()
        options= self.selectData(iocsv.header, "Select the signal for validation (per pairs): ")
        componentName= options[0].split('.')[0]
        iocsv.load_csvValues(componentName, options[0], options[1])
#         print 'Simulation Signal ', iocsv.get_senyal(componentName).__str__()
        self.referenceSignal= iocsv.get_senyal(componentName)
            
    def load_sourcesOUT(self, sourceOUT):
        '''
        sourceOUT: 
        '''
        sourceout= InputOUTStream(sourceOUT)
        sourceout.load_outputData()
        selectedOutput= self.selectData(sourceout.ch_id, "Select the signal for validation (per pairs):")
        sourceout.save_channelID(selectedOutput)
        sourceout.load_channelData()
        component= sourceout.signals.keys()
        self.referenceSignal= sourceout.signals[component[0]]
        
    def load_sourcesH5(self, sourceH5, isReference=False):
        ''' 
        sourceH5: .h5 file, i.e. './res/PMUdata_Bus1VA2VALoad9PQ.h5'
        compiler: 
        isReference: 
        '''
        ioh5= InputH5Stream(sourceH5)
        ioh5.open_h5()
        ioh5.load_h5Group()
        optcomponent= self.selectData(ioh5.datasetList, "Select the signal to be validated: ")
        componentName= optcomponent[0].split('_')[0]
        ioh5.load_h5(str(ioh5.group.name), componentName)
        if (isReference):
#             print 'Simulation Signal ', ioh5.get_senyal(componentName).__str__()
            self.referenceSignal= ioh5.get_senyal(componentName).get_signalReal()
        else:
#             print 'Simulation Signal ', ioh5.get_senyal(componentName).__str__()
            self.simulationSignal= ioh5.get_senyal(componentName)
        
    
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
        self.engineERA.signalOut= self.simulationSignal.get_signalReal()
        self.engineERA.signalRef= self.referenceSignal.get_signalMag()
        self.engineERA.calculate_eigenvalues()
        print 'From simulation outputs: '
        print 'A= ', self.engineERA.Aout
        print 'B= ', self.engineERA.Bout
        print 'C= ', self.engineERA.Cout
        print 'From reference outputs: '
        print 'A= ', self.engineERA.Aref
        print 'B= ', self.engineERA.Bref
        print 'C= ', self.engineERA.Cref
        
    def plot_outputERA(self):
        for eigenvalue in self.engineERA.eigenValueOut:
            mplot.scatter(eigenvalue.real, eigenvalue.imag)
        for eigenvalue in self.engineERA.eigenValueRef:
            mplot.scatter(eigenvalue.real, eigenvalue.imag)
        limit_x= 1.2 # set limits for axis
        limit_y= 1.2 # set limits for axis
        mplot.axis([-limit_x, limit_x, -limit_y, limit_y])
        mplot.title('Eigenvalues')
        mplot.ylabel('Imaginary')
        mplot.xlabel('Real')
        mplot.grid(True)
        mplot.show()

    def analyze_RMSE(self):
        qa= StatisticalAnalysis()
        qa.signalOut= self.simulationSignal
        qa.signalRef= self.referenceSignal
        # analysis results to report 
        qa.qaResampling()
        arrayRMSE= qa.qaErrorValidation()
        print 'Quantitative Analyisis: Results'
        print "MSE= "+ str(arrayRMSE[0])
        print "RMSE= "+ str(arrayRMSE[1])
        print "MAE= "+ str(arrayRMSE[2])
        print "MAPE= "+ str(qa.qaMAPE())
        # analysis results to plot  
        signalError= qa.qaSignalError()
        mplot.figure(1)
        mplot.subplot(211)
        mplot.plot(self.simulationSignal.get_sampleTime(), self.simulationSignal.get_signalReal())
        mplot.plot(self.referenceSignal.get_sampleTime(), self.referenceSignal.get_signalMag())
        mplot.title('Qualitative Analysis')
        mplot.xlabel('Time (s)')
        mplot.ylabel('Value')
        mplot.grid(True)
        mplot.subplot(212)
        mplot.plot(self.simulationSignal.get_sampleTime(), signalError, 'r-')
        mplot.xlabel('Time (s)')
        mplot.ylabel('Value')
        mplot.grid(True)
        mplot.show()
        
        
def main(argv):
    smith= ValidationData()
    while (True):
    # Selection of signals/variables to be analyzed
        options= ['dymola','openmodelica','psse','measurements']
        option= smith.selectData(options, "Select the source of the reference model: ")
        if (option[0]=='dymola'): 
            smith.load_sourcesH5(sys.argv[1], isReference=True)
        if (option[0]=='openmodelica'):
            smith.load_sourcesH5(sys.argv[1], isReference=True)
        if (option[0]=='psse'):
            smith.load_sourcesOUT(sys.argv[1])
        if (option[0]=='measurements'):
            smith.load_sourcesCSV(sys.argv[1])
        smith.load_sourcesH5(sys.argv[2])
        # Selection of validation/analysis method
        options= ['Mode Estimation','ERA','RMSE']
        option= smith.selectData(options, "Select the validation method: ")
        if (option[0]== 'Mode Estimation'):
            smith.analyze_ME()
        if (option[0]== 'ERA'):
            smith.analyze_ERA()
            smith.plot_outputERA()
        if (option[0]== 'RMSE'):
            smith.analyze_RMSE()
            
        value= raw_input('\n Do you want to continue (y/n)? ')
        if (value=='n'):
            break
        

if __name__ == '__main__':
    PSSE_PATH= r'C:\\Program Files (x86)\\PTI\\PSSE33\\PSSBIN'
    sys.path.append(PSSE_PATH)
    os.environ['PATH']+= ';'+ PSSE_PATH
    main(sys.argv[1:])
    
