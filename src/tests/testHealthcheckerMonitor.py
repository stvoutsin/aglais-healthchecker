'''
Created on Jul 30, 2020

@author: stelios
'''
import unittest
from  aglais_healthchecker import ZeppelinHealthchecker
from aglais_healthchecker import Status
 

class TestZeppelinHealthcheckMonitor(unittest.TestCase):


    def setUp(self):
        config = "../data/sample-config-healthy.json"
        self.z = ZeppelinHealthchecker(config)
        pass


    def tearDown(self):
        pass


    def testMonitor(self):
        self.z.startmonitor(recover=False,timeout=60)
        return True


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
    
    
    