#! python

import unittest
import sys
import os
from optparse import OptionParser
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','src')))
sys.path.append((os.path.dirname(os.path.abspath(__file__))))
import xunit.suite

def suite(args):
	ldr = xunit.suite.XUnitSuiteBase()
	for a in args:
		ldr.LoadCase(a)
	return ldr

def RunTests(args):
	st = suite(args)
	unittest.TextTestRunner().run(st)

def Usage(opt,ec,msg=None):
	fp = sys.stderr
	if ec == 0:
		fp = stdout
	if msg:
		fp.write('%s\n'%(msg))
	opt.print_help(fp)
	sys.exit(ec)

if __name__== '__main__':
	parser = OptionParser(usage="usage:%s [OPTIONS] testcases..."%(os.path.basename(__file__)))
	parser.add_option('-p','--path',action="append",dest="paths",help="to add the path to search")
	(options,nargs) = parser.parse_args()
	if nargs is None or len(nargs) < 1:
 		Usage(parser,3,"Need at least one testcase")	
 	if options.paths and len(options.paths) > 0:
		for p in options.paths:
			if p not in sys.path:
				sys.path.append(p)
	RunTests(nargs)
