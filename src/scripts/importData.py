'''
Created on 22 jan 2016

@author: fragom
'''

import sys, os
from inout import StreamCSVFile, StreamH5File, StreamMATFile, StreamOUTFile

class ImportData(object):
    ''' classdocs '''
    
    def __init__(self):
        pass
    
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
            print "Wrong choice ...!" 
        values= []
        for idx in lindex:  
            idx= int(idx)
            values.append(arrayQualquiera[indexMapping[idx]])
        return values
    
    def csv_to_h5(self, csvFile='.csv', delimiter= ','):
        sourcecsv= StreamCSVFile.InputCSVStream(csvFile, delimiter)
        sourcecsv.load_csvHeader()
#         print sourcecsv.cheader
        measname= self.selectData(sourcecsv.cheader)
        componentname= ':'.join([measname[0].split(':')[0], measname[0].split(':')[1]])
        sourcecsv.load_csvValues(componentname, measname[0], measname[1])
#         print sourcecsv.get_senyal(componentname)
        h5name= csvFile.split('.')[1].split('/')[-1]
        h5name= h5name + '.h5'
        sourceh5= StreamH5File.OutputH5Stream(['./res', h5name], 'meas')
        ''' TODO name of the model to be parametrized '''
        sourceh5.open_h5('WhiteNoiseModel')
        measname.insert(0, 'sampletime')
        sourceh5.set_senyal(componentname, sourcecsv.get_senyal(componentname))
        sourceh5.save_h5Names(componentname, measname)
        sourceh5.save_h5Values(componentname)
        sourceh5.close_h5()
        
    def mat_to_h5(self, matFile='.mat', compiler= 'openmodelica'):
        ''' .mat files resulting from Dymola or OpenModelica simulation 
        use of ModelicaRes library'''
        sourcemat= StreamMATFile.InputMATStream(matFile, compiler)
        sourcemat.load_components()
        componentsName= self.selectData(sourcemat.components, 'Select which component data to import: ')
        sourcemat.load_variables(componentsName)
        componentsSignals= zip(componentsName,sourcemat.variables)
        for component, componentSignal in componentsSignals:
            variablesName= self.selectData(componentSignal, 'Select which signals from components to import (per pairs): ')
            # TODO supose user only select 2 variabler per component, what if selects more?
            sourcemat.load_signals(component, variablesName)
        networkname= matFile.split('.')[1].split('/')[-1]
        h5name= networkname + '.h5'
        sourceh5= StreamH5File.OutputH5Stream(['./res', h5name], compiler)
        sourceh5.open_h5(networkname)
        for component in sourcemat.signalData.keys():
            signalNames= [component+'.V', component+'.angle']
            sourceh5.save_h5Names(component, signalNames)
            sourceh5.save_h5Values(component, sourcemat.signalData[component])
        sourceh5.close_h5()
        
    def out_to_h5(self, binpath= './', outfile= '.out'):
        PSSE_PATH= binpath
        sys.path.append(PSSE_PATH)
        os.environ['PATH']+= ';'+ PSSE_PATH
        
        ''' .out files resulting from psse dynamic simulations '''
        sourceout= StreamOUTFile.InputOUTStream(outfile)
        sourceout.load_outputData()
        selectedOutput= self.selectData(sourceout.ch_id, "Select the data to import, in pairs:")
        sourceout.save_channelID(selectedOutput)
        sourceout.load_channelData()
#         print 'signal: ', sourceout.signals
        networkname= outfile.split('.')[1].split('/')[-1]
        h5name= networkname + '.h5'
        sourceh5= StreamH5File.OutputH5Stream(['./res', h5name], 'psse')
        sourceh5.open_h5(networkname)
        for component in sourceout.signals.keys():
            sourceh5.save_h5Names(component, sourceout.selectedId[component])
            sourceh5.save_h5Values(component, sourceout.signals[component])
        sourceh5.close_h5()

if __name__ == '__main__':  
    theimporter= ImportData()
    options= ['dymola','openmodelica','psse','measurements']
    option= theimporter.selectData(options, 'Select the source of the simulation files to import: ')
    if (option[0]=='dymola'):
        theimporter.mat_to_h5(sys.argv[1], 'dymola') 
    if (option[0]=='openmodelica'):
        theimporter.mat_to_h5(sys.argv[1], 'openmodelica')
    if (option[0]=='psse'):
        theimporter.out_to_h5(sys.argv[1], sys.argv[2])
    if (option[0]=='measurements'):
        theimporter.csv_to_h5(sys.argv[1],sys.argv[2])