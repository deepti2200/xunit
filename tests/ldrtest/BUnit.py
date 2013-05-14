#! python

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','src')))
sys.path.append((os.path.dirname(os.path.abspath(__file__))))


from xunit.case import XUnitCase

class BUnit(XUnitCase):
	@classmethod
	def setUpClass(cls):
		sys.stdout.write('BUnit.BUnit:setUpClass\n')
		return

	@classmethod
	def tearDownClass(cls):
		sys.stdout.write('BUnit.BUnit:tearDownClass\n')
		return

	def setUp(self):
		sys.stdout.write('BUnit.BUnit:setUp\n')
		return

	def tearDown(self):
		sys.stdout.write('BUnit.BUnit:tearDown\n')
		return

	def test_BB(self):
		sys.stdout.write('BUnit.BUnit:test_BB\n')
		return
 	def test_BC(self):
 		sys.stdout.write('BUnit.BUnit:test_BC\n')
		return
