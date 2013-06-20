#! python

import os
import re
import xunit.utils.exptel
import xunit.config
import xunit.utils.exception
import logging

class NfsNoMapError(xunit.utils.exception.XUnitException):
	pass

class OpenExportsError(xunit.utils.exception.XUnitException):
	pass

class NotNfsSubDirError(xunit.utils.exception.XUnitException):
	pass


def GetMapDir(curdir):
	# now to get the current
	mapdir = None
	try:
		with open('/etc/exports','r') as f:
			while True:
				l = f.readline()
				if l is None or len(l) == 0:
					break
				l = l.rstrip('\r\n')
				if l.startswith('#'):
					continue
				if len(l) == 0:
					continue
				sarr = l.split()
				if len(sarr) < 2:
					continue
				vpat = re.compile(sarr[0])
				if vpat.search(curdir) :
					if mapdir is None or len(mapdir) < len(sarr[0]):
						mapdir = sarr[0]

			if mapdir is None:
				raise NfsNoMapError('no mapdir in the /etc/exports please used')
			return mapdir
	except:
		raise OpenExportsError('can not parse /etc/exports')
	return None
 
def MapNfsDir(mntdir,mapdir,hostdir):
	'''
		map dir into the remote nfs map
		for example:
		   mntdir /mnt/nfs          in the remote
		   mapdir /home/gmi     in the host
		   and we mount
		   mount -t nfs host:mapdir   mntdir -o nolock
		   we map 
		   /home/gmi/work/git
		   to 
		   /mnt/nfs/work/git
	'''
	restr = '^%s'%(mapdir)
	vpat = re.compile(restr)
	if not vpat.search(hostdir):
		raise NotNfsSubDirError('%s not subdir of %s'%(hostdir,mapdir))
	transdir = hostdir.replace(mapdir,mntdir,1)
	return transdir


