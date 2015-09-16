'''
Created on 7 apr 2015

@author: fragom
'''
import sys
from classes import PhasorMeasH5

def abc2phasor(argv):
    # Get the signal (a, b, c) from .mat file
    '''input of the function:
    result file, .mat, either from DY or OMC 
    folder, where to store data h5'''
#     if os.name== 'posix':
#         print platform.system()
    ''' Load simulation results from .mat file '''
    h5pmu= PhasorMeasH5.PhasorMeasH5(sys.argv[1:])
    # calculate phasor from signal
    h5pmu.set_senyalRect("pwLine4.n.vr","pwLine4.n.vi")
    h5pmu.set_senyalPolar("pwLine4.n.vr","pwLine4.n.vi")
    
    h5pmu.get_senyal().set_ccomponent("pwLine4.n")
    h5pmu.calc_phasorSignal()
    # save meas to h5 file   
    h5pmu.create_h5('pwLine4')
    h5pmu.save_h5('V')
    
if __name__ == '__main__':
    abc2phasor(sys.argv[1:])