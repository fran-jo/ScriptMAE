'''
Created on 22 jan 2016

@author: fragom
'''

import sys
from inout import StreamCSVFile, StreamH5File, StreamMATFile

class ImportData(object):
    ''' classdocs '''
    
    def __init__(self):
        pass
    
    def selectData(self, arrayQualquiera):
        count= 0
        indexMapping={}
        for i, meas in enumerate(arrayQualquiera):
            print '[%d] %s' % (i, meas)
            indexMapping[count]= i
            count+= 1
        try:
            value= raw_input("Select which variable do you want to plot: ")
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
        sourceh5= StreamH5File.OutputH5Stream(['./res', h5name], 'openmodelica')
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
        sourceh5= StreamH5File.OutputH5Stream(['./res', h5name], 'openmodelica')
        ''' TODO name of the model to be parametrized '''
        sourceh5.open_h5('WhiteNoiseModel')
        componentsName.insert(0, 'sampletime')
        sourceh5.set_senyal(componentsName, sourcemat.get_senyal(componentsName))
        sourceh5.save_h5Names(componentsName, variablesName)
        sourceh5.save_h5Values(componentsName)
        sourceh5.close_h5()
        
    def out_to_h5(self, outfile= '.out'):
        
        
        outlst = [argv[0]]
        chnfobj = dyntools.CHNF(outlst)
        print '\n Testing call to get_id'
        
        
        print '\n Testing call to get_range'
        ch_range = chnfobj.get_range()
        print ch_range
        
        print '\n Testing call to get_scale'
        ch_scale = chnfobj.get_scale()
        print ch_scale
        
        print '\n Testing call to print_scale'
        chnfobj.print_scale()
        
        print '\n Testing call to txtout'
        chnfobj.txtout(channels=[1,4])
        
        print '\n Testing call to xlsout'
        chnfobj.xlsout(channels=[1,2,3,4,5])

if __name__ == '__main__':
    theimporter= ImportData()
    theimporter.mat_to_h5(sys.argv[1])