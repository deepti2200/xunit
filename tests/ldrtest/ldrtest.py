#! python

import unittest
import sys
import logging
import os
sys.path.append((len(os.path.dirname(__file__))>0 and os.path.dirname(__file__) or '.' )+os.sep+'..'+os.sep+'..'+os.sep+'src'+os.sep)
sys.path.append((len(os.path.dirname(__file__))>0 and os.path.dirname(__file__) or '.' ))
import TestCaseLdr
import AUnit

class  LdrUnitTest(unittest.TestCase):
	def __hasUnitMethod(self,suite,fn,cn):
		_res = 0
		try:
			for t in suite:
				if isinstance(t,unittest.TestSuite):
					for tc in t:
						vname='%s (%s)'%(fn,cn)
						if str(tc) == fn or str(tc) == vname:
							_res  = 1
							raise Exception('\n')
				else:
					vname = '%s (%s)'%(fn,cn)
					if str(t) == vname:
						_res = 1
						raise Exception('\n')
		except Exception:
			pass
		return _res
	def test_LoadFunction(self):
		ldr = TestCaseLdr.TestCaseLoaderBase()
		ldr.LoadCase('AUnit.AUnit:test_A')
		_res = self.__hasUnitMethod(ldr,'test_A','AUnit.AUnit')
		self.assertEqual(_res,1)
		return

	def test_LoadModule(self):
		ldr = TestCaseLdr.TestCaseLoaderBase()
		ldr.LoadCase('AUnit.AUnit')
		_res = self.__hasUnitMethod(ldr,'test_B', 'AUnit.AUnit')
		self.assertEqual(_res,1)
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

	def test_2ClassAdd(self):
		ldr = TestCaseLdr.TestCaseLoaderBase()
		ldr.LoadCase('BUnit.BUnit')
		ldr.LoadCase('AUnit.AUnit')
		_res = self.__hasUnitMethod(ldr,'test_B', 'AUnit.AUnit')
		self.assertEqual(_res,1)
		_res = self.__hasUnitMethod(ldr,'test_BB','BUnit.BUnit')
		self.assertEqual(_res,1)
		return

	def test_Load1SuccAndFailed(self):
		ldr = TestCaseLdr.TestCaseLoaderBase()
		ldr.LoadCase('BUnit.BUnit')
		ok = 1
		try:
			ldr.LoadCase('NoModule.NoClass')
		except TestCaseLdr.LoadModuleError as e:
			ok = 0
		self.assertEqual(ok,0)
		_res = self.__hasUnitMethod(ldr,'test_BB','BUnit.BUnit')
		self.assertEqual(_res,1)
		return

	def test_LoadClassAndFunction(self):
		ldr = TestCaseLdr.TestCaseLoaderBase()
		ldr.LoadCase('BUnit.BUnit')
		ldr.LoadCase('AUnit.AUnit:test_A')
		_res = self.__hasUnitMethod(ldr,'test_B', 'AUnit.AUnit')
		self.assertEqual(_res,0)
		_res = self.__hasUnitMethod(ldr,'test_A', 'AUnit.AUnit')
		self.assertEqual(_res,1)
		_res = self.__hasUnitMethod(ldr,'test_BB','BUnit.BUnit')
		self.assertEqual(_res,1)
		return	


if __name__ == '__main__':
	if '-v' in sys.argv[1:] or '--verbose' in sys.argv[1:]:
		logging.basicConfig(level=logging.INFO,format="%(levelname)-8s [%(filename)-10s:%(funcName)-20s:%(lineno)-5s] %(message)s")
	unittest.main()
