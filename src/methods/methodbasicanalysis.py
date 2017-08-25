'''
Created on 3 aug. 2017

@author: fragom
'''
import os, platform
from subprocess import Popen
from PyQt4 import QtCore
from inout.streammodeh5 import StreamModeH5

class MethodAmbientAnalysis(QtCore.QThread):
    taskFinished = QtCore.pyqtSignal()
    
    __simulationsSignal= []
    __measurementSignal= []
    __order= 0
    __toolDir= ''
    __simulationModes= []
    __measurementModes= []
    
    def __init__(self, simulationSignal, measurementSignal, order= 4, parent= None):
        QtCore.QThread.__init__(self, parent)
        self.__simulationsSignal= simulationSignal
        self.__measurementSignal= measurementSignal
        self.__order= order
       
    @property
    def simulationModes(self):
        return self.__simulationModes
    @property
    def measurementModes(self):
        return self.__measurementModes
    
    @property
    def order(self):
        return self.__order
    @order.setter
    def order(self, value):
        self.__order= value
        
    @property
    def toolDir(self):
        return self.__toolDir
    @toolDir.setter
    def toolDir(self, value):
        self.__toolDir= value 
     
    def run(self):
        self.__ambientModeAnalysis()
        print 'Ambient Mode Analysis'
        if platform.system()== "Darwin":
            matlab= ['/Applications/MATLAB_R2016b.app/bin']
        else: 
            matlab= ['matlab']
        options = ['-nosplash', '-wait', '-r']
        command = ["run_mode_estimation"]
        p = Popen(matlab + options + command)
        stdout, stderr = p.communicate()
        self.taskFinished.emit()  

    def __ambientModeAnalysis(self):
        os.chdir('./res/matlab')
        scriptme= []
        ''' modify the script with the data to be processed '''
        ''' h5file and dataset '''
        scriptme.append("clc; close all; clear;\n")
#         scriptme.append("data= h5read('"+ str(self.h5simoutput)+ "', '"+  str(self.groupName)+ "/"+ str(self.datasetName)+"');\n")
        scriptme.append("simusignal= ["+ " ".join(str(value) for value in self.__simulationsSignal)+ "];\n")
        scriptme.append("simuY= simusignal.';\n")
        scriptme.append("meassignal= ["+ " ".join(str(value) for value in self.__measurementSignal)+ "];\n")
        scriptme.append("measY= meassignal.';\n")
        scriptme.append("order= "+ str(self.__order)+ ";\n")
        scriptme.append("[mode_freq, mode_damp]= mode_est_basic_fcn(simuY, order);\n")
        scriptme.append("hdf5write('mode_estimation_res.h5','/mode_estimation_res/signalfreq', mode_freq,'/mode_estimation_res/signaldamp', mode_damp, '/mode_estimation_res/signal', simuY);\n")
        scriptme.append("[mode_freq, mode_damp]= mode_est_basic_fcn(measY, order);\n")
        scriptme.append("hdf5write('mode_estimation_res.h5','/mode_estimation_res/measurementfreq', mode_freq,'/mode_estimation_res/measurementdamp', mode_damp, '/mode_estimation_res/measurement', measY,'WriteMode','append');\n")
        scriptme.append("exit\n")
        filefile = open('./run_mode_estimation.m', 'w')
        filefile.writelines(scriptme)
        
    def gather_EigenValues(self):
        dbmode= StreamModeH5('./res/matlab', 'mode_estimation_res.h5')
        dbmode.open()
        self.__simulationModes= dbmode.select_modes('simulation')
        self.__measurementModes= dbmode.select_modes('measurement')
        dbmode.close()
