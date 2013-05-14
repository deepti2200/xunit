#! python

import unittest
import sys
import logging
import os
import subprocess
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','src')))
sys.path.append((os.path.dirname(os.path.abspath(__file__))))
import xunit.suite
import AUnit
from xunit.case import XUnitCase

class  LdrUnitTest(XUnitCase):
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
		ldr = xunit.suite.XUnitSuiteBase()
		ldr.LoadCase('AUnit.AUnit:test_A')
		_res = self.__hasUnitMethod(ldr,'test_A','AUnit.AUnit')
		self.assertEqual(_res,1)
		return

	def test_LoadModule(self):
		ldr = xunit.suite.XUnitSuiteBase()
		ldr.LoadCase('AUnit.AUnit')
		_res = self.__hasUnitMethod(ldr,'test_B', 'AUnit.AUnit')
		self.assertEqual(_res,1)
		return
		

	def test_NotFunction(self):
		ldr = xunit.suite.XUnitSuiteBase()
		ok = 1
		try:
			ldr.LoadCase('AUnit.AUnit:test_NoFunction')
		except xunit.suite.LoadModuleError as e:
			ok = 0
		self.assertEqual(ok,0)
		return
 
	def test_NotLoadModule(self):
		ldr = xunit.suite.XUnitSuiteBase()
		ok = 1
		try:
			ldr.LoadCase('NoModule.NoClass')
		except xunit.suite.LoadModuleError as e:
			ok = 0
		self.assertEqual(ok,0)
		return

	def test_2ClassAdd(self):
		ldr = xunit.suite.XUnitSuiteBase()
		ldr.LoadCase('BUnit.BUnit')
		ldr.LoadCase('AUnit.AUnit')
		_res = self.__hasUnitMethod(ldr,'test_B', 'AUnit.AUnit')
		self.assertEqual(_res,1)
		_res = self.__hasUnitMethod(ldr,'test_BB','BUnit.BUnit')
		self.assertEqual(_res,1)
		return

	def test_Load1SuccAndFailed(self):
		ldr = xunit.suite.XUnitSuiteBase()
		ldr.LoadCase('BUnit.BUnit')
		ok = 1
		try:
			ldr.LoadCase('NoModule.NoClass')
		except xunit.suite.LoadModuleError as e:
			ok = 0
		self.assertEqual(ok,0)
		_res = self.__hasUnitMethod(ldr,'test_BB','BUnit.BUnit')
		self.assertEqual(_res,1)
		return

	def test_LoadClassAndFunction(self):
		ldr = xunit.suite.XUnitSuiteBase()
		ldr.LoadCase('BUnit.BUnit')
		ldr.LoadCase('AUnit.AUnit:test_A')
		_res = self.__hasUnitMethod(ldr,'test_B', 'AUnit.AUnit')
		self.assertEqual(_res,0)
		_res = self.__hasUnitMethod(ldr,'test_A', 'AUnit.AUnit')
		self.assertEqual(_res,1)
		_res = self.__hasUnitMethod(ldr,'test_BB','BUnit.BUnit')
		self.assertEqual(_res,1)
		return

	def __CallProcessReturn(self,cmd):
		sp = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		op = sp.stdout
		ls = op.readlines()
		ol = []
		for l in ls:
			ol.append(l.rstrip('\r\n'))
		return ol

	def __FindLineIdx(self,ls,s):
		i = 0
		idx = -1
		for l in ls:
			if s == l:
				idx = i
				break
			i += 1
		return idx
	def test_RunTestCase1(self):
		absd = os.path.dirname(os.path.abspath(__file__))
		# now we should give the process running
		cmd = 'python %s'%(absd)
		cmd += os.sep
		cmd += 'rtest.py'
		cmd += ' -p %s'%(absd)
		cmd += '  AUnit.AUnit:test_A '
		ol = self.__CallProcessReturn(cmd)
		self.assertTrue(len(ol) > 0)
		idx = self.__FindLineIdx(ol,'AUnit.AUnit:test_A')
		self.assertTrue(idx >= 0)
		return

	def test_RunTestCase2(self):
		absd = os.path.dirname(os.path.abspath(__file__))
		cmd = 'python %s'%(absd)
		cmd += os.sep
		cmd += 'rtest.py'
		cmd += ' -p %s'%(absd)
		cmd += ' BUnit.BUnit:test_BB '
		cmd += '  AUnit.AUnit:test_A '
		ol = self.__CallProcessReturn(cmd)
		ol = self.__CallProcessReturn(cmd)
		self.assertTrue(len(ol) > 0)
		aidx = self.__FindLineIdx(ol,'AUnit.AUnit:test_A')
		self.assertTrue(aidx >= 0)
		bidx = self.__FindLineIdx(ol,'BUnit.BUnit:test_BB')
		self.assertTrue(bidx >= 0)
		# call bunit earlier than aunit
		self.assertTrue(bidx < aidx)
		return

	def test_RunTestCase3(self):
		absd = os.path.dirname(os.path.abspath(__file__))
		cmd = 'python %s'%(absd)
		cmd += os.sep
		cmd += 'rtest.py'
		cmd += ' -p %s'%(absd)
		cmd += ' -p %s'%(absd)
		cmd += os.sep
		cmd += 'inc'
		cmd += ' BUnit.BUnit:test_BB '
		cmd += '  CUnit.CUnit:test_CC '
		cmd += ' BUnit.BUnit:test_BC '
		ol = self.__CallProcessReturn(cmd)
		ol = self.__CallProcessReturn(cmd)
		self.assertTrue(len(ol) > 0)
		cidx = self.__FindLineIdx(ol,'CUnit.CUnit:test_CC')
		self.assertTrue(cidx >= 0)
		bidx = self.__FindLineIdx(ol,'BUnit.BUnit:test_BB')
		self.assertTrue(bidx >= 0)
		# call bunit earlier than aunit
		self.assertTrue(bidx < cidx)
		bcidx = self.__FindLineIdx(ol,'BUnit.BUnit:test_BC')
		self.assertTrue(bcidx >= 0 )
		self.assertTrue(cidx < bcidx)
		return


if __name__ == '__main__':
	if '-v' in sys.argv[1:] or '--verbose' in sys.argv[1:]:
		logging.basicConfig(level=logging.INFO,format="%(levelname)-8s [%(filename)-10s:%(funcName)-20s:%(lineno)-5s] %(message)s")
	unittest.main()
