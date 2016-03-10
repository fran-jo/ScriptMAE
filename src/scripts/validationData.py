'''
Created on Sep 03, 2015

@author: ekj05
'''
import sys, os
from methods.ModeEstimation import ModeEstimation
from methods.ValidationERA import ValidationERA 
from methods.ValidationQA import StatisticalAnalysis
from inout.StreamCSVFile import InputCSVStream
from inout.StreamH5File import InputH5Stream, OutputH5Stream
from inout.StreamOUTFile import InputOUTStream
# import pandas as pd
# import numpy
import matplotlib.pyplot as mplot 


class ValidationData():
    ''' class for validation, things to do
    TODO: save the result in the same .h5 file of the simulation
    '''
    simulationSignal= []
    h5referenceIn= None
    h5referenceOut= None
    referenceSignal= []
    referenceMesurement= {}
    
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
        reads data from .csv and stores desired data into .h5
        '''
        iocsv= InputCSVStream(sourceCSV, ',')
        iocsv.load_csvHeader()
        measurementName= self.selectData(iocsv.header, "Select the signal for validation (per pairs): ")
        componentName= ':'.join(measurementName[0].split(':')[:-1])
        iocsv.load_csvValues(componentName, measurementName[0], measurementName[1])
#         iocsv.timestamp2sample(componentName)
        # TODO subset of signals, this pmu data has 1 milion samples, need to match the simulation 10k or 100k
        self.referenceSignal= iocsv.get_senyal(componentName)
        self.referenceMesurement[componentName]= measurementName
        
    def sourceCSV_to_H5(self, sourceCSV):
        componentName= self.referenceMesurement.keys()[0]
        measurementName= self.referenceMesurement.values()[0]
        h5name= sourceCSV.split('.')[1].split('/')[-1]
        h5name= h5name + '.h5'
        self.h5referenceOut= OutputH5Stream(['./res', h5name], 'meas')
        ''' TODO name of the model to be parametrized '''
        self.h5referenceOut.open_h5(componentName)
#         measurementName.insert(0, 'sampletime')
#         print 'mesurementName ', measurementName
#         sourceh5.set_senyales(componentName, iocsv.get_senyal(componentName))
        self.h5referenceOut.save_h5Names(componentName, measurementName)
        self.h5referenceOut.save_h5Values(componentName,  self.referenceSignal)
        self.h5referenceOut.close_h5()
           
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
        
    def load_sourceMAT(self, sourceMAT, compiler):
        pass
    
    def load_sourcesH5(self, sourceH5, isReference=False):
        ''' 
        sourceH5: .h5 file, i.e. './res/PMUdata_Bus1VA2VALoad9PQ.h5'
        isReference: 
        '''
        # TODO aware of the dir, need to change
        ioh5= InputH5Stream(['C:/Users/fragom/PhD_CIM/PYTHON/ScriptMAE', sourceH5])
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
        ''' TODO: this function works with reference signal and simulation signal '''
        self.meEngine= ModeEstimation()
        self.meEngine.matlabpath= 'C:/Users/fragom/PhD_CIM/PYTHON/ScriptMAE/res/matlab'
        value= raw_input("\nOrder to apply: ")
        self.meEngine.set_order(value)
        self.meEngine.signalRef= self.referenceSignal
        self.meEngine.signalOut= self.simulationSignal
        self.meEngine.save_channelH5()
        self.meEngine.modeEstimation()
        self.meEngine.load_channelH5()
        programPause = raw_input("Press the <ENTER> key to continue...")
#         self.meEngine.load_ModeEstimation('C:/Users/fragom/PhD_CIM/PYTHON/ScriptMAE/res/matlab')
        
    def plot_outputME(self):
        # 1st plot damping
        mplot.figure(1)
        mplot.subplot(211)
        for key, values in self.meEngine.signalDamping.iteritems():
            xdamp= range(len(values))
            mplot.plot(xdamp, values, 'ro')
            for i, txt in enumerate(values):
                mplot.annotate(txt, (xdamp[i], values[i]))
        mplot.title('Signal Damping')
        mplot.ylabel('Values')
        mplot.grid(True)
        mplot.subplot(212)
        for key, values in self.meEngine.signalFrequency.iteritems():
            xfreq= range(len(values))
            mplot.plot(xfreq, values, 'ro')
            for i, txt in enumerate(values):
                mplot.annotate(txt, (xfreq[i], values[i]))
        mplot.title('Signal Frequency')
        mplot.xlabel('Time (s)')
        mplot.ylabel('Values')
        mplot.grid(True)
        mplot.show()
        
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
            smith.sourceCSV_to_H5(sys.argv[1])
            smith.analyze_ME()
            smith.plot_outputME()
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
    
