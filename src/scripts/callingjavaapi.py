'''
Created on Sep 3, 2015

@author: ekj05
'''
import sys
import numpy as np
from scipy.signal import butter, lfilter, iirfilter
import subprocess

def dnsample(y,order):
    return y[::order];

def transpose_data(y):
    return y[:,None];
    
def length_signal(y):
    return y.shape

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

""" low pass filtering for mode estimation function"""
""" array must be declared and passed through the function"""    
def lowpass_filtering(y):
    b, a = iirfilter(17, Wn=0.1, rp=0.1, rs=50, btype='lowpass', analog=True, ftype='cheby2')
    y=lfilter(b,a,y)
    return y

""" similar like find """
def find_from_sample(y,find_what):
    return np.where(y==find_what)[0];

"""opening java executable jar file from python"""
def executing_jar(name):
    subprocess.call(['java','-jar',name])
    
if __name__ == '__main__':
    executing_jar(sys.argv[1])
