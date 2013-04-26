#! python


import unittest
import sys
import os
sys.path.append(os.path.abspath((os.path.dirname(os.path.abspath(__file__)))+os.sep+'..'+os.sep+'..'+os.sep+'src'))
import clsname
import logging
#sys.path.append(os.path.abspath((os.path.dirname(os.path.abspath(__file__)))+os.sep+'inc'+os.sep+'base' ))
import incbunit


class AUnit(object):
	def GetMsg(self):
		return clsname.GetCallerClassName(1)
	class AUnit2(object):
		def GetMsg(self):
			return clsname.GetCallerClassName(1) 
		class AUnit3(object):
			def GetMsg(self):
				return clsname.GetCallerClassName(1) 


class ClsNameTest(unittest.TestCase):
	def test_mainClass(self):
		a = AUnit()
		self.assertTrue(a.GetMsg(),'__main__.AUnit')
		a = AUnit.AUnit2()
		self.assertTrue(a.GetMsg(),'__main__.AUnit.AUnit2')
		a = AUnit.AUnit2.AUnit3()
		self.assertTrue(a.GetMsg(),'__main__.AUnit.AUnit2.AUnit3')
		return

	def test_CallImportClass(self):
		b = incbunit.base.BUnit.BUnit()
		self.assertTrue(b.GetMsg(),'incbunit.base.BUnit.BUnit')
		b = incbunit.base.BUnit.BUnit.BUnit2()
		self.assertTrue(b.GetMsg(),'incbunit.base.BUnit.BUnit.BUnit2')
		b = incbunit.base.BUnit.BUnit.BUnit2.BUnit3()
		self.assertTrue(b.GetMsg(),'incbunit.base.BUnit.BUnit.BUnit2.BUnit3')
		return


if __name__ == '__main__':
	if '-v' in sys.argv[1:] or '--verbose' in sys.argv[1:]:
		logging.basicConfig(level=logging.INFO,format="%(levelname)-8s [%(filename)-10s:%(funcName)-20s:%(lineno)-5s] %(message)s")
	unittest.main()
