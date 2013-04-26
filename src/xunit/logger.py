#! python

import logging
import xunit.utils.cls

class BaseLogger:
	def __init__(self,cn):
		pass



_instances = {}

def singleton(cls):
	def get_instance():
		ccn = xunit.utils.cls.GetCallerClassName(2)
		cn = xunit.utils.cls.GetClassName(cls)
		tn =  cn+':'+ ccn
 		if tn not in _instances  :
 			_instances[tn] = cls(cn)
 		return _instances[tn]
	return get_instance


@singleton
class AdvLogger(BaseLogger):
	pass
