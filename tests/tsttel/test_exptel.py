#! python
import logging
import sys
import os
import unittest
import socket
from optparse import OptionParser
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','src')))

from xunit.utils import exptel
import xunit.case
import xunit.config
import re
import xunit.suite
import xunit.result

from xunit.logger import ClassLogger

import random
import time


CharacterUse='abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789'

class ExpTelUnitCase(xunit.case.XUnitCase):
	def XUnitsetUp(self):
		utcfg = xunit.config.XUnitConfig()
		host = utcfg.GetValue('.telnet','host','')
		port = utcfg.GetValue('.telnet','port','23')
		user = utcfg.GetValue('.telnet','username',None)
		password = utcfg.GetValue('.telnet','password',None)
		loginnote = utcfg.GetValue('.telnet','loginnote','login:')
		passwordnote = utcfg.GetValue('.telnet','passwordnote','assword:')
		cmdnote = utcfg.GetValue('.telnet','cmdnote','# ')
		timeout = utcfg.GetValue('.telnet','timeout','5')
		port = int(port)
		timeout = int(timeout)
		
		self.__stream = None
		logclass = utcfg.GetValue('.telnet','logclass','none')
		if logclass == 'stdout' :
			self.__stream = sys.stdout
		elif logclass == 'stderr':
			self.__stream = sys.stderr
		elif logclass.lower() == 'none':
			self.__stream = None
		else:
			self.__stream = ClassLogger(logclass)
		self.__tel = exptel.XUnitTelnet(host,port,user,password,self.__stream,timeout,loginnote,passwordnote,cmdnote)		
		return 


	def XUnittearDown(self):
		if self.__tel:
			del self.__tel
			self.__tel = None
		self.__stream = None
		return
	def test_telnethostok(self):
		return

	def test_matchecho(self):
		cmd = 'echo "hello world"'
		match,rval = self.__tel.Execute(cmd,2)
		self.assertEqual(match,1)
		vpat = re.compile('hello')
		self.assertTrue(vpat.search(rval))
		vpat = re.compile('world')
		self.assertTrue(vpat.search(rval))
		vpat = re.compile('echo')
		self.assertFalse(vpat.search(rval))
		return

	def test_timeouterror(self):
		cmd = 'sleep 10'
		ok = 1
		try:
			match = self.__tel.Execute(cmd)
		except exptel.HostCmdTimeoutError:
			ok = 0
		self.assertEqual(ok,0)
		return
	def test_connectrefused(self):
		lip = socket.gethostbyname(socket.gethostname())
		vpat = re.compile('^192\.')
		# we assume that in the 10.0 subnet
		cip = '192.168.0.3'
		if vpat.search(lip):
			# we are now in 192.168. subnet
			cip = '10.0.6.89'
		ok = 1
		tel = None
		try:
			host = cip
			port = 23
			user = 'root'
			password = 'password'
			stream = None
			tel = exptel.XUnitTelnet(host,port,user,password,stream)
		except exptel.HostRefusedError:
			ok = 0
		self.assertEqual(ok,0)
		
		return
		
		
	def test_writelog(self):
		# first to close the code file
		if self.__tel:
			del self.__tel
		self.__tel = None
		self.__stream = None
		# now to test for the job
		random.seed(time.time())
		fname = ''
		flen = random.randint(10,20)
		clen = len(CharacterUse)
		clen -= 1
		for i in xrange(flen):
			fname += CharacterUse[random.randint(0,clen)]
		fname += '.log'
		self.__stream = open(fname,'w+b')
		utcfg = xunit.config.XUnitConfig()
		host = utcfg.GetValue('.telnet','host','')
		port = utcfg.GetValue('.telnet','port','23')
		user = utcfg.GetValue('.telnet','username',None)
		password = utcfg.GetValue('.telnet','password',None)
		timeout = utcfg.GetValue('.telnet','timeout','5')
		loginnote = utcfg.GetValue('.telnet','loginnote','login:')
		passwordnote = utcfg.GetValue('.telnet','passwordnote','assword:')
		cmdnote = utcfg.GetValue('.telnet','cmdnote','# ')
		port =int(port)
		timeout=int(timeout)
		self.__tel = exptel.XUnitTelnet(host,port,user,password,self.__stream,timeout,loginnote,passwordnote,cmdnote)
		# now we should 
		slen = random.randint(20,50)
		clen = len(CharacterUse)
		clen -= 1
		s = ''
		for i in xrange(slen):
			s += CharacterUse[random.randint(0,clen)]

		cmd = 'echo "%s"'%(s)
		ret ,sret = self.__tel.Execute(cmd)
		self.assertEqual(ret,1)
		vpat = re.compile(s)
		self.assertTrue(vpat.search(sret))
		self.__stream.flush()
		# now to open the file
		fh = open(fname,'r+b')
		matched = 0
		for l in fh:
			if vpat.search(l):
				matched = 1
				break
		self.assertEqual(matched,1)
		del self.__tel
		self.__tel = None		
		self.__stream.close()
		self.__stream = None
		del fh
		fh = None
		# now to remove the file
		os.remove(fname)
		# now to make the 
		return

		
		


def maintest(cfname,variables=[]):
	sbase = xunit.suite.XUnitSuiteBase()
	# now for the name of current case
	mn = '__main__'
	cn = 'ExpTelUnitCase'
	sbase.LoadCase(mn +'.'+cn)
	utcfg.SetValue('build','topdir',os.path.dirname(os.path.abspath(__file__)))
	utcfg.LoadFile(cfname)
	
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
	args.add_option('-H','--host',action='store',dest='host',nargs=1,help='specify the host')
	args.add_option('-p','--port',action='store',dest='port',nargs=1,help='specify the port default is 23')
	args.add_option('-u','--user',action='store',dest='user',nargs=1,help='specify username')
	args.add_option('-P','--pass',action='store',dest='password',nargs=1,help='specify password')
	args.add_option('-l','--login',action='store',dest='loginnote',nargs=1,help='login note default is (login:)')
	args.add_option('-e','--passnote',action='store',dest='passwordnote',nargs=1,help='password note default is (assword:)')
	args.add_option('-c','--cmdnote',action='store',dest='cmdnote',nargs=1,help='cmd note default is (# )')
	args.add_option('-t','--timeout',action='store',dest='timeout',nargs=1,help='set timeout value default is 5')
	args.add_option('-x','--xmllog',action='store',dest='xmllog',nargs=1,help='set xml log')
	options ,nargs = args.parse_args(sys.argv[1:])
	if options.verbose:
		verb = 1
	if options.failfast:
		ff = True
	if options.host:
		utcfg.SetValue('.telnet','host',options.host,1)
	if options.port:
		utcfg.SetValue('.telnet','port',options.port,1)
	if options.user:
		utcfg.SetValue('.telnet','username',options.user,1)
	if options.password:
		utcfg.SetValue('.telnet','password',options.password,1)

	if options.loginnote:
		utcfg.SetValue('.telnet','loginnote',options.loginnote,1)
	if options.passwordnote:
		utcfg.SetValue('.telnet','passwordnote',options.passwordnote,1)
	if options.cmdnote:
		utcfg.SetValue('.telnet','cmdnote',options.cmdnote,1)
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

	if options.xmllog:
		utcfg.SetValue('global','xmllog',options.xmllog,1)
	
	maintest()
	
