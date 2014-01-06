#! python

'''
this is the file for alarm info
'''

import struct

import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..')))
import xunit.utils.exception
import xunit.extlib.sdkproto.syscp as syscp

LOGINFO_SIZE=168
LOGINFO_SEARCH_SIZE=84
TYPE_LOGINFO_SEARCH=119
TYPE_LOGINFO=120
TYPE_LOGINFO_INT=121
SYSCODE_GET_LOGINFO_REQ=1227
SYSCODE_GET_LOGINFO_RSP=1228

class LogInfoInvalidError(xunit.utils.exception.XUnitException):
	pass

class LogInfoPackInvalidError(xunit.utils.exception.XUnitException):
	pass


class LogInfoSearchInvalidError(xunit.utils.exception.XUnitException):
	pass

class LogInfoSearchPackInvalidError(xunit.utils.exception.XUnitException):
	pass


class LogInfo:
	def __ResetVar(self):
		self.__majortype = 0
		self.__minortype = 0
		self.__logtime = ''
		self.__logdata = ''
		return
	def __init__(self):
		self.__ResetVar()
		return

	def __del__(self):
		self.__ResetVar()
		return
	def GetString(self,s,size):
		rbuf = ''
		lasti  = -1
		for i in xrange(size):
			if s[i] == '\0':
				lasti = i
				break

		if lasti >= 0:
			rbuf = s[:lasti]
		else:
			rbuf = s[:-2]
		return rbuf

	def ParseBuffer(self,buf):
		if len(buf) < LOGINFO_SIZE:
			raise LogInfoInvalidError('len(%d) < (%d)'%(len(buf),LOGINFO_SIZE))
		self.__majortype,self.__minortype = struct.unpack('>II',buf[:8])
		self.__logtime = self.GetString(buf[8:40],32)
		self.__logdata = self.GetString(buf[40:168],128)
		return buf[LOGINFO_SIZE:]

	def __Format(self):
		rbuf = ''
		rbuf += 'majortype       :(%d)\n'%(self.__majortype)
		rbuf += 'minortype       :(%d)\n'%(self.__minortype)
		rbuf += 'logtime         :(%s)\n'%(self.__logtime)
		rbuf += 'logdata         :(%s)\n'%(self.__logdata)
		return rbuf

	def __repr__(self):
		return self.__Format()

	def __str__(self):
		return self.__Format()

	def MajorType(self,val=None):
		ov = self.__majortype
		if ov is not None:
			self.__majortype = val
		return ov

	def MinorType(self,val=None):
		ov = self.__minortype
		if ov is not None:
			self.__minortype = val
		return ov

	def LogTime(self,val=None):
		ov = self.__logtime
		if ov is not None:
			self.__logtime = val
		return ov

	def LogData(self,val=None):
		ov = self.__logdata
		if val is not None:
			self.__logdata = val
		return ov

class LogInfoSearch:
	def __ResetVar(self):
		self.__selectmode = 0
		self.__majortype = 0
		self.__minortype = 0
		self.__starttime = ''
		self.__stoptime = ''
		self.__offset = 0
		self.__maxnum = 0

	def __init__(self):
		self.__ResetVar()
		return

	def __del__(self):
		self.__ResetVar()
		return


	def GetString(self,s,size):
		rbuf = ''
		lasti  = -1
		for i in xrange(size):
			if s[i] == '\0':
				lasti = i
				break

		if lasti >= 0:
			rbuf = s[:lasti]
		else:
			rbuf = s[:-2]
		return rbuf
	def FormatString(self,s,size):
		rbuf = ''
		if len(s) < size:
			rbuf += s
			lsize = size - len(s)
			rbuf += '\0' * lsize
		else:
			rbuf += s[:(size-1)]
			rbuf += '\0'
		return rbuf

	def ParseBuf(self,buf):
		if len(buf) < LOGINFO_SEARCH_SIZE:
			raise LogInfoSearchInvalidError('len(%d) < %d'%(len(buf),LOGINFO_SEARCH_SIZE))
		self.__selectmode,self.__majortype,self.__minortype = struct.unpack('>III',buf[:12])
		self.__starttime = self.GetString(buf[12:44],32)
		self.__stoptime = self.GetString(buf[44:76],32)
		self.__offset,self.__maxnum = struct.unpack('>II',buf[76:84])
		return buf[LOGINFO_SEARCH_SIZE:]

	def FormatBuf(self):
		rbuf = ''
		rbuf += struct.pack('>III',self.__selectmode,self.__majortype,self.__minortype)
		rbuf += self.FormatString(self.__starttime,32)
		rbuf += self.FormatString(self.__stoptime,32)
		rbuf += struct.pack('>II',self.__offset,self.__maxnum)
		return rbuf

	def __Format(self):
		rbuf = ''
		rbuf += 'selectmode      :(%d)\n'%(self.__selectmode)
		rbuf += 'majortype       :(%d)\n'%(self.__majortype)
		rbuf += 'minortype       :(%d)\n'%(self.__minortype)
		rbuf += 'starttime       :(%s)\n'%(self.__starttime)
		rbuf += 'stoptime        :(%s)\n'%(self.__stoptime)
		rbuf += 'offset          :(%d)\n'%(self.__offset)
		rbuf += 'maxnum          :(%d)\n'%(self.__maxnum)
		return rbuf

	def __repr__(self):
		return self.__Format()

	def __str__(self):
		return self.__Format()


	def SelectMode(self,val=None):
		ov = self.__selectmode
		if val is not None:
			self.__selectmode = val
		return ov

	def MajorType(self,val=None):
		ov = self.__majortype
		if val is not None:
			self.__majortype = val
		return ov

	def MinorType(self,val=None):
		ov = self.__minortype
		if val is not None:
			self.__minortype = val
		return ov
	def StartTime(self,val=None):
		ov = self.__starttime
		if val is not None:
			self.__starttime = val
		return ov

	def StopTime(self,val=None):
		ov = self.__stoptime
		if val is not None:
			self.__stoptime = val
		return ov

	def Offset(self,val=None):
		ov = self.__offset
		if val is not None:
			self.__offset=val
		return ov

	def MaxNum(self,val=None):
		ov = self.__maxnum
		if val is not None:
			self.__maxnum = val
		return ov


class LogInfoPack(syscp.SysCP):
	def __init__(self):
		syscp.SysCP.__init__(self)		
		self.__logs = []
		return 

	def __del__(self):
		syscp.SysCP.__del__(self)
		self.__logs = []
		return

	def FormatReq(self,sesid,seqid,search):
		if not isinstance(search,LogInfoSearch):
			raise LogInfoSearchInvalidError('param not subclass for LogInfoSearch')
		reqbuf = search.FormatBuf()
		seqbuf = self.TypeCodeForm(TYPE_LOGINFO_SEARCH,reqbuf)
		return self.FormatSysCp(SYSCODE_GET_LOGINFO_REQ,1,seqbuf,sesid,seqid)

	def ParseRsp(self,rbuf):
		cnt = 0
		attrbuf = self.UnPackSysCp(rbuf)
		if self.Code() != SYSCODE_GET_LOGINFO_RSP:
			raise LogInfoSearchPackInvalidError('code(%d) != (%d)'%(self.Code(),SYSCODE_GET_LOGINFO_RSP))
		self.__logs = []
		for i in xrange(self.AttrCount()):
			attrbuf = self.ParseTypeCode(attrbuf)
			if self.TypeCode() == TYPE_LOGINFO:
				li = LogInfo()
				attrbuf = li.ParseBuf(attrbuf)
				self.__logs.append(li)
			elif self.TypeCode() == TYPE_LOGINFO_INT:
				cnt = struct.unpack('>I',attrbuf[:4])[0]
				return cnt 
			else:
				raise LogInfoSearchPackInvalidError('[%d] attr is TypeCode(%d) Length(%d) %s '%(i,self.TypeCode(),self.TypeLen(),repr(attrbuf)))

		return self.__logs