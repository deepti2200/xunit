#! pthon

import unittest

import LocalException

class LoadModuleError(LocalException.LocalException):
	pass


class TestCaseLoader(unittest.TestSuite):
	def LoadCase(self,casestrstr):
		pass 
	def __LoadCase(self,mn,cn,fn=None):
		rst = unittest.TestSuite()
		try:
			m = __import__(mn)
			cls = getattr(m,cn)
			if fn:
				rst.addTest(cls(fn))
			else:
				tests = unittest.loader.loadTestsFromTestCase(cls)
				rst.addTest(tests)
		except:
			raise LoadModuleError('can not load [%s].%s:%s module'%(mn,cn,fn))
		return rst


