'''
Created on Jul 30, 2020

@author: stelios
'''
import unittest
from  aglais_healthchecker import ZeppelinHealthchecker

class TestZeppelinHealthcheck(unittest.TestCase):


    def setUp(self):
        with open('../data/sample-config.json', 'r') as outfile:
            config = outfile.read()
    
        self.z = ZeppelinHealthchecker(config)
        pass


    def tearDown(self):
        pass


    def testName(self):
        result = self.z.healthcheck(self.z.resources, recover=True)
        self.assertEquals(result["status"], "OK")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
    
    
    