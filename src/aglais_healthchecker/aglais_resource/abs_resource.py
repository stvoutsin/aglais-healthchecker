'''
Created on Jul 30, 2020

@author: stelios
'''
from abc import ABC, abstractmethod

class ServiceStatus(object):
    ERROR = "ERROR"
    OK = "OK"
    RESTARTED = "RESTARTED"
    
    
class AbsResource(ABC):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        