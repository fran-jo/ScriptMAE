'''
Created on 4 jun 2015

@author: fragom
'''
import sys
from classes import PhasorMeasH5
from data import signal

def loadabch5(argv):
    # Get the signal (r,i or m,p) from .h5 file
    h5pmu= PhasorMeasH5.PhasorMeasH5(sys.argv[1:])
    h5pmu.open_h5()
    
    print h5pmu.load_h5()
    
#     h5pmu.load_h5('pwLine4', 'V')
#     # result: 2 vectors per variable, work with pwLine4.n.vr, pwLine4.n.vi
#     senyal= h5pmu.get_senyal()
#     print 'mehequedaocontucara', senyal.signalCmp
    
if __name__ == '__main__':
    loadabch5(sys.argv[1:])