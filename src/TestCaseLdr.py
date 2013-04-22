#! pthon

import unittest

def LoadSuite(st,mn,cn,fn=None):
	rst = None
	try:
		m = __import__(mn)
		cls = getattr(m,cn)
		if fn :
			if st:
				st.addTest(cls(fn))
			else:
 				rst = unittest.TestSuite()
 				rst.addTest(cls(fn))
 		else:
			tests = unittest.loader.loadTestsFromTestCase(cls)
			if st:
				st.addTests(tests)
			else:
 				rst = unittest.TestSuite()
 				rst.addTests(tests)
		
	except:
		raise LocalException.LocalException('can not load [%s].%s function %s'%(mn,cn,fn))

