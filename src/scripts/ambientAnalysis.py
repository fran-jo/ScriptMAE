'''
Created on 3 aug. 2017

@author: fragom
'''
import os
from methods import MethodAmbientAnalysis

# Analysis Engine Methods
class AmbientAnalysis(object):
    
    __analysisTask= None
    
    def onStart_basicMethod(self):
        '''TODO: selected measurement from modelica outputs '''
        self.__analysisTask = MethodAmbientAnalysis(self.__measurement['magnitude'])
        self.__analysisTask.toolDir= os.getcwd()
        self.__analysisTask.taskFinished.connect(self.onFinish_basicMethod)
        self.__analysisTask.start()
            
    def onFinish_basicMethod(self):
        ''' TODO: show the results on the text area / table '''
        os.chdir(self.__analysisTask.toolDir)
        self.__analysisTask.gather_EigenValues()
        print self.__analysisTask.modes
        ''' TODO: first use the mode_estimation_res.h5 directly '''
        ''' TODO: second, use the whole workflow '''
        
if __name__ == '__main__':
    analysisapi= AmbientAnalysis()
    analysisapi.onStart_basicMethod()
    analysisapi.onFinish_basicMethod()
    