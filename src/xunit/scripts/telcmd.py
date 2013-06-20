#! python

#####################
#    this is the command for running the most
#    it  will depend on the exptel
#
#####################

import os
import sys
import time
from optparse import OptionParser
import logging
import re
__abdir=os.path.dirname(os.path.abspath(__file__))
__xunitdir=os.path.join(__abdir,'..','..')
sys.path.append(os.path.abspath(__xunitdir))
import xunit.utils.exptel
import xunit.config
import xunit.extlib.cfgexptel

def RunCmd(cmd,timeout=0):
	ret = 0
	cfgtel = None
	try:
		ctime=time.time()
		etime = ctime + timeout
		cfgtel = xunit.extlib.cfgexptel.CfgExpTel()
		cfgtel.Login()
		logging.info('cmd (%s)\n'%(cmd))
		cfgtel.WriteLine(cmd)
		totr=''
		finished = 0
		rlen = 0
		logging.info('\n')
		while True:
			ctime = time.time()
			if timeout != 0 and ctime < etime:
				break
			rbuf,ps1 = cfgtel.ReadImmediate()
			if len(rbuf) == 0:
				# if we do not read any more ,so sleep for a while
				time.sleep(0.1)
				continue
			endpat = re.compile(ps1)
			rlen += len(rbuf)
			logging.info('read %d'%(rlen))
			totr += rbuf
			if endpat.search(totr):
				# finished
				finished = 1
				break
			ps1len = len(ps1)
			if len(totr) > ps1len:
				# we reserved 8192 bytes
				totr = totr[-ps1len:]
		if finished != 1:
			# not finished ,so just timeout
			ret = -2
	except:
		logging.info('\n')
		ret = -1
	if cfgtel:
		cfgtel.Logout()
		del cfgtel 
	cfgtel = None
	logging.info('ret %d\n'%(ret))
	return ret 
def Usage(opt,ec,msg=None):
	fp = sys.stderr
	if ec == 0:
		fp = sys.stdout
	if msg :
		fp.write('%s\n'%(msg))
	opt.print_help(fp)
	sys.exit(ec)


def main():
	args = OptionParser('%s [OPTIONS] command...'%(os.path.basename(__file__)))
	args.add_option('-c','--config',action='store',dest='cfg',nargs=1,default=None,help='specify config')
	args.add_option('-t','--timeout',action='store',dest='timeout',nargs=1,default=0,help='specify timeout of running command')
	args.add_option('-v','--verbose',action='store_true',dest='verbose',default=False,help='verbose mode')
	options,nargs = args.parse_args(sys.argv[1:])
	if len(nargs) < 1:
		Usage(args,3,'please specify  command...')
	cmd = nargs[0] 
	if options.verbose:
		logging.basicConfig(level=logging.INFO,format="%(levelname)-8s [%(filename)-10s:%(funcName)-20s:%(lineno)-5s] %(message)s")	
	if len(nargs) > 1:
		cmd = ' '.join(nargs)
	if options.cfg is None:
		Usage(args,3,'please set config')
	utcfg = xunit.config.XUnitConfig()
	utcfg.LoadFile(options.cfg)
	timeout = int(options.timeout)
	ret = RunCmd(cmd,timeout)
	sys.exit(ret)


if __name__ == '__main__':
	main()
