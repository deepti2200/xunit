#! python

import unittest
import sys
import logging
import os
sys.path.append((len(os.path.dirname(__file__))>0 and os.path.dirname(__file__) or '.' )+os.sep+'..'+os.sep+'..'+os.sep+'src'+os.sep)
sys.path.append((len(os.path.dirname(__file__))>0 and os.path.dirname(__file__) or '.' ))
import TestCaseLdr

class  LdrUnitTest(unittest.TestCase):
	def test_LoadFunction(self):
		ldr = TestCaseLdr.TestCaseLoaderBase()
		ldr.LoadCase('AUnit.AUnit:test_A')
		return

	def test_LoadModule(self):
		ldr = TestCaseLdr.TestCaseLoaderBase()
		ldr.LoadCase('AUnit.AUnit')
		return
		

	def test_NotFunction(self):
		ldr = TestCaseLdr.TestCaseLoaderBase()
		ok = 1
		try:
			ldr.LoadCase('AUnit.AUnit:test_NoFunction')
		except TestCaseLdr.LoadModuleError as e:
			ok = 0
		self.assertEqual(ok,0)
		return
 
	def test_NotLoadModule(self):
		ldr = TestCaseLdr.TestCaseLoaderBase()
		ok = 1
		try:
			ldr.LoadCase('NoModule.NoClass')
		except TestCaseLdr.LoadModuleError as e:
			ok = 0
		self.assertEqual(ok,0)
		return



if __name__ == '__main__':
	if '-v' in sys.argv[1:] or '--verbose' in sys.argv[1:]:
		logging.basicConfig(level=logging.INFO,format="%(levelname)-8s [%(filename)-10s:%(funcName)-20s:%(lineno)-5s] %(message)s")
	unittest.main()
