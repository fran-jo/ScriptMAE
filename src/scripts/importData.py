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
    
    def csv_to_h5(self, csvFile='.csv', delimiter= ','):
        sourcecsv= StreamCSVFile.InputCSVStream(csvFile, delimiter)
        sourcecsv.load_csvHeader()
        print sourcecsv.cheader
        measname= self.selectData(sourcecsv.cheader)
        componentname= measname[0].split('.')[0]
        sourcecsv.load_csvValues(componentname, measname[0], measname[1])
#         print sourcecsv.get_senyal(componentname)
        h5name= csvFile.split('.')[1].split('/')[-1]
        print h5name
        h5name= h5name + '.h5'
        sourceh5= StreamH5File.OutputH5Stream(['./res', h5name], 'omc')
        ''' TODO name of the model to be parametrized '''
        sourceh5.open_h5('WhiteNoiseModel')
        measname.insert(0, 'sampletime')
        sourceh5.set_senyal(componentname, sourcecsv.get_senyal(componentname))
        sourceh5.save_h5Names(componentname, measname)
        sourceh5.save_h5Values(componentname)
        sourceh5.close_h5()
        
    def mat_to_h5(self, matFile='.mat'):
        ''' .mat files resulting from Dymola or OpenModelica simulation 
        use of ModelicaRes library'''
        sourcemat= StreamMATFile.InputMATStream(matFile, 'omc')
        sourcemat.load_components()
        #TODO Selection of variables, recursive
        componentsName= self.selectData(sourcemat.components)
        variablesName= self.selectData(componentsName)
        sourcemat.load_signals(componentsName, variablesName)
        # TODO save signals to h5 file
        h5name= matFile.split('.')[1].split('/')[-1]
        print h5name
        h5name= h5name + '.h5'
        sourceh5= StreamH5File.OutputH5Stream(['./res', h5name], 'omc')
        ''' TODO name of the model to be parametrized '''
        sourceh5.open_h5('WhiteNoiseModel')
        componentsName.insert(0, 'sampletime')
        sourceh5.set_senyal(componentsName, sourcemat.get_senyal(componentsName))
        sourceh5.save_h5Names(componentsName, variablesName)
        sourceh5.save_h5Values(componentsName)
        sourceh5.close_h5()
        
    def out_to_h5(self, binpath= './', outfile= '.out'):
        PSSE_PATH= binpath
        sys.path.append(PSSE_PATH)
        os.environ['PATH']+= ';'+ PSSE_PATH
        
        ''' .out files resulting from psse dynamic simulations '''
        sourceout= StreamOUTFile.InputOUTStream(outfile)
        sourceout.load_outputData()
        selectedOutput= self.selectData(sourceout.ch_id, "Select the data in pairs:")
        sourceout.save_channelID(selectedOutput)
        sourceout.load_channelData()
        print 'signal: ', sourceout.signals
        modelname= outfile.split('.')[1].split('/')[-1]
        print 'modelname: ', modelname
        h5name= modelname + '.h5'
        sourceh5= StreamH5File.OutputH5Stream(['./res', h5name], 'psse')
        ''' TODO name of the model to be parametrized '''
        ''' TODO check the h5Names and values '''
        sourceh5.open_h5(modelname)
        for component in sourceout.signals.keys():
            sourceh5.save_h5Names(component, sourceout.selectedId[component])
            sourceh5.save_h5Values(component, sourceout.signals[component])
        sourceh5.close_h5()

if __name__ == '__main__':  
    theimporter= ImportData()
    options= ['dymola','openmodelica','psse','measurements']
    option= theimporter.selectData(options)
    print option
    if (option[0]=='dymola') | (option[0]=='openmodelica'):
        theimporter.mat_to_h5(sys.argv[1])
    if (option[0]=='psse'):
        theimporter.out_to_h5(sys.argv[1], sys.argv[2])
    if (option[0]=='measurements'):
        theimporter.csv_to_h5(sys.argv[1],sys.argv[2])