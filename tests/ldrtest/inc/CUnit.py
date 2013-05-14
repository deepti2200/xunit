#! python

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','..','src')))
sys.path.append((os.path.dirname(os.path.abspath(__file__))))


from xunit.case import XUnitCase
class CUnit(XUnitCase):
	@classmethod
	def setUpClass(cls):
		sys.stdout.write('CUnit.CUnit:setUpClass\n')
		return

	@classmethod
	def tearDownClass(cls):
		sys.stdout.write('CUnit.CUnit:tearDownClass\n')
		return

	def setUp(self):
		sys.stdout.write('CUnit.CUnit:setUp\n')
		return

	def tearDown(self):
		sys.stdout.write('CUnit.CUnit:tearDown\n')
		return

	def test_CC(self):
		sys.stdout.write('CUnit.CUnit:test_CC\n')
		return
 	def test_CD(self):
 		sys.stdout.write('CUnit.CUnit:test_CD\n')
		return

