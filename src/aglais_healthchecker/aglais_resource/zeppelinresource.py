'''
Created on Jul 30, 2020

@author: stelios
'''
from . import AbsResource
from . import ServiceStatus
import requests


class ZeppelinResource(AbsResource):
    '''
    Class to hold information for Zeppelin Service
    
    '''


    def __init__(self, url=None, name=None, max_execution_time=None, notebookid=None, paragraphid=None, interpreterid=None, auth=None, storage=None):
        '''
        Constructor
        '''
        self.baseurl = url
        self.url = url + "/api"
        self.name = name
        self.max_execution_time = max_execution_time 
        self.notebookid = notebookid
        self.paragraphid = paragraphid
        self.interpreterid = interpreterid
        self.auth = auth
        self.storage = storage
        self.session = requests.Session()
        self.authenticate()
        self.status = ServiceStatus.OK
        
        
    def authenticate(self):
        """
        Authenticate a user, using the parameters from the configuration
        """
        self.session = requests.Session()
        self.session.post(self.url + "/login",data={"userName" : self.auth.username, "password" : self.auth.password})
            
            
    def get_paragraph_url(self):
        """
        Formulate the paragraph URL to run for the REST API
    
          http://[zeppelin-server]:[zeppelin-port]/api/notebook/run/[noteId]/[paragraphId]
        """
        return self.url + "/notebook/run/" + self.notebookid + "/" + self.paragraphid
        
        
    def get_interpreter_restart_url(self):
        """
        Formulate the interpeter restart URL to run for the REST API

          http://[zeppelin-server]:[zeppelin-port]/api/interpreter/setting/restart/[interpreter ID]
        """
        return self.url + "/interpreter/setting/restart/" + self.interpreterid        
    
    
    