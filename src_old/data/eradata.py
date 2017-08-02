'''
Created on 16 okt 2015

@author: fragom
'''

class DataERA(object):
    '''
    classdocs
    '''
    __A= []
    __B= []
    __C= []
    __elambda= []
    __vlambda= []
    
    def __init__(self):
        '''
        Constructor
        '''

    def get_a(self):
        return self.__A

    def get_b(self):
        return self.__B

    def get_c(self):
        return self.__C

    def get_elambda(self):
        return self.__elambda

    def get_vlambda(self):
        return self.__vlambda

    def set_a(self, value):
        self.__A = value

    def set_b(self, value):
        self.__B = value

    def set_c(self, value):
        self.__C = value

    def set_elambda(self, value):
        self.__elambda = value

    def set_vlambda(self, value):
        self.__vlambda = value

    def del_a(self):
        del self.__A

    def del_b(self):
        del self.__B

    def del_c(self):
        del self.__C

    def del_elambda(self):
        del self.__elambda

    def del_vlambda(self):
        del self.__vlambda

    A = property(get_a, set_a, del_a, "A's docstring")
    B = property(get_b, set_b, del_b, "B's docstring")
    C = property(get_c, set_c, del_c, "C's docstring")
    lambdaValues = property(get_elambda, set_elambda, del_elambda, "elambda's docstring")
    lambdaVector = property(get_vlambda, set_vlambda, del_vlambda, "vlambda's docstring")
        
    