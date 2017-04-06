'''
Created on Sep 23, 2015

@author: fran_jo
'''

from scipy import signal
import statsmodels.api as smapi
import subprocess, os
# from subprocess import Popen
from quantitativeAnalysis import QuantitativeAnalysis
from inout.StreamH5File import InputH5Stream, OutputH5Stream
# import win32com.client

# from pymatbridge import Matlab

class ModeEstimation(QuantitativeAnalysis):
    '''
    classdocs
    '''
    _h5resultFile= ''
    _h5inputfile= ''
    _matlabpath= ''
    __order= 0
    __signalFrequency= {}
    __signalDamping= {}
    
    def __init__(self, params):
        super(ModeEstimation, self).__init__(params)

    def get_matlabpath(self):
        return self._matlabpath

    def set_matlabpath(self, value):
        self._matlabpath = value

    def del_matlabpath(self):
        del self._matlabpath

    def get_signal_frequency(self):
        return self.__signalFrequency
    
    def get_signal_damping(self):
        return self.__signalDamping

    def set_signal_frequency(self, value):
        self.__signalFrequency = value

    def set_signal_damping(self, value):
        self.__signalDamping = value

    def del_signal_frequency(self):
        del self.__signalFrequency

    def del_signal_damping(self):
        del self.__signalDamping

    def get_order(self):
        return self.__order

    def set_order(self, value):
        self.__order = value

    def del_order(self):
        del self.__order

#         if platform.system()== 'Windows':
#             self.win = __import__('win32com.client')
#             '''Opening MATLAB application'''

    def save_channelH5(self):
        '''
        this function sets the .h5 file containing the data, to be used by the matlab script
        matlabPath where the mode estimation matlab script is
        '''
        channelH5= OutputH5Stream(['./res/matlab', 'mode_estimation_resources.h5'], 'none')
        channelH5.open_h5('signal_data')
        channelH5.save_channelData(self._signalRef)
        channelH5.save_channelData(self._signalOut)
        self._packageName= channelH5.group.name
        channelH5.close_h5()
        self._h5inputfile= str(channelH5.fileName)
    
    def compute_method(self, parametro= None):
        # TODO: check cpu time
#         os.chdir('C:/Users/fragom/PhD_CIM/PYTHON/ScriptMAE/res/matlab')
        os.chdir(self._matlabpath)
        nameDataRef= self._packageName+ '/'+ self._signalRef.get_component()
        nameDataSim= self._packageName+ '/'+ self._signalOut.get_component() 
        scriptme= []
        scriptme.append("clc; close all; clear;\n")
        scriptme.append("dataRef= h5read('"+ str(self._h5inputfile)+ "', '"+
                        str(nameDataRef)+"');\n")
        scriptme.append("do= dataRef(1,:);\n")
        scriptme.append("Y= do.';\n")
        scriptme.append("order= "+ str(self.__order)+ ";\n")
        scriptme.append("[mode_freq_ref, mode_damp_ref]=mode_est_basic_fcn(Y, order);\n")
        scriptme.append("dataSim= h5read('"+ str(self._h5inputfile)+ "', '"+
                        str(nameDataSim)+"');\n")
        scriptme.append("do= dataSim(1,:);\n")
        scriptme.append("Y= do.';\n")
        scriptme.append("[mode_freq_sim, mode_damp_sim]=mode_est_basic_fcn(Y, order);\n")
        #TODO me_reference/damp me_reference/freq, me_simulation/damp me_simulation/freq
        refFreqName= '/'+ str(self._signalRef.get_component())+ '/freq'
        refDampName= '/'+ str(self._signalRef.get_component())+ '/damp'
        simFreqName= '/'+ str(self._signalOut.get_component())+ '/freq'
        simDampName= '/'+ str(self._signalOut.get_component())+ '/damp'
        self._h5resultFile= 'mode_estimation_results.h5'
        scriptme.append("hdf5write('"+self._h5resultFile+ "','"+ 
                        refFreqName+ "', mode_freq_ref,'"+ 
                        refDampName+ "', mode_damp_ref,'")
        scriptme.append(simFreqName+ "', mode_freq_sim,'"+ 
                        simDampName+ "', mode_damp_sim);\n")
        scriptme.append("exit\n")
        filefile = open('./run_mode_estimation.m', 'w') #os.chdir('C:/Users/fragom/PhD_CIM/PYTHON/SimuGUI/res/matlab/') before
        filefile.writelines(scriptme)
        # This lines are for developing under eclipse, to pause the script execution
        subprocess.call("matlab -r run_mode_estimation")
        # This two lines is the correct way of dealing with external program to finish
#         matlab = Popen('matlab -r run_mode_estimation')
#         matlab.communicate('input')
#         print 'matlab.returncode ', matlab.returncode

    def load_channelH5(self):
        resulth5= InputH5Stream([self._matlabpath, self._h5resultFile])
        resulth5.open_h5()
        for group in resulth5.groupList:
            resulth5.load_h5Data(group)
#         dataFreqName= str(resulth5.group.name)+ '/freq'
#         dataDampName= str(resulth5.group.name)+ '/damp'
            self.__signalDamping[group]= resulth5.datasetValues['damp']
            self.__signalFrequency[group]= resulth5.datasetValues['freq']
        print 'self.mode_damp ', self.__signalDamping
        print 'self.mode_freq ', self.__signalFrequency
        resulth5.close_h5()
    
    def modeEstimationPY(self, senyal):
        # TODO Check CPU time
        '''
        low pass filtering for mode estimation function 
        array must be declared and passed through the function 
        '''
        # step 1 vedran, design filter
        ''' Wn= length-2 sequence giving the critical frequencies - Fp, Fst parameters from matlab fdesign.lowpass(Fp,Fst,Ap,Ast)
        rp: maximum ripple in the pass band. (dB) - Ap parameter from matlab fdesign.lowpass(Fp,Fst,Ap,Ast)
        rs:  minimum attenuation in the stop band. (dB) - Ast parameter from matlab fdesign.lowpass(Fp,Fst,Ap,Ast)
        '''
        b, a= signal.iirfilter(self.order, Wn=[2/25,2.5/25], rp=0.1, rs=50, btype='lowpass', 
                               analog=True, ftype='cheby2')
        # step 2 vedran, apply filter
        senalFiltrada= signal.lfilter(b, a, senyal)
        # step 3 vedran, downsample the signal
        senyalsampled = signal.decimate(senalFiltrada, 10, ftype='iir')
        
        # step 4 vedran, armax, _signal.real or signal.magnitude and signal.sampling data
        sys_ident= smapi.tsa.ARMA(senyalsampled, order=(self.order,self.order)).fit()
        print sys_ident
        # sys_ident contains poles of the system and frequency related to this poles (modes), so we can apply 
        # definition of Natural Frequency -> Omega_n= abs(pole) and Damping ratio -> -cos(angle(pole))
        # step I with signal.freqs(b,a,y) we obtain frequency response of the signal
        angularHz, responseHz = signal.freqs(b, a, senyal)
#         print responseHz
        # step II according to matlab, Wn = abs(R)
        print 'angular frequency ', angularHz
        print 'frequency response ', responseHz
        
    
    order = property(get_order, set_order, del_order, "order's docstring")
    signalFrequency = property(get_signal_frequency, set_signal_frequency, del_signal_frequency, "signalFrequency's docstring")
    signalDamping = property(get_signal_damping, set_signal_damping, del_signal_damping, "signalDamping's docstring")
    matlabpath = property(get_matlabpath, set_matlabpath, del_matlabpath, "matlabpath's docstring")
    
    