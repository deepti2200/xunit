
import logging
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','src')))
import xunit.case
import xunit.utils.cls
import unittest
class XUnitTest(xunit.case.XUnitCase):
	@classmethod
	def XUnitsetUpClass(cls):
		cls._cls_set =1
		cls._case_count = 0
		cls._case_set = 0		
		return

	@classmethod
	def XUnittearDownClass(cls):
		assert(cls._cls_set == 1)
		assert(cls._case_count >= 0)
		assert(cls._case_set == 0)
		return

	def XUnitsetUp(self):
		assert(self._case_set  == 0)
		self._case_set = 1
		self._case_count += 1 
		return
	def XUnittearDown(self):
		assert(self._case_set == 1)
		self._case_set = 0
		return

	def test_OneCase(self):
		self.assertEqual(self._case_set,1)
		self.assertTrue(self._case_count > 0)
		return

if __name__ == '__main__':
	if '-v' in sys.argv[1:] or '--verbose' in sys.argv[1:]:
		logging.basicConfig(level=logging.INFO,format="%(levelname)-8s [%(filename)-10s:%(funcName)-20s:%(lineno)-5s] %(message)s")	
	unittest.main()
