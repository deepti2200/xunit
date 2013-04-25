#! python

import unittest
import sys
import os
from optparse import OptionParser
sys.path.append((len(os.path.dirname(__file__))>0 and os.path.dirname(__file__) or '.' )+os.sep+'..'+os.sep+'..'+os.sep+'src'+os.sep)
sys.path.append((len(os.path.dirname(__file__))>0 and os.path.dirname(__file__) or '.' ))
import TestCaseLdr

def suite(args):
	ldr = TestCaseLdr.TestCaseLoaderBase()
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