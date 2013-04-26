#! python

import logging
import clsname

class BaseLogger:
	def __init__(self,cn):
		pass



_instances = {}

def singleton(cls):
	def get_instance():
		ccn = clsname.GetCallerClassName(2)
		cn = clsname.GetClassName(cls)
		tn =  cn+':'+ ccn
 		if tn not in _instances  :
 			_instances[tn] = cls(cn)
 		return _instances[tn]
	return get_instance


@singleton
class AdvLogger(BaseLogger):
	pass
