'''
Created on Jul 31, 2020

@author: stelios
'''
from . import Recoverer
import json


class ZeppelinRecoverer(Recoverer):
    '''
    Class used to perform a recovery process on a Zeppelin Resource
    Extends Recoverer class
    '''

    
    def __init__(self, params):
        '''
        Constructor
        '''


    @staticmethod
    def recover(resource):
        """
        Recover a Zeppelin Resource
        Perform a restart of the interpreter that we are using to test
        :type resource: ZeppelinResource
        """
        ZeppelinRecoverer.restart_interpreter(resource)
        return 
    
    
    @staticmethod
    def restart_interpreter(resource):
        """
        Restart a Zeppelin Interpeter
            http://[zeppelin-server]:[zeppelin-port]/api/interpreter/setting/restart/[interpreter ID]
            
        :type resource: ZeppelinResource
        """
        response = resource.session.put(resource.get_interpreter_restart_url())
        json_object = json.loads(response.text)
        if json_object.get("status", "Unknown") != "OK":
            raise Exception("Received status: {}". format(json_object.get("status", "Unknown")))
        else:
            return 
        