#! python

import logging
import xunit.utils.cls
import xunit.config
import sys


MAX_CASE_LEN = 50
MAX_CASE_NAME_LEN = 30
class BaseLogger:
	def __init__(self,cn):
		self.__logger = logging.getLogger(cn)
		self.__logger.setLevel(logging.INFO)
		formatter = logging.Formatter("[%(filename)-10s:%:%(lineno)-5s] %(message)s")
		fh = logging.StreamHandler(None)
		fh.setFormatter(formatter)
		self.__logger.addHandler(fh)
		self.__caselen = 0
	
	def Info(self,msg):
		self.__logger.info(msg)

	def Warn(self,msg):
		self.__logger.warning(msg)

	def Error(self,msg):
		self.__logger.error(msg)

	def Debug(self,msg):
		self.__logger.debug(msg)

	def TestStart(self,msg):
		self.__caselen = 0
		return

	def CaseStart(self,msg):
		_msg = msg
		if self.__caselen > 0:
			for i in xrange(0,self.__caselen):
				sys.stdout.write('\b')
		self.__caselen = 0
		if len(_msg) > MAX_CASE_NAME_LEN:
			_tmp = '['
			_tmp += _msg[:MAX_CASE_NAME_LEN]
			_msg = _tmp
		else:
			cnt = MAX_CASE_NAME_LEN - len(_msg)
			_tmp = '['
			_tmp += ' ' * cnt
			_tmp += _msg
			_msg =_tmp 
		sys.stdout.write('%s'%(_msg))
		sys.stdout.flush()
		self.__caselen = len(_msg)
		return

	def CaseFail(self,msg):
		_msg = msg
		if len(_msg) > (MAX_CASE_LEN - MAX_CASE_NAME_LEN):
			_tmp = '\t'
			_tmp += _msg[:(MAX_CASE_LEN - MAX_CASE_NAME_LEN)]
			_msg = _tmp
		else:
			cnt =MAX_CASE_LEN - MAX_CASE_NAME_LEN - len(_msg)
			_tmp = '\t'
			_tmp += ' '*cnt
			_tmp += _msg
			_msg = _tmp
			
		sys.stdout.write('%s'%(_msg))
		sys.stdout.flush()
		self.__caselen += len(_msg)
		return

	def CaseError(self,msg):
		_msg = msg
		if len(_msg) > (MAX_CASE_LEN - MAX_CASE_NAME_LEN):
			_tmp = '\t'
			_tmp += _msg[:(MAX_CASE_LEN - MAX_CASE_NAME_LEN)]
			_msg = _tmp
		else:
			cnt =MAX_CASE_LEN - MAX_CASE_NAME_LEN - len(_msg)
			_tmp = '\t'
			_tmp += ' '*cnt
			_tmp += _msg
			_msg = _tmp
		sys.stdout.write('%s'%(_msg))
		sys.stdout.flush()
		self.__caselen += len(_msg)
		return

	def CaseSucc(self,msg):
		_msg = msg
		if len(_msg) > (MAX_CASE_LEN - MAX_CASE_NAME_LEN):
			_tmp = '\t'
			_tmp += _msg[:(MAX_CASE_LEN - MAX_CASE_NAME_LEN)]
			_msg = _tmp
		else:
			cnt =MAX_CASE_LEN - MAX_CASE_NAME_LEN - len(_msg)
			_tmp = '\t'
			_tmp += ' '*cnt
			_tmp += _msg
			_msg = _tmp
		sys.stdout.write('%s'%(_msg))
		sys.stdout.flush()
		self.__caselen += len(_msg)
		return
	def CaseSkip(self,msg):
		_msg = msg
		if len(_msg) > (MAX_CASE_LEN - MAX_CASE_NAME_LEN):
			_tmp = '\t'
			_tmp += _msg[:(MAX_CASE_LEN - MAX_CASE_NAME_LEN)]
			_msg = _tmp
		else:
			cnt =MAX_CASE_LEN - MAX_CASE_NAME_LEN - len(_msg)
			_tmp = '\t'
			_tmp += ' '*cnt
			_tmp += _msg
			_msg = _tmp
		sys.stdout.write('%s'%(_msg))
		sys.stdout.flush()
		self.__caselen += len(_msg)
		return
	def CaseEnd(self,msg):
		sys.stdout.write(']')
		sys.stdout.flush()
		self.__caselen += 1
		return

	def TestEnd(self,msg):
		sys.stdout.write('\n%s\n'%(msg))
		self.__caselen = 0
		return

	def __xmltagstart(self,logger,tag,**kattrs):
		pass

	def __xmltagend(self,logger,tag):
		pass

	def __xmltagvalue(self,logger,tag,value):
		pass

	def __directmsg(self,logger,msg):
		pass




_logger_instances = {}

def singleton(cls):
	def get_instance():
		ccn = xunit.utils.cls.GetCallerClassName(2)
 		if ccn not in _logger_instances  :
 			_logger_instances[ccn] = cls(ccn)
 		return _logger_instances[ccn]
	return get_instance


def singletonbyargs(class_):
	def getinstance(*args, **kwargs):
		pn = args[0]
		tn =  pn
		if tn not in _logger_instances:
			_logger_instances[tn] = class_(*args, **kwargs)
		return _logger_instances[tn]
	return getinstance	
	

@singleton
class AdvLogger(BaseLogger):
	pass

@singletonbyargs
class ClassLogger(BaseLogger):
	pass
