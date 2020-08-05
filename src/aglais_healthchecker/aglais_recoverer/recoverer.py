'''
Created on Jul 31, 2020

@author: stelios
'''
from abc import ABC, abstractstaticmethod

class Recoverer(ABC):
    '''
    Class used to recover a given Resource
    '''


    def __init__(self):
        '''
        Constructor
        '''
    
    @abstractstaticmethod
    def recover(self):        
        """
        Recover method
        """
        return