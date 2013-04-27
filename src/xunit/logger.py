#! python

import logging
import xunit.utils.cls
import xunit.config

class BaseLogger:
	def __init__(self,cn):
		self.__logger = logging.getLogger(cn)
		self.__logger.setLevel(logging.INFO)
		formatter = logging.Formatter("[%(filename)-10s:%:%(lineno)-5s] %(message)s")
		fh = logging.StreamHandler(None)
		fh.setFormatter(formatter)
		self.__logger.addHandler(fh)
	
	def Info(self,msg):
		self.__logger.info(msg)

	def Warn(self,msg):
		self.__logger.warning(msg)

	def Error(self,msg):
		self.__logger.error(msg)

	def Debug(self,msg):
		self.__logger.debug(msg)

	def CaseStart(self,msg):
		sys.stdout.write('[%s'%(msg))

	def CaseFail(self,msg):
		sys.stdout.write('\t%s'%(msg))

	def CaseSucc(self,msg):
		sys.stdout.write('\t%s'%(msg))

	def CaseEnd(self,msg):
		sys.stdout.write(']\n')

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