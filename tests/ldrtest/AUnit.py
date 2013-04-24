#! python

import unittest

class AUnit(unittest.TestCase):
	def test_A(self):
		pass

	def test_B(self):
		pass

if __name__ == '__main__':
	m = __import__('__main__')
	cls = getattr(m,'AUnit')
	print('%s'%(AUnit))
	tests = unittest.loader.TestLoader().loadTestsFromTestCase(AUnit)
	print('cls %s'%(cls))
	tests = unittest.loader.TestLoader().loadTestsFromTestCase(cls)
	print('cls %s'%(cls))
