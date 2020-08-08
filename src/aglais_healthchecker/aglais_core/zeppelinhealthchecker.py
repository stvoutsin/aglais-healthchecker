'''
Created on Jul 30, 2020

@author: stelios
'''
import json
import requests
import time
import logging
from . import Healthchecker
from aglais_healthchecker.aglais_auth import Auth
from aglais_healthchecker.aglais_results import ZeppelinResults, Status as ZeppelinStatus
from aglais_healthchecker.aglais_resource import ZeppelinResource, ServiceStatus
from aglais_healthchecker.aglais_recoverer import ZeppelinRecoverer
from aglais_healthchecker.aglais_storage import Storage, StorageTypes


class ZeppelinHealthchecker(Healthchecker):
    '''
    Zeppelin HealthChecker Class
    
    Used to Health Check a list of resources using the REST API of each Zeppelin Resource.
    Resources are built from a configuration file, where you can define the list of resources, authentication configuration, paragraphs and cells to execute, and maxtimeouts
    and whether to recover the service
    
    If recover is True, also try to recover the Service if it does not respond.
    '''

    def __init__(self, config, isTest = False):
        '''
        Constructor
        '''
        self.config = config
        self.resources, self.hasValidConfig = self.unpack(config) 
        self.isTest = isTest
    
    
    @property
    def resources(self):
        return self.__resources
    
    
    @resources.setter 
    def resources(self, resources):
        self.__resources = resources    

    @property
    def config(self):
        return self.__config
    
    
    @config.setter 
    def config(self, config):
        self.resources, self.hasValidConfig = self.unpack(config) 
        self.__config = config    
            
    
    def loadConfig(self, config):
        self.config = config
        
    
    def hasValidConfig(self):
        """
        Return if Healthchecker has a valid configuration loaded
        """
        return self.hasValidConfig
    
    
    def unpack(self, configFile):
        """
        Unpack a configuration File and store the data for the Resources that will be healthchecked in Healthchecker object
        
        :type configFile: str
        :rtype: (dict, bool)
        """
        
        def _getResources(config):
            resources = []
            auth = None
            storage = None
            
            for r in config["resources"]:
                if "auth" in r:
                    auth = Auth(username=r["auth"]["username"], password=r["auth"]["password"])             
                if "logging" in r:
                    storage_obj = r["logging"]
                    storage = Storage(storage_obj["storageType"], **{  "file" : storage_obj["file"], "path" : storage_obj["path"]})
                resource = ZeppelinResource(url=r["url"], name=r["name"], max_execution_time=r["max_execution_time"], notebookid=r.get("notebookid",None), paragraphid=r.get("paragraphid",None), interpreterid=r.get("interpreterid",None), auth=auth, storage=storage)
                resources.append(resource)
            
            return resources

        unpacked = {}
        validConfig = True
        
        try:
            with open(configFile, 'r') as outfile:
                config = outfile.read()
            unpacked =  _getResources(json.loads(config))
        except Exception as e:
            print(e)
            logging.exception(e)
            validConfig = False
        finally:
            if not unpacked:
                validConfig = False   
        
        return (unpacked, validConfig)


    def _http_request(self, session, url, timeout=None):
        """
        Perform an HTTP Request and get output as a string
        
        :type session: requests.Session
        :type url: str
        :rtype: str
        """
        response_text = ""
        
        if timeout:
            r = session.post(url, timeout=timeout)
            response_text = r.text 
        else:
            r = session.post(url)
            response_text = r.text 
            
        return response_text
    
    
    def healthcheck(self, resources, recover=True):
        """
        Health Check a list of resources, Return response dictionary with status, message & timestamp of check
        If recover is True, also try to recover the Service if it does not respond.
        
        
        :type resources: List[ZeppelinResource]
        :type recover: bool
        :rtype: List[dict]
        
        """
        responses = []
        results = {}
        timestamp = time.strftime('%X %x %Z')

        for resource in resources:
            results[resource] = self.run_paragraphs(resource)
            
            response = {}
            for resource, result in results.items():
                try:
                    isAlive = result.isServiceAlive()
                    if not isAlive:
                        if recover:
                            ZeppelinRecoverer.recover(resource)
                            result.status = ZeppelinStatus.RESTARTED
                            response["message"] = "Service restarted at: {}".format(timestamp) 
                        else:
                            response["message"] = "Service Status: {}, but not recovered".format(resource.status)
                    else:
                        response["message"] = "Service Status: {}".format(resource.status)
                    response["status"] =  result.status
                except Exception as e:
                    logging.exception(e)
                    response["status"] = ZeppelinStatus.FAILED
                    response["message"] = e
                finally:
                    response["timestamp"] = timestamp 
                    # Log Results
                    resource.storage.log(response)
                    
                responses.append(response)
                resource.session.close()

        return responses
    
    
    def run_paragraphs(self, resource):
        """
        Run all Zeppelin test Paragraphs in resource
        :type resources: ZeppelinResource
        :rtype: ZeppelinResults
        """
        zepResults = ZeppelinResults()
        elapsed_time = 0
        start, end =  (0, 0)
        
        try:
            start = time.time()
            max_execution_time = resource.max_execution_time 
            session = resource.session
            
            if self.isTest:
                response_text = '{"status":"OK","body":{"code":"SUCCESS","msg":[{"type":"TEXT","data":"Pi is roughly 3.141573"}]}}'
            else:
                response_text = self._http_request(session, resource.get_paragraph_url(), max_execution_time)
            
            zepResults = ZeppelinResults(unparsed = response_text, executiontime=elapsed_time)
            end = time.time()
            elapsed_time = end - start
        except Exception as e:
            logging.exception(e)
            if start and not end:
                end = time.time()
                elapsed_time = end - start    
            resource.status = ServiceStatus.FAILED
            zepResults = ZeppelinResults(status=ZeppelinStatus.UNHEALTHY, msg=str(e), executiontime=elapsed_time)

        return zepResults
        
    
    def startmonitor(self, recover=False, timeout=60.0):
        """
        Start a monitor in a continuous loop, running the healthchecker every [timeout] seconds

        :type recover: bool
        :type timeout: float        
        """
        import time
        timeout = float(timeout)
        starttime = time.time()
        print(timeout, starttime)
        while True:
            self._healthCheck_wrapper(recover)
            time.sleep(timeout - ((time.time() - starttime) % timeout))
        
        
    def _healthCheck_wrapper(self, recover):
        """
        
        Wrapper funtion used to run a healthcheck on the Resources
        :type recover: bool 
        :rtype: 
        """
        self.healthcheck(self.resources, recover=recover)
        return


