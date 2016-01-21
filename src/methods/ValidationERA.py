'''
Created on 20 jan 2016

@author: fragom
'''

import modred as mr
import numpy as np
from scipy import linalg

class ValidationERA(object):
    '''
    classdocs
    '''
    __A= []
    __B= []
    __C= []
    __elambda= []
    __vlambda= []

    def __init__(self, params):
        '''
        Constructor
        '''
        
    def calculate_eigenvalues(self, oneSignal):
        ''' eigenvalues and eigen vectors '''
        print len(oneSignal)
        #first era method
        self.__A, self.__B, self.__C = mr.compute_ERA_model(np.array(oneSignal), 3)
        # second, eigenvalues and eigenvectors
        self.__elambda, self.__vlambda = linalg.eig(self.__A)
#         ''' TODO: this functions shows a warning, catch it and print it in the GUI '''
        

    def get_A(self):
        return self.__A


    def get_B(self):
        return self.__B


    def get_C(self):
        return self.__C


    def get_eigenValues(self):
        return self.__elambda


    def get_eigenVector(self):
        return self.__vlambda


    def set_A(self, value):
        self.__A = value


    def set_B(self, value):
        self.__B = value


    def set_C(self, value):
        self.__C = value


    def set_eigenValues(self, value):
        self.__elambda = value


    def set_eigenVector(self, value):
        self.__vlambda = value


    def del_A(self):
        del self.__A


    def del_B(self):
        del self.__B


    def del_C(self):
        del self.__C


    def del_eigenValues(self):
        del self.__elambda


    def del_eigenVector(self):
        del self.__vlambda
 
        
    A = property(get_A, set_A, del_A, "A's docstring")
    B = property(get_B, set_B, del_B, "B's docstring")
    C = property(get_C, set_C, del_C, "C's docstring")
    eigenValue = property(get_eigenValues, set_eigenValues, del_eigenValues, "elambda's docstring")
    eigenVector = property(get_eigenVector, set_eigenVector, del_eigenVector, "vlambda's docstring")