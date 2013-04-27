

import xunit.utils.cls

class BUnit(object):
	def GetMsg(self):
		return xunit.utils.cls.GetCallerClassName(1)
	class BUnit2(object):
		def GetMsg(self):
			return xunit.utils.cls.GetCallerClassName(1) 
		class BUnit3(object):
			def GetMsg(self):
				return xunit.utils.cls.GetCallerClassName(1) 
			class BUnit(object):
				def GetMsg(self):
					return xunit.utils.cls.GetCallerClassName(1) 
	
