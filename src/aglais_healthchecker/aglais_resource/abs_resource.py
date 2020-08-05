'''
Created on Jul 30, 2020

@author: stelios
'''
from abc import ABC, abstractmethod

class ServiceStatus(object):
    """
    Enum for the status of a service
    """
    OK = "OK"
    FAILED = "FAILED"
    
    
class AbsResource(ABC):
    '''
    Abstract Resource class
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        