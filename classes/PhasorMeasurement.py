'''
Created on 7 apr 2015

@author: fragom
'''
import itertools
from numpy import rad2deg,angle

class PhasorMeasurement(object):
    '''
    classdocs
    '''
    _time= []
    _magnitude= []
    _angle= []
    _source= ''
    _unit= ''

    def __init__(self):
        '''
        Constructor
        '''
    
    def get_time(self):
        return self._time

    def get_magnitude(self):
        return self._magnitude


    def get_angle(self):
        return self._angle


    def get_source(self):
        return self._source


    def get_unit(self):
        return self._unit


    def set_time(self, value):
        self._time= value
    
    def set_magnitude(self, value):
        self._magnitude = value


    def set_angle(self, value):
        self._angle = value


    def set_source(self, value):
        self._source = value


    def set_unit(self, value):
        self._unit = value


    def del_time(self):
        del self._time
        
    def del_magnitude(self):
        del self._magnitude


    def del_angle(self):
        del self._angle


    def del_source(self):
        del self._source


    def del_unit(self):
        del self._unit

    time = property(get_time, set_time, del_time, "time's docstring")
    magnitude = property(get_magnitude, set_magnitude, del_magnitude, "magnitude's docstring")
    angle = property(get_angle, set_angle, del_angle, "angle's docstring")
    source = property(get_source, set_source, del_source, "source's docstring")
    unit = property(get_unit, set_unit, del_unit, "unit's docstring")
        