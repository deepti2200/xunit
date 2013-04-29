
import logging
import sys
import os
import unittest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','src')))
from xunit import logger
from xunit import case
from xunit.utils import cls


_logs={}
class LoggerTest(case.XUnitCase):
	def test_Logger(self):
		logg1 = logger.AdvLogger()
		logg2 = logger.AdvLogger()
		self.assertEqual(logg1,logg2)
		if 'logger' in _logs.keys():
			self.assertEqual(logg1,_logs['logger'])
		else:
			_logs['logger'] = logg1
		return

	def test_Logger2(self):
		logg1 = logger.AdvLogger()
		logg2 = logger.AdvLogger()
		self.assertEqual(logg1,logg2)
		if 'logger' in _logs.keys():
			self.assertEqual(logg1,_logs['logger'])
		else:
			_logs['logger'] = logg1

		if 'logdiff' in _logs.keys():
			self.assertNotEqual(logg1,_logs['logdiff'])
		return

class LogDiffTest(case.XUnitCase):
	def test_Logger(self):
		logg1 = logger.AdvLogger()
		logg2 = logger.AdvLogger()
		self.assertEqual(logg1,logg2)
		if 'logdiff' in _logs.keys():
			self.assertEqual(logg1,_logs['logdiff'])
		else:
			_logs['logdiff'] = logg1
		return

	def test_Logger2(self):
		logg1 = logger.AdvLogger()
		logg2 = logger.AdvLogger()
		self.assertEqual(logg1,logg2)
		if 'logdiff' in _logs.keys():
			self.assertEqual(logg1,_logs['logdiff'])
		else:
			_logs['logdiff'] = logg1
		if 'logger' in _logs.keys():
			self.assertNotEqual(logg1,_logs['logger'])
		return

	def test_ClassLogger1(self):
		logg1 = logger.ClassLogger('class1')
		logg2 = logger.ClassLogger('class1')
		self.assertEqual(logg1,logg2)
		logg2 = logger.ClassLogger('class2')
		self.assertNotEqual(logg1,logg2)
		cn = cls.GetCallerClassName(1)
		logg1 = logger.AdvLogger()
		logg2 = logger.ClassLogger(cn)
		self.assertEqual(logg1,logg2)
		return
	


if __name__ == '__main__':
	if '-v' in sys.argv[1:] or '--verbose' in sys.argv[1:]:
		logging.basicConfig(level=logging.INFO,format="%(levelname)-8s [%(filename)-10s:%(funcName)-20s:%(lineno)-5s] %(message)s")	
	unittest.main()

