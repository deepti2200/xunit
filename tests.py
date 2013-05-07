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
	_res = xunit.result.XUnitResultBase()
	for s in suites:
		s(_res)
		if _res.shouldStop:
			break

	_ret = -1
	if _res.Fails() == 0 and _res.UnexpectFails() ==0 and _res.UnexpectSuccs() == 0:
		_ret = 0
	
	return _ret

def Usage(opt,ec,msg=None):
	fp = sys.stderr
	if ec == 0:
		fp = sys.stdout
	if msg :
		fp.write('%s\n'%(msg))
	opt.print_help(fp)
	sys.exit(ec)

if __name__ == '__main__':
	args = OptionParser()
	args.add_option('-v','--verbose',action='store_true',dest='verbose',help='verbose mode')
	args.add_option('-f','--failfast',action="store_true",dest="failfast",help="failfast mode")
	args.add_option('-x','--xmllog',action='store',dest='xmllog',nargs=1,help='set xmllog file default is none')

	options ,nargs = args.parse_args(sys.argv[1:])
	if len (nargs) < 1:
		Usage(args,3,"need one config files")
	utcfg = xunit.config.XUnitConfig()
	
	if options.verbose:
		utcfg.SetValue('global','debug.mode','y',1)
		logging.basicConfig(level=logging.INFO,format="%(levelname)-8s [%(filename)-10s:%(funcName)-20s:%(lineno)-5s] %(message)s")

	if options.failfast:
		utcfg.SetValue('global','failfast','y',1)
	if options.xmllog:
		utcfg.SetValue('global','xmllog',options.xmllog,1)
	_ret = Runtest(nargs[0])
	if _ret != 0:
		sys.exit(3)
	sys.exit(0)
