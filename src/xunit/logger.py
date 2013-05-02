#! python

import logging
import xunit.utils.cls
import xunit.config
import sys
import StringIO
import inspect


CRITICAL_LEVEL=1
ERROR_LEVEL=2
WARNING_LEVEL=3
INFO_LEVEL=4
DEBUG_LEVEL=5

def DebugString(msg,level=1):
	_f = inspect.stack()[level]
	_msg = '[%s:%s] %s'%(_f[1],_f[2],msg)
	sys.stderr.write(_msg+'\n')

def DebugString2(msg,level=1):
	_msg = '%s'%(msg)
	sys.stderr.write(_msg+'\n')


MAX_CASE_LEN = 70
MAX_CASE_NAME_LEN = 55
class BaseLogger:
	def __init__(self,cn):
		'''
		    init the logger ,and we do this by the string 
		    input
		    @cn class name of logger get
		'''
		self.__strio = None
		self.__level = WARNING_LEVEL
		self.__output = 1
		self.__ResetStrLogger()
		

	def __ResetStrLogger(self):
		if self.__strio :
			self.__strio.close()
			del self.__strio
			self.__strio = None

		# now to set the logger format
		try:
			# this will call error on delete function call sequence
			self.__strio = StringIO.StringIO()
		except:
			pass
		self.__caselen = 0
		return


	def __del__(self):
		#DebugString2('delete %s'%(repr(self)))
		self.Flush()
		del self.__strio
		self.__strio = None
		return

	def SetLevel(self,level=WARNING_LEVEL):
		oldlevel = self.__level
		self.__level = level
		return oldlevel
	def SetOutput(self,output=1):
		oldoutput = self.__output
		self.__output = output
		return oldoutput
	
	def Info(self,msg):
		if self.__level >= INFO_LEVEL:
			_f = inspect.stack()[1]
			_msg = '[%s:%s] %s\n'%(_f[1],_f[2],msg)
			self.__strio.write(_msg)

	def Warn(self,msg):
		if self.__level >= WARNING_LEVEL:
			_f = inspect.stack()[1]
			_msg = '[%s:%s] %s\n'%(_f[1],_f[2],msg)
			self.__strio.write(_msg)

	def Error(self,msg):
		if self.__level >= ERROR_LEVEL:
			_f = inspect.stack()[1]
			_msg = '[%s:%s] %s\n'%(_f[1],_f[2],msg)
			self.__strio.write(_msg)

	def Debug(self,msg):
		if self.__level >= DEBUG_LEVEL:
			_f = inspect.stack()[1]
			_msg = '[%s:%s] %s\n'%(_f[1],_f[2],msg)
			self.__strio.write(_msg)

	def Flush(self):
		value = None
		if self.__strio :
			try:
				value = self.__strio.getvalue()
				if self.__output > 0:
					sys.stdout.write(value)
			except TypeError:
				value = None
			self.__ResetStrLogger()
		return value

	def TestStart(self,msg):
		self.__caselen = 0
		return

	def CaseStart(self,msg):
		_msg = msg
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
		sys.stdout.write(']\n')
		sys.stdout.flush()
		self.__caselen += 2
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
	def get_instance(*args, **kwargs):
		ccn = xunit.utils.cls.GetCallerClassName(2)
 		if ccn not in _logger_instances  :
 			_logger_instances[ccn] = cls(ccn,*args, **kwargs)
			#DebugString('caller %s %s\n'%(ccn,repr(_logger_instances[ccn])))
 		return _logger_instances[ccn]
	return get_instance


def singletonbyargs(class_):
	def getinstance(*args, **kwargs):
		pn = args[0]
		tn =  pn
		if tn not in _logger_instances:			
			_logger_instances[tn] = class_(*args, **kwargs)
			#DebugString('caller %s %s\n'%(tn,repr(_logger_instances[tn])))
		return _logger_instances[tn]
	return getinstance	
	

@singleton
class AdvLogger(BaseLogger):
	pass

@singletonbyargs
class ClassLogger(BaseLogger):
	pass
