'''
Created on 16 okt 2015

@author: fragom
'''

class OutputERA(object):
    '''
    classdocs
    '''

    def __init__(self, params):
        '''
        Constructor
        '''
        self.clambda= []
        self.cdamping= []
        self.cfrequency= []
        
    def get_signalLambda(self):
        return self.clambda
    
    def get_signalDamping(self):
        return self.cdamping
    
    def get_signalFrequency(self):
        return self.cfrequency
    
    
    def calc_signalDamping(self):
        pass
    
    def calc_signalFrequency(self):
        pass