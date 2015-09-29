'''
Created on Sep 24, 2015

@author: fran_jo
'''

import numpy as np
import modred as mr

class ERAMethod(object):
    '''
    System Identification Technique: Eigensystem Realization Algorithm
    ERA takes a series of Markov parameters (defined by (16)) and from them 
    produces a reduced-order input-output model 
    '''

    lambdau= []
    num_vecs= 0
    
    def __init__(self, params):
        '''
        Constructor
        '''
    
    def get_lambda(self):
        return self.lambdau
    
    def eraMethodPY(self, _signal):
        self.num_vecs = 4
        
        '''what is eigenvalues?'''
        a,b,c = mr.compute_ERA_model(_signal, self.num_vecs)
        print 'printing a matrix'
        print a
        print 'printing b matrix'
        print b
        print 'printing c matrix'
        print c
        """ creating the file to write the ERA results """
        File2 = h5py.File('noisesignal.h5','w')# 
        dset3 = File2.create_dataset("ERA_A", data=a)
        dset4 = File2.create_dataset("ERA_B", data=b)
        dset5 = File2.create_dataset("ERA_C", data=c) 
