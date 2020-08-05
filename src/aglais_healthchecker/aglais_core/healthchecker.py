'''
Created on Jul 30, 2020

@author: stelios
'''
from abc import ABC, abstractmethod

class Healthchecker(ABC):
    '''
    Healthchecker Abstract Class
      
    Perform a healthcheck on a given set of resources
      
    '''


    def __init__(self, config):
        '''
        Constructor
        '''
        pass


    @abstractmethod    
    def healthcheck(self):
        """
        Performs healthcheck
        """
        pass
    
    @abstractmethod
    def startmonitor(self):
        """
        Start the monitoring process as a continuous process
        """
        pass
    
    
    