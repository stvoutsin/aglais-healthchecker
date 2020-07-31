'''
Created on Jul 31, 2020

@author: stelios
'''
from . import Recoverer
import requests
import json


class ZeppelinRecoverer(Recoverer):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''

    @staticmethod
    def recover(resource):
        ZeppelinRecoverer.restart_interpreter(resource)
        return 
    
    
    @staticmethod
    def restart_interpreter(resource):
        """
        Restart a Zeppelin Interpeter
            http://[zeppelin-server]:[zeppelin-port]/api/interpreter/setting/restart/[interpreter ID]
        """
        response = resource.session.put(resource.get_interpreter_restart_url())
        json_object = json.loads(response.text)
        if json_object.get("status", "Unknown") != "OK":
            raise Exception("Received status: {}". format(json_object.get("status", "Unknown")))
        else:
            return 
        