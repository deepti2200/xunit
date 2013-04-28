#! python

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','src')))
sys.path.append((os.path.dirname(os.path.abspath(__file__))))

import xunit.result
import xunit.suite
import xunit.case
import unittest
import logging


class XUnitTested(xunit.case.XUnitCase):
	def test_case1(self):
		pass

	def test_casefail(self):
		self.assertEqual(1,0)
		return

	@unittest.skip("must skiped")
	def test_skip(self):
		return

	@unittest.expectedFailure
	def test_succwhenexpectfail(self):
		return
	


class XUnitTestResult(xunit.case.XUnitCase):
	def test_result(self):
		sbase = xunit.suite.XUnitSuiteBase()
		# now for the name of current case
		mn = self.__module__
		cn = 'XUnitTested'
		sbase.LoadCase(mn +'.'+cn)

		_res = xunit.result.XUnitResultBase()

		for s in sbase:
			logging.info('%s'%(s))
			s(_res)
			logging.info('cases %d succ %d fail %d skip %d UnexpectFails %d  UnexpectSuccs %d '%(_res.Cases(),_res.Succs(),_res.Fails(),_res.Skips(),_res.UnexpectFails(),_res.UnexpectSuccs()))

		logging.info('cases %d succ %d fail %d skip %d UnexpectFails %d  UnexpectSuccs %d '%(_res.Cases(),_res.Succs(),_res.Fails(),_res.Skips(),_res.UnexpectFails(),_res.UnexpectSuccs()))
		return


def MainTest():
	verb = 1
	ff = False
	if '-v' in sys.argv[1:] or '--verbose' in sys.argv[1:]:
		logging.basicConfig(level=logging.INFO,format="%(levelname)-8s [%(filename)-10s:%(funcName)-20s:%(lineno)-5s] %(message)s")
		verb = 2
	if '-f' in sys.argv[1:] or '--failfast' in sys.argv[1:]:
		ff = True
	suites = xunit.suite.XUnitSuiteBase()
	suites.LoadCase('__main__.XUnitTestResult')

	unittest.TextTestRunner(sys.stderr,descriptions=True, verbosity=verb ,failfast=ff, buffer=False, resultclass=None).run(suites)
	return

if __name__ == '__main__':
	MainTest()


