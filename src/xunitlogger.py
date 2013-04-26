#! python

import logging
import clsname

class BaseLogger:
	pass



_instances = {}

def singleton(cls):
	def get_instance():
		ccn = clsname.GetCallerClassName(2)
		cn = clsname.GetClassName(cls)
		tn =  cn+':'+ ccn
 		if tn not in _instances  :
 			_instances[tn] = cls()
 		return _instances[tn]
	return get_instance


@singleton
class AdvLogger(BaseLogger):
	pass
