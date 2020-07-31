'''
Created on Jul 30, 2020

@author: stelios
'''
import json
import requests
import time

from . import Healthchecker
from aglais_healthchecker.aglais_auth import Auth
from aglais_healthchecker.aglais_results import ZeppelinResults
from aglais_healthchecker.aglais_resource import ZeppelinResource, ServiceStatus
from aglais_healthchecker.aglais_recoverer import ZeppelinRecoverer
from aglais_healthchecker.aglais_storage import Storage, StorageTypes


class ZeppelinHealthchecker(Healthchecker):
    '''
    classdocs
    '''

    def __init__(self, config):
        '''
        Constructor
        '''
        self._unpacked = self.unpack(config)
        self.resources = self._unpacked["resources"]
        
        
    @property
    def resources(self):
        return self.__resources
    
    
    @resources.setter 
    def resources(self, resources):
        self.__resources = resources    
    
    
    def unpack(self, config):
        
        def _getResources(config):
            resources = []
            auth = None
            storage = None
            
            for r in config["resources"]:
                if "auth" in r:
                    auth = Auth(username=r["auth"]["username"], password=r["auth"]["password"])
               
                if "logging" in r:
                    storage_obj = r["logging"]
                    storage = Storage(storage_obj["storageType"], storage_obj["file"], storage_obj["path"])
                    
                resource = ZeppelinResource(url=r["url"], name=r["name"], max_execution_time=r["max_execution_time"], notebookid=r.get("notebookid",None), paragraphid=r.get("paragraphid",None), interpreterid=r.get("interpreterid",None), auth=auth, storage=storage)
                resources.append(resource)
            
            return resources
        
        result = {}
        unpacked = json.loads(config)
        result["resources"] = _getResources(unpacked)
        return result


    def _http_request(self, session, url, timeout=None):
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
        Health Check a list of resources
        """
        response = {}
        timestamp = time.strftime('%X %x %Z')

        try:
            results = self.run_paragraphs(resources)
            for resource, result in results.items():
                isAlive = self.validate_results(result)
                if not isAlive:
                    if recover:
                        resource.status = ServiceStatus.ERROR
                        ZeppelinRecoverer.recover(resource)
                        resource.status = ServiceStatus.RESTARTED
                        response["message"] = "Service restarted at: {}".format(timestamp) if resource.status == ServiceStatus.RESTARTED else ""
                    else:
                        response["message"] = "Service is UNHEALTHY, but not recovered"
                else:
                    response["message"] = "Service is HEALTHY"

            response["status"] =  resource.status

        except Exception as e:
            response["status"] = "FAILED"
            response["message"] = e
        
        response["timestamp"] = timestamp 

        # Log Results
        resource.storage.log(response)
    
        return response
    
    
    def validate_results(self, result):
        return result.is_service_alive()
    
    
    def run_paragraphs(self, resources):
        """
        Run all Zeppelin test Paragraphs in resources
        """
        zepResults = ZeppelinResults()
        elapsed_time = 0
        start, end =  (0, 0)
        results = {}
        
        for resource in resources:
            
            try:
                start = time.time()
                storage = resource.storage
                max_execution_time = resource.max_execution_time 
                session = resource.session
                response_text = self._http_request(session, resource.get_paragraph_url(), max_execution_time)
                #response_text = '{"status":"OK","body":{"code":"SUCCESS","msg":[{"type":"TEXT","data":"Pi is roughly 3.141573"}]}}'
                zepResults = ZeppelinResults(unparsed = response_text, executiontime=elapsed_time)
                end = time.time()
                elapsed_time = end - start
                
            except Exception as e:
                if start and not end:
                    end = time.time()
                    elapsed_time = end - start    
                zepResults = ZeppelinResults(status="FAILED", msg=e, executiontime=elapsed_time)
            print(zepResults)

            results[resource] = zepResults
        return results
        
    
    def startmonitor(self):
        pass
    