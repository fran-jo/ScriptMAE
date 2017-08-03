'''
Created on 3 aug. 2017

@author: fragom
'''
import os
from subprocess import Popen
from PyQt4 import QtCore
from inout.streammodeh5 import StreamModeH5

class MethodAmbientAnalysis(QtCore.QThread):
    taskFinished = QtCore.pyqtSignal()
    
    __signal= []
    __order= 0
    __toolDir= ''
    __modes= []
    
    def __init__(self, measurementSignal, order= 4, parent= None):
        QtCore.QThread.__init__(self, parent)
        self.__signal= measurementSignal
        self.__order= order
       
    @property
    def modes(self):
        return self.__modes
    @modes.setter
    def modes(self, value):
        self.__modes= value 
        
    @property
    def toolDir(self):
        return self.__toolDir
    @toolDir.setter
    def toolDir(self, value):
        self.__toolDir= value 
     
    def run(self):
        print 'Ambient Mode Analysis'
        self.__ambientModeAnalysis()
        matlab  = ['matlab']
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
        scriptme.append("do= ["+ " ".join(str(value) for value in self.__signal)+ "];\n")
        scriptme.append("Y= do.';\n")
        scriptme.append("order= "+ str(self.__order)+ ";\n")
        scriptme.append("[mode_freq, mode_damp]=mode_est_basic_fcn(Y, order);\n")
        scriptme.append("hdf5write('mode_estimation_res.h5','/mode_estimation_res/freq', mode_freq,'/mode_estimation_res/damp', mode_damp, '/mode_estimation_res/signal', do);\n")
        scriptme.append("exit\n")
        filefile = open('./run_mode_estimation.m', 'w')
        filefile.writelines(scriptme)
        
    def gather_EigenValues(self):
        dbmode= StreamModeH5('./res/matlab', 'mode_estimation_res.h5')
        dbmode.open()
        self.__modes= dbmode.select_modes()