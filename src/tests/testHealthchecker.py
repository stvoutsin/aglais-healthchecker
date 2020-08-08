'''
Created on Jul 30, 2020

@author: stelios
'''
import unittest
from  aglais_healthchecker import ZeppelinHealthchecker
from aglais_healthchecker import Status
 

class TestZeppelinHealthcheckHealthy(unittest.TestCase):


    def setUp(self):
        config = "../data/sample-config-healthy.json"
        self.z = ZeppelinHealthchecker(config)
        pass


    def tearDown(self):
        pass


    def testHealthy(self):
        result = self.z.healthcheck(self.z.resources, recover=False)[0]
        self.assertEqual(result["status"], Status.SUCCESS)



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
    
    
    