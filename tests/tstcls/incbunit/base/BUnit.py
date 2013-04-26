

import clsname

class BUnit(object):
	def GetMsg(self):
		return clsname.GetCallerClassName(1)
	class BUnit2(object):
		def GetMsg(self):
			return clsname.GetCallerClassName(1) 
		class BUnit3(object):
			def GetMsg(self):
				return clsname.GetCallerClassName(1) 
			class BUnit(object):
				def GetMsg(self):
					return clsname.GetCallerClassName(1) 
	
