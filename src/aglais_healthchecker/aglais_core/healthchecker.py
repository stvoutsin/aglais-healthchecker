'''
Created on Jul 30, 2020

@author: stelios
'''
from abc import ABC, abstractmethod

class Healthchecker(ABC):
    '''
    Healthchecker Abstract Class    
    '''


    def __init__(self, config):
        '''
        Constructor
        '''
        pass
        
    @abstractmethod
    def unpack(self, config):
        return 
    
    @abstractmethod    
    def healthcheck(self):
        pass
    
    @abstractmethod
    def startmonitor(self):
        pass
    
    
    