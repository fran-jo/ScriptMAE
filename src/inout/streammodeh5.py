'''
Created on 7 apr 2015

@author: fragom
'''
import h5py as h5
from data.EigenValue import EigenValue

class StreamModeH5(object):
    '''
    _h5file file object with reference to the .h5 file
    _group object to keep in memory a group from the .h5 file
    cdataset objet to keep in memory the dataset of signals from the .h5 file
    '''
    __h5namefile= ''
    __h5file= None
    __resfolder= ''
    __gResults= None
    __dfreq= None
    __ddamp= None
    
    def __init__(self, respath= '', resfile= ''):
        '''
        Constructor
        dbpath= folder where to locate h5 files
        resFile= instances of a SimRes object with result file
        '''
        self.__resfolder= respath
        self.__h5namefile= resfile
        
    def open(self, mode= 'r'):
        ''' h5name is name of the model '''
        self.__h5file= h5.File(self.__resfolder+ '/'+ self.__h5namefile, mode)
        self.__gResults= self.__h5file['mode_estimation_res']
            
    def select_modes(self):
        ''' build an array of EigenValues '''
        modes = []    
        self.__ddamp= self.__gResults['damp']
        self.__dfreq= self.__gResults['freq']
        for vdamp, vfreq in zip(self.__ddamp, self.__dfreq):
            mode= EigenValue(vdamp,vfreq)
            modes.append(mode)
        return modes
