#! python

import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','src')))
sys.path.append((os.path.dirname(os.path.abspath(__file__))))


from xunit.case import XUnitCase
class DUnit1(XUnitCase):
	def test_A(self):
		sys.stdout.write('DUnit.DUnit1:test_A\n')
		return

	def test_B(self):
		sys.stdout.write('DUnit.DUnit1:test_B\n')
		return

class DUnit2(XUnitCase):
	def test_A(self):
		sys.stdout.write('DUnit.DUnit2:test_A\n')
		return

	def test_B(self):
		sys.stdout.write('DUnit.DUnit2:test_B\n')
		return

class DUnit3(XUnitCase):
	def test_A(self):
		sys.stdout.write('DUnit.DUnit3:test_A\n')
		return

	def test_B(self):
		sys.stdout.write('DUnit.DUnit3:test_B\n')
		return

	
if __name__ == '__main__':
	m = __import__('__main__')
	cls = getattr(m,'DUnit1')
	print('%s'%(DUnit1))
	tests = unittest.loader.TestLoader().loadTestsFromTestCase(DUnit1)
	print('cls %s'%(cls))
	tests = unittest.loader.TestLoader().loadTestsFromTestCase(cls)
	print('cls %s'%(cls))
	

