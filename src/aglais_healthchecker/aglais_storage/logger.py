'''
Created on Jul 30, 2020

@author: stelios
'''
import logging
from abc import ABC, abstractmethod

class Logger(ABC):
    '''
    Store information about the storage to be used for logging the output of a Healthcheck
    To start with we are using file, this may be extend to log to DBs or ElasticSearch etc..
    
    '''

    def __init__(self):
        '''
        Constructor
        '''
        pass

    @abstractmethod
    def log(self):
        pass
   