'''
Created on Jul 30, 2020

@author: stelios
'''

class StorageTypes(object):
    FILE = "FILE"
    DATABASE = "DATABASE"
    
    
class Storage(object):
    '''
    Store information about the storage to be used for logging the output of a Healthcheck
    To start with we are using file, this may be extend to log to DBs or ElasticSearch etc..
    
    '''

    def __init__(self, storageType=None, name=None, path=None, mode='a'):
        '''
        Constructor
        '''
        self.storageType = storageType
        self.name = name
        self.path = path
        self.mode = mode


    @property
    def storageType(self):
        return self.__storageType
    
    
    @storageType.setter 
    def storageType(self, storageType):
        self.__storageType = storageType     
        
        
    @property
    def name(self):
        return self.__name
    
    
    @name.setter 
    def name(self, name):
        self.__name = name    
    
    
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
        if self.storageType == StorageTypes.FILE:
            self.log_to_file(dictionary)
        return 
    
    
    def log_to_file(self, dictionary):  
        """
        Log the given dictionary to File
        :type dictionary: dict
        :rtype: bool
        """
          
        with open(self.path + "/" + self.name, "a") as myfile:
            for k, v in dictionary.items():
                myfile.write(k + ": " + str(v))
                myfile.write('\n')
            myfile.write('\n\n')

        return True