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

