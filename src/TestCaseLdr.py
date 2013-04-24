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
				tests = unittest.loader().loadTestsFromTestCase(cls)
				rst.addTest(tests)
		except:
			raise LoadModuleError('can not load [%s].%s:%s module'%(mn,cn,fn))
		return rst


	def LoadCase(self,case):
		'''
			case is in the format like module.class:function
			module is the module name
			class is the class name in the modulef
			function is the function name 
		'''
		mcname = case
		fn = None
		if ':' in case:
			mcname,fn = case.split(':')

		kpart = mcname
		rst = None
		while len(kpart) > 0:
			r = kpart.rfind('.')
			mn = mcname[:r]
			cn = mcnam[r+1:]
			try:
				rst = self.__LoadCase(mn,cn,fn)
			except LoadModuleError as e :
				kpart = mn

		if rst is None:
			raise LoadModuleError('can not load %s'%(case))
		self.addTests(rst)
		return

	