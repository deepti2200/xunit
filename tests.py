#! python

import os
import sys
import logging
from optparse import OptionParser
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),'src'))
import xunit.config
import xunit.suite
import unittest


def Runtest(cfname):
	utcfg = xunit.config.XUnitConfig()
	# now to add the %(build.topdir)s
	utcfg.SetValue('build','topdir',os.path.dirname(os.path.abspath(__file__)))
	utcfg.LoadFile(cfname)

	# now we should get
	units = utcfg.GetUnitTests()
	suites = xunit.suite.XUnitSuiteBase()
	if len(units) > 0:
		for u in units:
			suites.LoadCase(u)

	# now we should set for the case verbose is none we debug our self information
	unittest.TextTestRunner().run(suites)
	return

if __name__ == '__main__':
	if len(sys.argv[1:]) < 1:
		sys.stderr.write('%s config_file'%(os.path.basename(__file__)))
		sys.exit(3)
	Runtest(sys.argv[1])
