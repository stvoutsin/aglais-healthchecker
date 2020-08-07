'''
Created on Jul 30, 2020

@author: stelios
'''
import logging
from .filelogger import FileLogger
from .storageTypes import StorageTypes    

class Storage(object):
    '''
    Store information about the storage to be used for logging the output of a Healthcheck
    To start with we are using file, this may be extend to log to DBs or ElasticSearch etc..
    
    '''
    
    storageEngines = {StorageTypes.FILE : FileLogger}
        

    def __init__(self, storageType=None, **kwargs):
        '''
        Constructor
        '''
        self.storageType = storageType
        self.storageEngine = self.storageEngines[storageType](**kwargs)
        
        
    def addStorageEngine(self, name, engine):
        self.storageEngines[name] = engine
        

    @property
    def storageType(self):
        return self.__storageType
    
    
    @storageType.setter 
    def storageType(self, storageType):
        self.__storageType = storageType     
    
    
    def log(self, dictionary):
        self.storageEngine.log(dictionary)
        return 
    
    
