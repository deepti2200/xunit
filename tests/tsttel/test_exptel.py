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

class ExpTelUnitCase(xunit.case.XUnitCase):
	def XUnitsetUp(self):
		utcfg = xunit.config.XUnitConfig()
		host = utcfg.GetValue('global','host','')
		port = utcfg.GetValue('global','port','23')
		user = utcfg.GetValue('global','username',None)
		password = utcfg.GetValue('global','password',None)
		
		port = int(port)
		
		self.__stream = None
		logfile = utcfg.GetValue('global','telnet.logfile','none')
		if logfile == 'stdout' :
			self.__stream = sys.stdout
		elif logfile == 'stderr':
			self.__stream = sys.stderr
		elif logfile.lower() == 'none':
			self.__stream = None
		else:
			self.__stream = open(logfile,'a+b')
		self.__tel = exptel.XUnitTelnet(host,port,user,password,self.__stream)		
		return 


	def XUnittearDown(self):
		if self.__tel:
			del self.__tel
			self.__tel = None
		if self.__stream:
			if self.__stream != sys.stdout and self.__stream != sys.stderr:
				self.__stream.close()
				del self.__stream
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


def maintest():
	sbase = xunit.suite.XUnitSuiteBase()
	# now for the name of current case
	mn = '__main__'
	cn = 'ExpTelUnitCase'
	sbase.LoadCase(mn +'.'+cn)
	utcfg = xunit.config.XUnitConfig()
	_res = xunit.result.XUnitResultBase(1)

	for s in sbase:
		s.run(_res)
		if _res.shouldStop:
			break
	if _res.Fails() != 0 or _res.UnexpectSuccs() !=0:
		logging.error('on fails %d unexpect succs %d'%(_res.Fails() , _res.UnexpectSuccs() ))
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
	options ,nargs = args.parse_args(sys.argv[1:])
	if options.verbose:
		verb = 1
	if options.failfast:
		ff = True
	if options.host:
		utcfg.SetValue('global','host',options.host,1)
	if options.port:
		utcfg.SetValue('global','port',options.port,1)
	if options.user:
		utcfg.SetValue('global','username',options.user,1)
	if options.password:
		utcfg.SetValue('global','password',options.password,1)
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
	
