
import logging
import sys
import os
import unittest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','src')))
from xunit import logger
from xunit import case
from xunit.utils import cls
import re


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

	def test_LoggerString(self):
		log1 = logger.AdvLogger()
		log1.SetLevel(logger.INFO_LEVEL)
		log1.SetOutput(0)
		log1.Info('hello')
		log1.Info('self')
		v = log1.Flush()
		self.assertTrue(v is not None)
		vpat = re.compile('hello')
		self.assertTrue(vpat.search(v))
		vpat = re.compile('self')
		self.assertTrue(vpat.search(v))
		log1.Info('news')
		log1.Info('make')
		v = log1.Flush()
		self.assertTrue(v is not None)
		vpat = re.compile('hello')
		self.assertTrue(not vpat.search(v))
		vpat = re.compile('self')
		self.assertTrue(not vpat.search(v))
		vpat = re.compile('news')
		self.assertTrue(vpat.search(v))
		vpat = re.compile('make')
		self.assertTrue(vpat.search(v))
		# to get the none if nothing in it
		v = log1.Flush()
		self.assertEqual( v , '')
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
		logging.basicConfig(level=logging.INFO,format="%(levelname)-8s [%(filename)-10s:%(lineno)-5s] %(message)s")	
		pass
	unittest.main()

