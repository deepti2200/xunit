
import logging
import sys
import os
import unittest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','src')))
import xunitlogger
import xunitcase


_logs={}
class LoggerTest(xunitcase.XUnitCase):
	def test_Logger(self):
		logg1 = xunitlogger.AdvLogger()
		logg2 = xunitlogger.AdvLogger()
		self.assertEqual(logg1,logg2)
		if 'logger' in _logs.keys():
			self.assertEqual(logg1,_logs['logger'])
		else:
			_logs['logger'] = logg1
		return

	def test_Logger2(self):
		logg1 = xunitlogger.AdvLogger()
		logg2 = xunitlogger.AdvLogger()
		self.assertEqual(logg1,logg2)
		if 'logger' in _logs.keys():
			self.assertEqual(logg1,_logs['logger'])
		else:
			_logs['logger'] = logg1

		if 'logdiff' in _logs.keys():
			self.assertNotEqual(logg1,_logs['logdiff'])
		return

class LogDiffTest(xunitcase.XUnitCase):
	def test_Logger(self):
		logg1 = xunitlogger.AdvLogger()
		logg2 = xunitlogger.AdvLogger()
		self.assertEqual(logg1,logg2)
		if 'logdiff' in _logs.keys():
			self.assertEqual(logg1,_logs['logdiff'])
		else:
			_logs['logdiff'] = logg1
		return

	def test_Logger2(self):
		logg1 = xunitlogger.AdvLogger()
		logg2 = xunitlogger.AdvLogger()
		self.assertEqual(logg1,logg2)
		if 'logdiff' in _logs.keys():
			self.assertEqual(logg1,_logs['logdiff'])
		else:
			_logs['logdiff'] = logg1
		if 'logger' in _logs.keys():
			self.assertNotEqual(logg1,_logs['logger'])
		return
	


if __name__ == '__main__':
	if '-v' in sys.argv[1:] or '--verbose' in sys.argv[1:]:
		logging.basicConfig(level=logging.INFO,format="%(levelname)-8s [%(filename)-10s:%(funcName)-20s:%(lineno)-5s] %(message)s")	
	unittest.main()

