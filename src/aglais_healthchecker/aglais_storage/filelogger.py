'''
Created on Jul 30, 2020

@author: stelios
'''
import logging
from .logger import Logger
from . import StorageTypes

class FileLogger(Logger):
    '''
    Store information about the storage to be used for logging the output of a Healthcheck
    To start with we are using file, this may be extend to log to DBs or ElasticSearch etc..
    
    '''

    def __init__(self, **kwargs):
        '''
        Constructor
        '''
        self.storageType = StorageTypes.FILE
        if "path" in kwargs:
            self.path = kwargs["path"]
        if "file" in kwargs:
            self.file = kwargs["file"]
        if "mode" in kwargs:
            self.mode = kwargs["mode"]
        

    @property
    def file(self):
        return self.__file
    
    
    @file.setter 
    def file(self, file):
        self.__file = file    
    
    
    @property
    def path(self):
        return self.__path
    
    
    @path.setter 
    def path(self, path):
        self.__path = path
        
    
    @property
    def mode(self):
        return self.__mode
    
    
    @mode.setter 
    def mode(self, mode):
        self.__mode = mode    
        
    
    def log(self, dictionary):
        self._log_to_file(dictionary)
        return 
    
    
    def _log_to_file(self, dictionary):  
        """
        Log the given dictionary to File
        :type dictionary: dict
        :rtype: bool
        """
        try:  
            with open(self.path + "/" + self.file, "a") as myfile:
                for k, v in dictionary.items():
                    myfile.write("[" + k.upper() + "]: " + str(v))
                    myfile.write('\n')
                myfile.write('\n\n')
                
        except Exception as e:
            print(e)
            logging.debug(e)
        return True
