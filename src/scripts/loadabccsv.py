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
    
    #     tiempos= [datetime.strptime(x,"%Y/%m/%d %H:%M:%S.%f") for x in self.csignal[_variable]]
#         timeZero= time.mktime(tiempos[0])
#         timeUno= time.mktime(tiempos[1])
#         print tiempos[0], ',', tiempos[1]
#         print timeZero, ',', timeUno
#         c= tiempos[1] - tiempos[0]
#         c= timeUno - timeZero
#         s= divmod(c.days * 86400 + c.seconds, 60)
#         print c.microseconds
#         print c.microseconds/1000
#         sampletime= [(t- tiempos[0]).microseconds/1000 for t in tiempos]
#         sampletime= []
#         for t in tiempos:
#             milis= (t- tiempos[0]).microseconds/1000
#             sampletime.append(milis)
#         print sampletime
#         return sampletime
       
#         senyal= [(time.mktime(x)- timeZero)*1000 for x in tiempos]
#         print senyal
#         return senyal