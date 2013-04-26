#! python
import inspect
import types
import logging
def FuncMethodSearh(obj):
	if inspect.ismethod(obj):
		return True
	if inspect.isfunction(obj):
		return True
	if inspect.isclass(obj):
		return True
	return False


def __IsCodeInClass(clsobj,codeobj):
	mns = inspect.getmembers(clsobj,predicate=FuncMethodSearh)
	ret = 0
	for m in mns:
		#logging.info('%s %s'%(repr(m[1]),repr(codeobj)))
		if type(m[1]) is types.MethodType or type(m[1]) is types.FunctionType or\
		  type(m[1]) is types.GeneratorType:
			fobj = m[1].func_code
			if fobj.co_name == codeobj.co_name  and \
			fobj.co_firstlineno == codeobj.co_firstlineno:
				ret = 1
				break
	return ret

def __GetCodeObjClass(clsobj,codeobj,calllevel=0):
	if calllevel > 300:
		raise 
	ret = __IsCodeInClass(clsobj,codeobj)
	if ret > 0:
		return clsobj.__name__
	mns = inspect.getmembers(clsobj,predicate=inspect.isclass)
	for m in mns:
		# we do not recursive for the two  types
		if m[0] != '__class__' and m[0] != '__base__':
			#logging.info('%s %s'%(repr(m[1]),repr(codeobj)))
			n = __GetCodeObjClass(m[1],codeobj,calllevel + 1)
			if n:
				return clsobj.__name__+'.'+n
	return None

def GetCallerClassFullName(modobj,codeobj):
	'''
		@modobj : module object area to search for code object
		@codeobj : code object will find its class belong to

		@return : it codeobj can not detect the name return module name
		              if codeobj is the function not belong to any of the class 
		              return the module name
		              if codeobj is the method or function of class ,return whole class name including module name 
	'''
	mns = inspect.getmembers(modobj,predicate=FuncMethodSearh)
	ret = 0
	for m in mns:
		if type(m[1]) is types.MethodType or type(m[1]) is types.FunctionType or\
		  type(m[1]) is types.GeneratorType:
			fobj = m[1].func_code
			if fobj.co_name == codeobj.co_name  and \
			fobj.co_firstlineno == codeobj.co_firstlineno:
				ret = 1
				break
	if ret > 0:
		return modobj.__name__

	mns = inspect.getmembers(modobj,predicate=inspect.isclass)
	for m in mns:
		n = __GetCodeObjClass(m[1],codeobj)
		if n:
			return modobj.__name__ +'.'+n
	return modobj.__name__
	
def GetCallerClassName(level=2):
	mn = ''
	stks = inspect.stack()
	if len(stks) > level:
		frm = stks[level]
		mm = inspect.getmodule(frm[0])
		fc = frm[0].f_code
		mn = GetCallerClassFullName(mm,fc)
	return mn


def __IsClassSame(clsroot,clsobj):
	if clsroot == clsobj:
		return 1
	else:
		return 0

def __GetClassName(clsroot,clsobj,level=0):
	if level > 300:
		raise Exception('class object %s'%(repr(clsobj)))
	if __IsClassSame(clsroot,clsobj):
		return clsroot.__name__
	mns = inspect.getmembers(clsroot,predicate=inspect.isclass)
	for m in mns:
		if m[0] != '__class__' and m[0] != '__base__':
			n = __GetClassName(m[1],clsobj,level+1)
			if n:
				return clsroot.__name__ + '.' + n
	return None
	
def __GetFullClassName(modobj,clsobj,level=0,modsearch=[]):
	#mns = inspect.getmembers(modobj,predicate=inspect.isclass)
	if level > 300:
		raise Exception('modobj %s clsobj %s'%(repr(modobj),repr(clsobj)))
	mns = inspect.getmembers(modobj,predicate=None)
	#logging.info('%s'%(repr(mns)))
	for m in mns:
		if inspect.isclass(m[1]):
			n = __GetClassName(m[1],clsobj,level+1)
			if n:
				return modobj.__name__ + '.' + n
		elif inspect.ismodule(m[1]):
			if m[0] not in modsearch:
				modsearch.append(m[0])
	 			n = __GetFullClassName(m[1],clsobj,level+1,modsearch)
	 			if n:
					return  n
	return None
	

def GetClassName(obj):
	cn = ''
	if inspect	.isclass(obj):
		m = __import__(obj.__module__)
		cn = __GetFullClassName(m,obj)
		if cn is None:
			cn = obj.__module__ +'.'+obj.__name__
	return cn
