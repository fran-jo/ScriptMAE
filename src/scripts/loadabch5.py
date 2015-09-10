'''
Created on 4 jun 2015

@author: fragom
'''
import sys
import h5py as h5

def loadabch5(argv):
    pass
    # Get the signal (r,i or m,p) from .h5 file
#     h5pmu= PhasorMeasH5.PhasorMeasH5(sys.argv[1:])
#     h5pmu.open_h5()
#     
#     print h5pmu.load_h5()
    
#     h5pmu.load_h5('pwLine4', 'V')
#     # result: 2 vectors per variable, work with pwLine4.n.vr, pwLine4.n.vi
#     senyal= h5pmu.get_senyal()
#     print 'mehequedaocontucara', senyal.signalCmp
    
if __name__ == '__main__':
#     loadabch5(sys.argv[1:])
    ch5file= h5.File('./res/PMUdata_Bus1VA2VALoad9PQ.h5', 'r')
    grup= ch5file['df']
    print grup.keys()
    datanames= grup['block0_items']
    datavalues= grup['block0_values']
    idx= 0
    for item in datanames:
        print item, idx
#         print data
#         print len(datanames)
        if (item == 'bus9.v'):
            print datavalues[:,idx]
            print datavalues[:,idx+ 1]
        
        idx+= 1