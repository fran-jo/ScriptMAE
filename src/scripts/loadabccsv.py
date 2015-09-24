'''
Created on 4 jun 2015

@author: fragom
'''

from classes.StreamCSVFile import InputCSVStream
from datetime import datetime 
import time, os, platform

if __name__ == '__main__':
    
    print 'platform.system() ', platform.system()
    ''' load names from .csv '''
    csvpmu= InputCSVStream('./res/File_8.csv', ',')
#     print csvpmu.load_csvHeader()
    variable= 'KTHLAB:EMLAB:Magnitude'.split(':')[:-1]
    variable = ':'.join(variable)
    csvpmu.load_csvValues(variable,'KTHLAB:EMLAB:Magnitude','KTHLAB:EMLAB:Angle')
#     print csvpmu.get_senyal(variable)
    
#     variable= 'NTNU_PMU:Va:Magnitude'.split(':')[:-1]
#     variable = ':'.join(variable)
#     csvpmu.load_csvValues(variable, 'NTNU_PMU:Va:Magnitude','NTNU_PMU:Va:Angle')
#     print csvpmu.get_senyal(variable)
#     print 'hola'
    ''' select variable, matching variable from model with variable from memory (.csv) '''
#     csvpmu.load_column('KTHLAB:Frequency')
#     print csvpmu.get_signal('KTHLAB:Frequency')
#     print len(csvpmu.get_column('KTHLAB:Frequency'))
#     csvpmu.load_column('Timestamp')
#     csvpmu.get_sampletime('Timestamp')
    
    tiempos= [datetime.strptime(x,"%Y/%m/%d %H:%M:%S.%f") for x in  csvpmu.get_senyal(variable).get_sampleTime()]
#     timeZero= time.mktime(tiempos[0])
#     timeUno= time.mktime(tiempos[1])
#     print tiempos[0], ',', tiempos[1]
#     print timeZero, ',', timeUno
#     c= tiempos[1] - tiempos[0]
#     c= timeUno - timeZero
#     s= divmod(c.days * 86400 + c.seconds, 60)
#     print c.microseconds
#     print c.microseconds/1000
    sampletime= [(t- tiempos[0]).microseconds/1000 for t in tiempos]
#     sampletime= []
#     for t in tiempos:
#         milis= (t- tiempos[0]).microseconds/1000
#         sampletime.append(milis)
    print sampletime
#     return sampletime
    
#     senyal= [(time.mktime(x)- timeZero)*1000 for x in tiempos]
#     print senyal
#     return senyal