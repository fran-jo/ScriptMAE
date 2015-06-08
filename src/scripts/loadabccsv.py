'''
Created on 4 jun 2015

@author: fragom
'''
import sys
from classes import PhasorMeasCSV

if __name__ == '__main__':
    ''' load names from .csv '''
    csvpmu= PhasorMeasCSV.PhasorMeasCSV(sys.argv[1],',')
    csvpmu.load_header()
    
    ''' select variable, matching variable from model with variable from memory (.csv) '''
#     csvpmu.load_column('KTHLAB:Frequency')
#     print csvpmu.get_signal('KTHLAB:Frequency')
#     print len(csvpmu.get_column('KTHLAB:Frequency'))
    csvpmu.load_column('Timestamp')
    csvpmu.get_sampletime('Timestamp')