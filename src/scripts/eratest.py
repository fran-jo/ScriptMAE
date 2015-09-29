'''
Created on Jul 30, 2015

@author: ekj05
'''
import numpy as N
import modred as MR
'''----num_vecs------------------------------column number'''
num_vecs = 4
'''test case---------------------generating arbitrary data'''
vecs = N.random.random((10, num_vecs))
print vecs
'''what is eigenvalues?'''
a,b,c =MR.compute_ERA_model(vecs,4)
print 'printing a matrix'
print a
print 'printing b matrix'
print b
print 'printing c matrix'
print c


# """ opening the h5 file """
#         #File1=h5py.File('Simu.h5','r')
#         ''' using solution from load_pandaSource '''
# #         h5Data= h5py.File(_sourceH5,'r')
#         senyal = self.ioh5.get_senyal('block0')
#         ''' format of the signal (sampletime, real/magnintude, imag/polar) '''
#         """ getting the data set from the h5 file """     
#         #d1=File1[u'subgroup']
# #         d1= h5Data[u'df']
#         """ selecting the vector or array from the h5 file """
#         #d2=d1['highVoltage']
# #         d2=d1['block0_values']
# #         d3=d2[:,1]
#         #print d3[0:100]
#         a,b,c =MR.compute_ERA_model(d3[0:5000],3)
# #         while ()
# #             a,b,c =MR.compute_ERA_model(d3[0:_winSamples],3)
#         """a,b,c =MR.compute_ERA_model(array,5) here 2 is the matrix size of A, B, C  """
#           
#         print 'printing a matrix'
#         #print 'printing matrix a with dimensation ', a.shape
#         print a
#         print 'printing b matrix'
#        
#         print b
#         print 'printing c matrix'
#         print c
#         """ creating the file to write the ERA results """
#         File2 = h5py.File('noisesignal.h5','w')# 
#           
#           
#         dset3 = File2.create_dataset("ERA_A", data=a)
#         dset4 = File2.create_dataset("ERA_B", data=b)
#         dset5 = File2.create_dataset("ERA_C", data=c) 