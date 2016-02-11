'''
Created on 10 feb 2016

@author: fragom
'''

import os, sys 
# import psspy, dyntools
from data import signal

class StreamOUTFile(object):
    '''
    classdocs
    '''

    _chnfobj = None
    
    def __init__(self, params):
        '''
        Constructor
        '''
#        PSSE_PATH= r'C:\\Program Files (x86)\\PTI\\PSSE33\\PSSBIN'
        PSSE_PATH= params[0]
        sys.path.append(PSSE_PATH)
        os.environ['PATH']+= ';'+ PSSE_PATH
        
        self._chnfobj = dyntools.CHNF([params[1]])

class InputOUTStream(StreamOUTFile): 
    '''
    classdocs
    '''
    __outid= []
    __outdata= []
    __signals= {}

    def __init__(self, pssebinpath, psseoutfile):
        super(InputOUTStream, self).__init__([pssebinpath, psseoutfile])

    def get_outid(self):
        return self.__outid

    def set_outid(self, value):
        self.__outid = value

    def del_outid(self):
        del self.__outid


    def get_signals(self):
        return self.__signals

    def set_signals(self, value):
        self.__signals = value

    def del_signals(self):
        del self.__signals
     
       
    def load_outputData(self):
        sh_ttl, self.__outid, self.__outdata= self._chnfobj.get_data()
    
    def load_channelData(self, outputname='time'):
        channels = [self.__outid[index] for index in range(1, len(self.__outid))]
#         print self.__outdata[index]
#         print self.__outdata['time']
        emptyarray= [0 for x in range(0,len(self.__outdata['time']))]
        for out in outputname:
            index= channels.index(out)+ 1
            senyal= signal.Signal()
            senyal.set_signal(self.__outdata['time'], self.__outdata[index], emptyarray)
            self.__signals[out]= senyal
        
    signals = property(get_signals, set_signals, del_signals, "signals's docstring")
    ch_id = property(get_outid, set_outid, del_outid, "ch_id's docstring")
    
    