'''
Created on Jun 18, 2015
This script test the use of the mode estimate function inside python environment

@author: ekj05
'''
import numpy as np
import data.mode as m
import win32com.client
if __name__ == '__main__':
    h = win32com.client.Dispatch('matlab.application')
    #h.Execute("load LinearSystem64")
    h.Execute("data2 = h5read('pandas5.h5','/df/block0_values');")
    h.Execute("order=18;")
    h.Execute("y=data2(1,:)")
    h.Execute("j=y.'")
    h.Execute("[mode_freq, mode_damp]=mode_est_basic_fcn(j, order);")
    a=h.Execute("disp([mode_freq  mode_damp])")
   # a=h.Execute("runh5")
    
#     h.Execute("dt=0.02;")
#     h.Execute("t=(0:Len-1)*dt;")
#     h.Execute("order=18;")
#     h.Execute("k=203+48;")
#     h.Execute("sys=ss(A,B,C(k,:),D(k,:));")
#     h.Execute("u=randn(Len,size(B,2));")
#     h.Execute("y=lsim(sys,u,t);")
    '''
    call the array from h5 (test one single array i.e voltage)
    '''
   
#     h.Execute("[mode_freq, mode_damp]=mode_est_basic_fcn(Y, order);")
#     
    #a=h.Execute("disp ' Printing in output console freq'")
#     b=h.Execute("disp(mode_freq(1,1))")
#     a1=h.Execute("disp ' Printing in output console damp'")
#     c=h.Execute("disp([mode_damp])")
    '''
    
    '''
    
    print a
    #xx=np.array(b)
#     print b
#      
#     #print b
#     print a1
#     print c
#     
    
    
  
    
    #pass
    
    ''' csvpmu= PhasorMeasCSV.PhasorMeasCSV(sys.argv[1],',') '''
#     1) load data from .csv or .h5 (format of the data? engineering value? p.u.?
#     2) if necessary, process data from sources to the format for the mode estimate functions
#     3) call the mode estimate function
#     4) store outputs from mode estimate functions into Mode class
#     5) print results
    
