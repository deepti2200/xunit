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

if __name__== '__main__':
	RunTests(sys.argv[1:])