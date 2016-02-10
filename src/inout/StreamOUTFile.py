'''
Created on 10 feb 2016

@author: fragom
'''

import os, sys 
import psspy, dyntools

class StreamOUTFile(object):
    '''
    classdocs
    '''

    chnfobj = None
    
    def __init__(self, params):
        '''
        Constructor
        '''
#        PSSE_PATH= r'C:\\Program Files (x86)\\PTI\\PSSE33\\PSSBIN'
        PSSE_PATH= params[0]
        sys.path.append(PSSE_PATH)
        os.environ['PATH']+= ';'+ PSSE_PATH
        
        self.chnfobj = dyntools.CHNF([params[1]])

class InputOUTStream(StreamOUTFile): 
    '''
    classdocs
    '''
    ch_id= []
    ch_data= []

    def __init__(self, pssebinpath, psseoutfile):
        super(InputOUTStream, self).__init__([pssebinpath, psseoutfile])
        
    def load_outputData(self):
        sh_ttl, self.ch_id, self.ch_data= self.chnfobj.get_data()
        
    def get_channelID(self):
        return self.ch_id
    
    def get_channelData(self, outputname='time'):
        channels = [self.ch_id[index] for index in range(1, len(self.ch_id))]
        index= channels.index(outputname)+ 1
        self.ch_data[index]
        print ch_data['time']
    