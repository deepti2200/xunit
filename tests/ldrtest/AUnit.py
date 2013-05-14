#! python

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','src')))
sys.path.append((os.path.dirname(os.path.abspath(__file__))))


from xunit.case import XUnitCase
class AUnit(XUnitCase):
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
