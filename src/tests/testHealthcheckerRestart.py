'''
Created on Jul 30, 2020

@author: stelios
'''
import unittest
from  aglais_healthchecker import ZeppelinHealthchecker
from aglais_healthchecker import Status

class TestZeppelinHealthcheck(unittest.TestCase):


    def setUp(self):
        config = "../data/sample-config.json"
        self.z = ZeppelinHealthchecker(config)
        pass


    def tearDown(self):
        pass


    def testNotHealthyRecover(self):
        result = self.z.healthcheck(self.z.resources, recover=True)[0]
        self.assertEqual(result["status"], Status.RESTARTED)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
    
    
    