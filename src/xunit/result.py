#! python

import unittest
import logging
import xunit.config
from xunit.utils import cls
import xunit.logger
import time
from xunit.utils import exception

class FailFastException(exception.XUnitException):
	pass


class XUnitResultBase(unittest.runner.TextTestResult):
	def __init__(self):
		self.__fails = 0
		self.__succs = 0
		self.__skips = 0
		self.__cases = 0
		self.__unexpectfails = 0
		self.__unexpectsuccs = 0
		self.showAll = 0
		self.dots = 0
		self.shouldStop = False
		super(unittest.runner.TextTestResult,self).__init__(None,'',0)
		utcfg = xunit.config.XUnitConfig()
		v = utcfg.GetValue('global','debug.mode','')
		self.__logger = xunit.logger.ClassLogger('__main__')
		self.__verbose = 0
		if v == 'y':
			self.__verbose = 1
		self.__failfast = 0
		v = utcfg.GetValue('global','failfast','')
		if v == 'y':
			self.__failfast = 1
		return

	def startTest(self, test):
		if self.__verbose:
			cn = cls.GetClassName(test.__class__)
			self.__logger.CaseStart(cn+':'+test._testMethodName)
		return

	def addSuccess(self, test):
		self.__succs += 1
		self.__cases += 1
		if self.__verbose:
			self.__logger.CaseSucc('Success')
			self.__logger.CaseEnd('')
		return

	def addError(self, test, err):
		self.__fails += 1
		self.__cases += 1
		if self.__verbose:
			self.__logger.CaseError('Error')
			self.__logger.CaseEnd('')
		if self.__failfast:
			logging.error('\n')
			self.shouldStop = True
		return

	def addFailure(self, test, err):
		self.__fails += 1
		self.__cases += 1
		if self.__verbose:
			self.__logger.CaseFail('Failure')
			self.__logger.CaseEnd('')
		if self.__failfast:
			logging.error('\n')
			self.shouldStop = True
		return
	

	def addSkip(self, test, reason):
		self.__skips += 1
		self.__cases += 1
		if self.__verbose:
			self.__logger.CaseSkip('Skip')
			self.__logger.CaseEnd('')
		return

	def addExpectedFailure(self, test, err):
		self.__unexpectfails += 1
		self.__cases += 1
		if self.__verbose:
			self.__logger.CaseFail('Expected Failure')
			self.__logger.CaseEnd('')
		if self.__failfast:
			logging.error('\n')
			self.shouldStop = True
		return

	def addUnexpectedSuccess(self, test):
		self.__unexpectsuccs += 1
		self.__cases += 1
		if self.__verbose:
			self.__logger.CaseFail('Unexpected Success')
			self.__logger.CaseEnd('')
		if self.__failfast:
			logging.error('\n')
			self.shouldStop = True
		return

	def Cases(self):
		return self.__cases
	def Succs(self):
		return self.__succs

	def Fails(self):
		return self.__fails

	def Skips(self):
		return self.__skips

	def UnexpectFails(self):
		return self.__unexpectfails

	def UnexpectSuccs(self):
		return self.__unexpectsuccs

def singleton(cls):
	instances = {}
	def get_instance():
		if cls not in instances:
			instances[cls] = cls()
		return instances[cls]
	return get_instance

@singleton
class XUnitResult(XUnitResultBase):
	pass

