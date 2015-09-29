'''
Created on 25 sep 2015

@author: fragom
'''
from pymatbridge import Matlab

if __name__ == '__main__':
    mlab= Matlab(matlab='C:/Program Files/MATLAB/R2012b/bin/matlab.exe')
    mlab.start()
    for i in range(10):
        print mlab.run('C:/IDE/python-matlab-bridge/test.m',{'a':i})['result']
    mlab.stop()