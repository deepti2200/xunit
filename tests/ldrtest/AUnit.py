#! python

import unittest
import sys
class AUnit(unittest.TestCase):
	def test_A(self):
		sys.stdout.write('AUnit.AUnit:test_A\n')
		return

	def test_B(self):
		sys.stdout.write('AUnit.AUnit:test_B\n')
		return
if __name__ == '__main__':
	m = __import__('__main__')
	cls = getattr(m,'AUnit')
	print('%s'%(AUnit))
	tests = unittest.loader.TestLoader().loadTestsFromTestCase(AUnit)
	print('cls %s'%(cls))
	tests = unittest.loader.TestLoader().loadTestsFromTestCase(cls)
	print('cls %s'%(cls))
