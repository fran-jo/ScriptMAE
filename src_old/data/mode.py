'''
Created on 26 maj 2015

@author: fragom
'''

class Mode(object):
    '''
    Class to store outputs from Mode estimation function (Vedran)
    '''

    def __init__(self):
        '''
        Constructor
        '''
        '''
        Enam 18-06-2015 add attributes to class for storing mode analysis results
        '''
        self.mode_freq=[]
        self.mode_damp=[]

    def get_mode_freq(self):
        return self.mode_freq


    def get_mode_damp(self):
        return self.mode_damp


    def set_mode_freq(self, value):
        self.mode_freq = value


    def set_mode_damp(self, value):
        self.mode_damp = value


    def del_mode_freq(self):
        del self.mode_freq


    def del_mode_damp(self):
        del self.mode_damp

    mode_freq = property(get_mode_freq, set_mode_freq, del_mode_freq, "mode_freq's docstring")
    mode_damp = property(get_mode_damp, set_mode_damp, del_mode_damp, "mode_damp's docstring")
        
    