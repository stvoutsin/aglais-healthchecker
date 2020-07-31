'''
Created on Jul 30, 2020

@author: stelios
'''


class Auth(object):
    '''
    classdocs
    '''

    def __init__(self, username="", password="", token=""):
        '''
        Constructor
        '''
        self.username = username
        self.password = password
        self.token = token
       
       
    @property
    def username(self):
        return self.__username
    
    
    @username.setter 
    def username(self, username):
        self.__username = username


    @property
    def password(self):
        return self.__password
    
    
    @password.setter 
    def password(self, password):
        self.__password = password
        
        
    @property
    def token(self):
        return self.__token
    
    
    @token.setter 
    def token(self, token):
        self.__token = token
        
        
        
        
        