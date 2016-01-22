'''
Created on 22 jan 2016

@author: fragom
'''

import sys
from inout import StreamCSVFile, StreamH5File

class ImportData(object):
    ''' classdocs '''
    
    def __init__(self):
        pass
    
    def csv_to_h5(self, csvFile='.csv', delimiter= ','):
        sourcecsv= StreamCSVFile.InputCSVStream(csvFile, delimiter)
        sourcecsv.load_csvHeader()
        print sourcecsv.cheader
        count= 0
        indexMapping={}
        for i, meas in enumerate(sourcecsv.cheader):
            print '[%d] %s' % (i, meas)
            indexMapping[count]= i
            count+= 1
        try:
            value= raw_input("Select which variable do you want import: ")
            lindex = value.split()
        except ValueError:
            print "Mal! Mal! Mal! Verdadera mal! Por no decir borchenoso!" 
        measurements= []
        for idx in lindex:  
            idx= int(idx)
            measurements.append(sourcecsv.cheader[indexMapping[idx]])
        componentname= measurements[0].split('.')[0]
        sourcecsv.load_csvValues(componentname, measurements[0], measurements[1])
#         print sourcecsv.get_senyal(componentname)
        h5name= csvFile.split('.')[1].split('/')[-1]
        print h5name
        h5name= h5name + '.h5'
        sourceh5= StreamH5File.OutputH5Stream(['./res', h5name], 'openmodelica')
        ''' TODO name of the model to be parametrized '''
        sourceh5.open_h5('WhiteNoiseModel')
        measurements.insert(0, 'sampletime')
        sourceh5.set_senyal(componentname, sourcecsv.get_senyal(componentname))
        sourceh5.save_h5Names(componentname, measurements)
        sourceh5.save_h5Values(componentname)
        sourceh5.close_h5()
        
    def mat_to_H5(self, matFile='.mat'):
        pass

if __name__ == '__main__':
    theimporter= ImportData()
    theimporter.csv_to_h5(sys.argv[1], sys.argv[2])