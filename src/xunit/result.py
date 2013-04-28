#! python

import unittest
import logging

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
		super(unittest.runner.TextTestResult,self).__init__(None,'',0)
		return

	def startTest(self, test):
		return

	def addSuccess(self, test):
		self.__succs += 1
		self.__cases += 1
		return

	def addError(self, test, err):
		self.__fails += 1
		self.__cases += 1
		return

	def addFailure(self, test, err):
		self.__fails += 1
		self.__cases += 1
		return
	

	def addSkip(self, test, reason):
		self.__skips += 1
		self.__cases += 1
		return

	def addExpectedFailure(self, test, err):
		self.__unexpectfails += 1
		self.__cases += 1
		return

	def addUnexpectedSuccess(self, test):
		self.__unexpectsuccs += 1
		self.__cases += 1
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

