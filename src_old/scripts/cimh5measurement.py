'''
Created on Jul 20, 2017

@author: fran_jo
'''
import sys, os
from methods.ModeEstimation import ModeEstimation
from methods.eigenvalueAnalysis import EigenvalueAnalysis 
from methods.statisticAnalysis import StatisticAnalysis
from inout.StreamCSVFile import InputCSVStream
from inout.StreamH5File import InputH5Stream, OutputH5Stream
from inout.StreamOUTFile import InputOUTStream
# import pandas as pd
import numpy as np
import matplotlib.pyplot as mplot


class AnalogMeasurement(object):
    ''' class for validation, things to do
    TODO: save the result variables, from .mat file, into h5
    TODO: API for CIM database in H5
    '''
    
    def __init__(self):
        ''' 
        PowerSystemResource 1..N Analog
        Analog 1..N AnalogValue
        saveAnalogValue(array)
        main group, name of the resource
        secondary group, analog (name of variable)
        dataset, analogvalue, value of the variable
        '''
        
        ''' if group does not exist - add group, component name '''
        ''' add group (variable), group attributes '''
        ''' add dataset (analogValue), dataset table '''
        
        ''' if group does exist - update group '''
        ''' update group (variable), group attributes '''
        ''' update dataset (analogValue), dataset table '''
        
def main(argv):
    pass

if __name__ == '__main__':
    main()
    
