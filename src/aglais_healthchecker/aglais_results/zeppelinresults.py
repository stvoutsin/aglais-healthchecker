'''
Created on Jul 30, 2020

@author: stelios
'''
from . import Results
import json


class Status(object):
    """
    Enum type class to hold Status of a Health check
    """
    RESTARTED = "RESTARTED"
    HEALTHY = "HEALTHY"
    UNHEALTHY = "UNHEALTHY"
    FAILED = "FAILED"


class ZeppelinResults(Results):
    '''
    Store the information on the results of the execution of a Healthcheck on a Zeppelin Resource
    '''

    def __init__(self, status=None, msg=None, executiontime=None, unparsed=None):
        '''
        Constructor
        Example of unparsed input:
            {"status":"OK","body":{"code":"SUCCESS","msg":[{"type":"TEXT","data":"Pi is roughly 3.141573\n"}]}}
            
        '''
        if unparsed: 
            self.msg, self.status = self._unpack(unparsed)
        else:
            self.msg = msg
            self.status = status
        self.executiontime = executiontime
        

    @property
    def executiontime(self):
        return self.__executiontime
    
    
    @executiontime.setter 
    def executiontime(self, executiontime):
        self.__executiontime = executiontime
        
        
    @property
    def status(self):
        return self.__status
    
    
    @status.setter 
    def status(self, status):
        self.__status = status


    @property
    def msg(self):
        return self.__msg
    
    
    @msg.setter 
    def msg(self, msg):
        self.__msg = msg
 
        
    def _unpack(self, packed):    
        """
        Unpack the packed JSON object and return as msg, status
        :type packed: str
        :rtype: tuple
        """
        try:
            status, msg = None, None
            json_object  = json.loads(packed)
            body = json_object.get('body', {})
            status = body.get('code',"").upper() 
            fullmessage = body.get('msg',[])
            if len(fullmessage)>0:
                msg = fullmessage[0].get('data',None)
        except Exception as e:
            status = Status.FAILED
            msg = e
            
        return (msg, status)
    
    
    def isServiceAlive(self):
        """
        Return if the Zeppelin Service is alive or not
        :rtype: bool
        """
        return self.status == Status.HEALTHY

    
    def __str__(self):
        """
        Return String representation
        """
        return "Message: {}\nStatus: {}\nExecution Time: {:.2f}\n".format(self.msg,self.status,self.executiontime)    
        

