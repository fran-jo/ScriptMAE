'''
Created on 28 jan 2016

@author: fragom
'''

from modelicares import SimRes
from data import signal

class StreamMATFile(object):
    '''
    classdocs
    '''
    _resultFile= None
    _compiler= ''
    
    def __init__(self, params):
        '''
        Constructor
        '''
        self._resultFile= SimRes(params[0])
        print self._resultFile
        self._compiler= params[1]
    
class InputMATStream(StreamMATFile):
    '''
    classdocs
    '''
    __components= []
    __variables= []
    __signalData= {}
    
    def __init__(self, matfile, compiler= 'omc'):
        super(InputMATStream,self).__init__([matfile, compiler])
        
    def get_signalData(self):
        return self.__signalData

    def set_signalData(self, value):
        self.__signalData = value

    def del_signalData(self):
        del self.__signalData


    def get_variables(self):
        return self.__variables

    def set_variables(self, value):
        self.__variables = value

    def del_variables(self):
        del self.__variables


    def get_components(self):
        return self.__components

    def set_components(self, value):
        self.__components = value

    def del_components(self):
        del self.__components
        
        
    def load_components(self):
        ''' from the object file, loads the name of the components of the network '''
        self.__components= sorted(self._resultFile.nametree().keys())
    
    def load_variables(self, componentes):
        '''
        components
        '''
        #TODO improve the importer to show variable names
        for component in componentes:
            self.__variables.append(self._resultFile.nametree()[component].keys())
        
    def load_signals(self, component, variable):
        '''
        component
        variables
        '''
        if self._compiler== 'omc': 
            nameVarTime= 'time' 
        else: 
            nameVarTime= "Time"
        senyal= signal.Signal()
        firstSignal= component+ '.'+ variable[0]
        secondSignal= component+ '.'+ variable[1]
        senyal.set_signal(self._resultFile[nameVarTime], self._resultFile[firstSignal], 
                          self._resultFile[secondSignal])
        self.__signalData[component]= senyal
            
        print self.__signalData
            
    components = property(get_components, set_components, del_components, "components's docstring")
    variables = property(get_variables, set_variables, del_variables, "variables's docstring")
    signalData = property(get_signalData, set_signalData, del_signalData, "signalData's docstring")