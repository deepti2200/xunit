#! python

import logging
import sys
import os
import unittest
from optparse import OptionParser
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','src')))
import xunit.suite
import xunit.config
import xunit.result
from xunit import logger 
from xunit import case
from xunit.utils import cls
from xunit.utils import randgen
import re


class TestXmlLogger(case.XUnitCase):
	@classmethod
	def XUnitsetUpClass(cls):
		randgen.InitRandom()
		return
	def XUnitsetUp(self):
		cn = cls.GetClassName(self.__class__)
		sec = '.'+cn
		utcfg = xunit.config.XUnitConfig()
		self._xmlold = utcfg.GetValue(sec,'xmllog','')
		fname = randgen.GenRandomChars(20)
		self.__fname = fname + '.log'
		utcfg.SetValue(sec,'xmllog',self.__fname,1)
		self.__fh = open(self.__fname,'w')
		return

	def XUnittearDown(self):
		if self.__fh :
			self.__fh.close()
			del self.__fh
			self.__fh = None
		if self.__fname and os.path.isfile(self.__fname):
			os.remove(self.__fname)
		self.__fname = None
		utcfg = xunit.config.XUnitConfig()
		if self._xmlold :
			cn = cls.GetClassName(self.__class__)
			sec = '.' + cn 
			utcfg.SetValue(sec,'xmllog',self._xmlold,1)
		self._xmlold = None
		
		return

	def test_xmldebug(self):
		cn = cls.GetClassName(self.__class__)
		xl = logger.XmlLogger(cn,self.__fh)
		xl.SetLevel(logger.DEBUG_LEVEL)
		n = randgen.GenRandomNum(100,1)
		s = randgen.GenRandomChars(n)
		xl.Debug(s)
		vpat = re.compile(s)
		v = xl.Flush()
		self.assertTrue(vpat.search(v))
		vpat = re.compile(cn)
		self.assertTrue(vpat.search(v))
		xl.SetLevel(logger.WARNING_LEVEL)
		n = randgen.GenRandomNum(100,1)
		s = randgen.GenRandomChars(n)
		xl.Debug(s)
		vpat = re.compile(s)
		v = xl.Flush()
		self.assertTrue(v == '')
		return

	def test_xmlfiledebug(self):
		cn = cls.GetClassName(self.__class__)
		xl = logger.XmlLogger(cn,self.__fh)
		xl.SetLevel(logger.DEBUG_LEVEL)
		n = randgen.GenRandomNum(100,1)
		s = randgen.GenRandomChars(n)
		xl.Debug(s)
		vpat = re.compile(s)
		xl.Flush()
		v = ''
		with open(self.__fname) as f:
			sl = f.readlines()
			v = ''.join(sl)
		self.assertTrue(vpat.search(v))
		vpat = re.compile(cn)
		self.assertTrue(vpat.search(v))
		return

	def test_xmlfilewarn(self):
		cn = cls.GetClassName(self.__class__)
		xl = logger.XmlLogger(cn,self.__fh)
		xl.SetLevel(logger.WARNING_LEVEL)
		n = randgen.GenRandomNum(100,1)
		s = randgen.GenRandomChars(n)
		xl.Debug(s)
		vpat = re.compile(s)
		xl.Flush()
		v = ''
		with open(self.__fname,'r+b') as f:
			sl = f.readlines()
			v = ''.join(sl)
		self.assertTrue(v == '')
		return

	
def maintest():
	sbase = xunit.suite.XUnitSuiteBase()
	# now for the name of current case
	mn = '__main__'
	cn = 'TestXmlLogger'
	sbase.LoadCase(mn +'.'+cn)
	utcfg = xunit.config.XUnitConfig()
	_res = xunit.result.XUnitResultBase(1)

	for s in sbase:
		s.run(_res)
		if _res.shouldStop:
			break
	if _res.Fails() != 0 or _res.UnexpectSuccs() !=0:
		sys.exit(3)
	sys.exit(0)


def Usage(opt,ec,msg=None):
	fp = sys.stderr
	if ec == 0:
		fp = sys.stdout
	if msg :
		fp.write('%s\n'%(msg))
	opt.print_help(fp)
	sys.exit(ec)
	
if __name__ == '__main__':
	verb = 0
	ff = False
	utcfg = xunit.config.XUnitConfig()
	args = OptionParser()
	args.add_option('-v','--verbose',action='store_true',dest='verbose',help='verbose mode')
	args.add_option('-f','--failfast',action="store_true",dest="failfast",help="failfast mode")
	options ,nargs = args.parse_args(sys.argv[1:])
	if options.verbose:
		verb = 1
	if options.failfast:
		ff = True

	if verb :
		logging.basicConfig(level=logging.INFO,format="%(levelname)-8s [%(filename)-10s:%(funcName)-20s:%(lineno)-5s] %(message)s")
		utcfg.SetValue('global','debug.mode','y',1)
	else:
		logging.basicConfig(level=logging.WARNING,format="%(levelname)-8s [%(filename)-10s:%(funcName)-20s:%(lineno)-5s] %(message)s")
		utcfg.SetValue('global','debug.mode','n',1)
	if ff:
		utcfg.SetValue('global','failfast','y',1)
	else:
		utcfg.SetValue('global','failfast','n',1)
	
	maintest()
	

