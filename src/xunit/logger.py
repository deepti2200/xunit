#! python

import logging
import xunit.utils.cls
import xunit.config
import sys
import StringIO
import inspect
import atexit


from xunit.utils import exception

class NotDefinedClassMethodException(exception.XUnitException):
	pass

CRITICAL_LEVEL=1
ERROR_LEVEL=2
WARNING_LEVEL=3
INFO_LEVEL=4
DEBUG_LEVEL=5

def DebugString(msg,level=1):
	_f = inspect.stack()[level]
	_msg = '[%s:%s] %s'%(_f[1],_f[2],msg)
	sys.stderr.write(_msg+'\n')


MAX_CASE_LEN = 70
MAX_CASE_NAME_LEN = 55


class AbstractLogger:
	def __init__(self,cn):
		pass

	def __del__(self):
		pass

	def SetLevel(self,level=WARNING_LEVEL):
		raise NotDefinedClassMethodException('not defined SetLevel')
	def SetOutput(self,output=1):
		raise NotDefinedClassMethodException('not defined SetOutput')	
	def Info(self,msg):
		raise NotDefinedClassMethodException('not defined Info')
	def Warn(self,msg):
		raise NotDefinedClassMethodException('not defined Warn')
	def Error(self,msg):
		raise NotDefinedClassMethodException('not defined Error')
	def Debug(self,msg):
		raise NotDefinedClassMethodException('not defined Debug')
	def Flush(self):
		raise NotDefinedClassMethodException('not defined Flush')
	def TestStart(self,msg):
		raise NotDefinedClassMethodException('not defined TestStart')
	def CaseStart(self,msg):
		raise NotDefinedClassMethodException('not defined CaseStart')
	def CaseFail(self,msg):
		raise NotDefinedClassMethodException('not defined CaseFail')
	def CaseError(self,msg):
		raise NotDefinedClassMethodException('not defined CaseError')
	def CaseSucc(self,msg):
		raise NotDefinedClassMethodException('not defined CaseSucc')
	def CaseSkip(self,msg):
		raise NotDefinedClassMethodException('not defined CaseSkip')
	def CaseEnd(self,msg):
		raise NotDefinedClassMethodException('not defined CaseEnd')
	def TestEnd(self,msg):
		raise NotDefinedClassMethodException('not defined TestEnd')
	def write(self,msg):
		raise NotDefinedClassMethodException('not defined write')
	def flush(self):
		raise NotDefinedClassMethodException('not defined flush')

class BaseLogger(AbstractLogger):
	def __init__(self,cn):
		'''
		    init the logger ,and we do this by the string 
		    input
		    @cn class name of logger get
		'''
		self.__strio = None
		self.__level = WARNING_LEVEL
		self.__output = 1
		self.__outfh = sys.stdout
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

	def __flush(self):
		v = ''
		if self.__strio:
			v = self.__strio.getvalue()
			if len(v) > 0 and self.__output > 0:
				self.__outfh.write(v)
			if len(v) == 0:
				v = ''
		return v

	def __del__(self):
		self.__flush()
		del self.__strio
		self.__strio = None
		self.__outfh = None
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
		value = ''
		if self.__strio :
			value = self.__flush()
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
		self.__outfh.write('%s'%(_msg))
		self.__outfh.flush()
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
			
		self.__outfh.write('%s'%(_msg))
		self.__outfh.flush()
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
		self.__outfh.write('%s'%(_msg))
		self.__outfh.flush()
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
		self.__outfh.write('%s'%(_msg))
		self.__outfh.flush()
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
		self.__outfh.write('%s'%(_msg))
		self.__outfh.flush()
		self.__caselen += len(_msg)
		return
	def CaseEnd(self,msg):
		self.__outfh.write(']\n')
		self.__outfh.flush()
		self.__caselen += 2
		return

	def TestEnd(self,msg):
		self.__outfh.write('\n%s\n'%(msg))
		self.__caselen = 0
		return

	def write(self,msg):
		if self.__level >= INFO_LEVEL:
			self.__strio.write(msg)
		return
	def flush(self):
		return self.Flush()
		


class XmlLogger(AbstractLogger):
	def __init__(self,cn):
		'''
		    init the logger ,and we do this by the string 
		    input
		    @cn class name of logger get
		'''
		self.__strio = None
		self.__level = WARNING_LEVEL
		self.__output = 1
		self.__outfh = sys.stdout
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

	def __flush(self):
		v = ''
		if self.__strio:
			v = self.__strio.getvalue()
			if len(v) > 0 and self.__output > 0:
				self.__outfh.write(v)
			if len(v) == 0:
				v = ''
		return v

	def __del__(self):
		self.__flush()
		del self.__strio
		self.__strio = None
		self.__outfh = None
		return

	def SetLevel(self,level=WARNING_LEVEL):
		raise NotDefinedClassMethodException('not defined SetLevel')
	def SetOutput(self,output=1):
		raise NotDefinedClassMethodException('not defined SetOutput')	
	def Info(self,msg):
		raise NotDefinedClassMethodException('not defined Info')
	def Warn(self,msg):
		raise NotDefinedClassMethodException('not defined Warn')
	def Error(self,msg):
		raise NotDefinedClassMethodException('not defined Error')
	def Debug(self,msg):
		raise NotDefinedClassMethodException('not defined Debug')
	def Flush(self):
		raise NotDefinedClassMethodException('not defined Flush')
	def TestStart(self,msg):
		raise NotDefinedClassMethodException('not defined TestStart')
	def CaseStart(self,msg):
		raise NotDefinedClassMethodException('not defined CaseStart')
	def CaseFail(self,msg):
		raise NotDefinedClassMethodException('not defined CaseFail')
	def CaseError(self,msg):
		raise NotDefinedClassMethodException('not defined CaseError')
	def CaseSucc(self,msg):
		raise NotDefinedClassMethodException('not defined CaseSucc')
	def CaseSkip(self,msg):
		raise NotDefinedClassMethodException('not defined CaseSkip')
	def CaseEnd(self,msg):
		raise NotDefinedClassMethodException('not defined CaseEnd')
	def TestEnd(self,msg):
		raise NotDefinedClassMethodException('not defined TestEnd')
	def write(self,msg):
		raise NotDefinedClassMethodException('not defined write')
	def flush(self):
		raise NotDefinedClassMethodException('not defined flush')
	



class _AdvLogger:
	def __init__(self,cn):
		self.__loggers = []
		self.__loggers.append(BaseLogger(cn))
		return

	def __del__(self):
		while len(self.__loggers) > 0:
			_logger =self.__loggers[0]
			self.__loggers.remove(_logger)
			del _logger
			_logger = None
		return

	def SetLevel(self,level=WARNING_LEVEL):
		l = level
		for _logger in self.__loggers:
			l = _logger.SetLevel(level)
		return l
	def SetOutput(self,output=1):
		o = output
		for _logger in self.__loggers:
			o = _logger.SetOutput(output)
		return o
		
	def Info(self,msg):
		for _logger in self.__loggers:
			_logger.Info(msg)
		return
	def Warn(self,msg):
		for _logger in self.__loggers:
			_logger.Info(msg)
		return
	def Error(self,msg):
		raise NotDefinedClassMethodException('not defined Error')
	def Debug(self,msg):
		raise NotDefinedClassMethodException('not defined Debug')
	def Flush(self):
		raise NotDefinedClassMethodException('not defined Flush')
	def TestStart(self,msg):
		raise NotDefinedClassMethodException('not defined TestStart')
	def CaseStart(self,msg):
		raise NotDefinedClassMethodException('not defined CaseStart')
	def CaseFail(self,msg):
		raise NotDefinedClassMethodException('not defined CaseFail')
	def CaseError(self,msg):
		raise NotDefinedClassMethodException('not defined CaseError')
	def CaseSucc(self,msg):
		raise NotDefinedClassMethodException('not defined CaseSucc')
	def CaseSkip(self,msg):
		raise NotDefinedClassMethodException('not defined CaseSkip')
	def CaseEnd(self,msg):
		raise NotDefinedClassMethodException('not defined CaseEnd')
	def TestEnd(self,msg):
		raise NotDefinedClassMethodException('not defined TestEnd')
	def write(self,msg):
		raise NotDefinedClassMethodException('not defined write')
	def flush(self):
		raise NotDefinedClassMethodException('not defined flush')



class ComBind:
	def __appendClass(self,cls):
		mm = __import__(self.__module__)
		if not hasattr(mm,cls):
			raise Exception('can not get %s'%(cls))
		_cls = getattr(mm,cls)
		self.__clss.append(_cls())
		return
	def __init__(self,*cls):
		self.__clss = []
		for clsn in cls:
			self.__appendClass(clsn)
	def __getattr__(self, name):
		if hasattr(self,name):
			return self.__dict__[name]

		def _missing(*args,**kwargs):
			ret =''
			for c in self.__clss:
				_f = getattr(c,name)
				if len(args) > 0 and len(kwargs.keys())>0:
					ret=_f(args,kwargs)
				elif len(args) > 0:
					ret=_f(args)
				elif len(kwargs.keys()) >0:
					ret=_f(kwargs)
				else:
					ret=_f()
			return ret
		return _missing
	
	


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
	

def logger_cleanup():
	while len(_logger_instances.keys()) > 0:
		k = _logger_instances.keys()[0]
		log1 = _logger_instances[k]
		del log1
		log1 = None
		del _logger_instances[k]
	return

@singleton
class AdvLogger(BaseLogger):
	pass

@singletonbyargs
class ClassLogger(BaseLogger):
	pass

atexit.register(logger_cleanup)
