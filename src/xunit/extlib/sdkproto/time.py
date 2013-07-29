#! python

'''
	this is the file for the showcfg set and get
'''

import struct

import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..')))
import xunit.utils.exception
import xunit.extlib.sdkproto.syscp as syscp


TYPE_TIMETYPE=109
TYPE_TIMETYPE_STRUCT_LENGTH=8
TYPE_TIMETYPE_LENGTH=(TYPE_TIMETYPE_STRUCT_LENGTH+4)


TYPE_SYSTIME=15
TYPE_SYSTIME_STRUCT_LENGTH=24
TYPE_SYSTIME_LENGTH=(TYPE_SYSTIME_STRUCT_LENGTH+4)

TYPE_TIMEZONE=108
TYPE_TIMEZONE_STRUCT_LENGTH=36
TYPE_TIMEZONE_LENGTH=(TYPE_TIMEZONE_STRUCT_LENGTH+4)


TYPE_NTPSERVER=107
TYPE_NTPSERVER_STRUCT_LENGTH=96
TYPE_NTPSERVER_LENGTH=(TYPE_NTPSERVER_STRUCT_LENGTH+4)

SYSCODE_SET_TIME_REQ=1061
SYSCODE_SET_TIME_RSP=1062
SYSCODE_GET_TIME_REQ=1063
SYSCODE_GET_TIME_RSP=1064

class TimeInvalidError(xunit.utils.exception.XUnitException):
	pass


class TimeType:
	def __init__(self):
		self.__type = 0
		self.__ntpinterval = 0
		return

	def __del__(self):
		self.__type = 0
		self.__ntpinterval = 0
		return

	def __Format(self):
		rbuf = ''
		rbuf += 'type           : %d\n'%(self.__type)
		rbuf += 'ntpinterval    : %d\n'%(self.__ntpinterval)
		return rbuf

	

	def __str__(self):
		return self.__Format()

	def __repr__(self):
		return self.__Format()

	def ParseBuf(self,buf):
		if len(buf) < TYPE_TIMETYPE_STRUCT_LENGTH:
			raise TimeInvalidError('len(%d) < (%d)'%(len(buf),TYPE_TIMETYPE_STRUCT_LENGTH))
		self.__type , self.__ntpinterval = 	struct.unpack('>II',buf[:TYPE_TIMETYPE_STRUCT_LENGTH])
		return buf[TYPE_TIMETYPE_STRUCT_LENGTH:]

	def FormBuf(self):
		rbuf = ''
		rbuf += struct.pack('>II',self.__type , self.__ntpinterval)
		return rbuf

	def Type(self,val=None):
		ov = self.__type
		if val is not None:
			self.__type = val
		return ov

	def NtpInterval(self,val=None):
		ov = self.__ntpinterval
		if val is not None:
			self.__ntpinterval = val
		return ov


class SysTime:
	def __init__(self):
		self.__year = 0
		self.__month = 0
		self.__day = 0
		self.__hour = 0
		self.__minute = 0
		self.__second = 0
		return

	def __del__(self):
		self.__year = 0
		self.__month = 0
		self.__day = 0
		self.__hour = 0
		self.__minute = 0
		self.__second = 0
		return 

	def __Format(self):
		rbuf = ''
		rbuf += 'year    : %d\n'%(self.__year)
		rbuf += 'month   : %d\n'%(self.__month)
		rbuf += 'day     : %d\n'%(self.__day)
		rbuf += 'hour    : %d\n'%(self.__hour)
		rbuf += 'minute  : %d\n'%(self.__minute)
		rbuf += 'second  : %d\n'%(self.__second)
		return rbuf

	def __str__(self):
		return self.__Format()

	def __repr__(self):
		return self.__Format()

	def ParseBuf(self,buf):
		if len(buf) < TYPE_SYSTIME_STRUCT_LENGTH:
			raise TimeInvalidError('len(%d) < (%d)'%(len(buf),TYPE_SYSTIME_STRUCT_LENGTH))
		self.__year , self.__month ,self.__day \
		self.__hour , self.__minute,self.__second = \
		struct.unpack('>IIIIII',buf[:TYPE_SYSTIME_STRUCT_LENGTH])
		return buf[TYPE_SYSTIME_STRUCT_LENGTH:]

	def FormBuf(self):
		rbuf = ''
		rbuf += struct.pack('>IIIIII',self.__year , self.__month ,self.__day \
		self.__hour , self.__minute,self.__second)
		return rbuf

	def Year(self,val=None):
		ov = self.__year
		if val is not None:
			self.__year = val
		return ov

	def Month(self,val=None):
		ov = self.__month
		if val is not None:
			self.__month = val
		return ov

	def Day(self,val=None):
		ov = self.__day
		if val is not None:
			self.__day = val
		return ov

	def Hour(self,val=None):
		ov = self.__hour
		if val is not None:
			self.__hour = val
		return ov

	def Minute(self,val=None):
		ov = self.__minute
		if val is not None:
			self.__minute = val
		return ov

	def Second(self,val=None):
		ov = self.__second
		if val is not None:
			self.__second = val
		return ov



class TimeZone:
	def __init__(self):
		self.__timezone = 0
		self.__timezonename = ''
		return

	def __del__(self):
		self.__timezone = 0
		self.__timezonename = ''
		return

	def TimeZone(self,val=None):
		ov = self.__timezone
		if val:
			self.__timezone = val
		return ov

	def TimeZoneName(self,val=None):
		ov = self.__timezonename
		if val:
			self.__timezonename = val
		return ov

	def __Format(self):
		rbuf = ''
		rbuf += 'timezone          : %d\n'%(self.__timezone)
		rbuf += 'timezonename      : %s\n'%(self.__timezonename)
		return rbuf

	def __str__(self):
		return self.__Format()

	def __repr__(self):
		return self.__Format()

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
		self.__timezone = struct.unpack('>I',buf[:4])[0]

		self.__timezonename = self.GetString(buf[4:],32)
		return buf[TYPE_TIMEZONE_STRUCT_LENGTH:]

	def FormBuf(self):
		rbuf = ''
		rbuf += struct.pack('>I',self.__timezone)
		rbuf += self.FormatString(self.__timezone,32)
		return rbuf

class NtpServer:
	def __init__(self):
		self.__ntpaddr1 = ''
		self.__ntpaddr2 = ''
		self.__ntpaddr3 = ''
		return

	def __del__(self):
		self.__ntpaddr1 = ''
		self.__ntpaddr2 = ''
		self.__ntpaddr3 = ''
		return
	
	def __Format(self):
		rbuf = ''
		rbuf += 'ntpaddr1          : %s\n'%(self.__ntpaddr1)
		rbuf += 'ntpaddr2          : %s\n'%(self.__ntpaddr2)
		rbuf += 'ntpaddr3          : %s\n'%(self.__ntpaddr3)
		return rbuf
	def __str__(self):
		return self.__Format()

	def __repr__(self):
		return self.__Format()

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

	def FormatBuf(self):
		rbuf = ''
		rbuf += self.FormatString(self.__ntpaddr1,32)
		rbuf += self.FormatString(self.__ntpaddr2,32)
		rbuf += self.FormatString(self.__ntpaddr3,32)
		return rbuf

	def ParseBuf(self,buf):
		if len(buf) < TYPE_NTPSERVER_STRUCT_LENGTH:
			raise 
		self.__ntpaddr1 = self.GetString(buf,32)
		self.__ntpaddr2 = self.GetString(buf[32:],32)
		self.__ntpaddr3 = self.GetString(buf[64:],32)
		return buf[TYPE_NTPSERVER_STRUCT_LENGTH:]

	def NtpAddr1(self,val=None):
		ov = self.__ntpaddr1
		if val:
			self.__ntpaddr1 = val
		return ov

	def NtpAddr2(self,val=None):
		ov = self.__ntpaddr2
		if val:
			self.__ntpaddr2 = val
		return ov
		
	def NtpAddr3(self,val=None):
		ov = self.__ntpaddr3
		if val:
			self.__ntpaddr3 = val
		return ov


class SdkTimeInvalidError(xunit.utils.exception.XUnitException):
	pass


class SdkTime(syscp.SysCP):
	def __init__(self):
		syscp.SysCP.__init__(self)
		self.__timetype = None
		self.__systime = None
		self.__ntpserver = None
		self.__timezone = None
		return
	def __del__(self):
		syscp.SysCP.__del__(self)
		self.__timetype = None
		self.__systime = None
		self.__ntpserver = None
		self.__timezone = None
		return

	def FormGetTimeReq(self,sesid=None,seqid=None):
		return self.FormatSysCp(SYSCODE_GET_TIME_REQ,0,'',sesid,seqid)

	def ParseGetTimeResp(self,buf):
		attrbuf = self.UnPackSysCp(buf)
		if self.Code() != SYSCODE_GET_TIME_RSP:
			raise SdkTimeInvalidError('code (%d) != (%d)'%(self.Code(),SYSCODE_GET_TIME_RSP))
		if self.AttrCount() != 4:
			raise SdkTimeInvalidError('attrcount (%d) != (4)'%(self.AttrCount()))

		self.__systime = None
		self.__timetype = None
		self.__ntpserver = None
		self.__timezone = None
		for i in xrange(self.AttrCount()):
			attrbuf = self.ParseTypeCode(attrbuf)
			if self.TypeCode() == TYPE_TIMETYPE:
				if self.__timetype is not None:
					raise SdkTimeInvalidError('specify timetype twice')
				self.__timetype = TimeType()
				attrbuf = self.__timetype.ParseBuf(attrbuf)
			elif self.TypeCode() == TYPE_SYSTIME:
				if self.__systime is not None:
					raise SdkTimeInvalidError('specify systime twice') 
				self.__systime = SysTime()
				attrbuf = self.__systime.ParseBuf(attrbuf)
			elif self.TypeCode() == TYPE_NTPSERVER:
				if self.__ntpserver is not None:
					raise SdkTimeInvalidError('specify ntpserver twice') 
				self.__ntpserver = NtpServer()
				attrbuf = self.__ntpserver.ParseBuf(attrbuf)
			elif self.TypeCode() == TYPE_TIMEZONE:
				if self.__timezone is not None:
					raise SdkTimeInvalidError('specify timezone twice') 
				self.__timezone = TimeZone()
				attrbuf = self.__timezone.ParseBuf(attrbuf)
			else:
				raise SdkTimeInvalidError('typecode (%d) should not appear'%(self.TypeCode()))

		if self.__timezone is None or self.__ntpserver is None or\
			self.__systime is None or self.__timetype is None:
			raise SdkTimeInvalidError('not valid pass 4 struct')

		return self.__timetype,self.__systime,self.__ntpserver,self.__timezone

	def FormSetTimeReq(self,timetype,systime,ntpserver,timezone,sesid=None,seqid=None):
		count =0
		attrbuf = ''
		if timetype is not None and not isinstance(timetype,TimeType):
			raise SdkTimeInvalidError('param timetype is not TimeType class')
		elif timetype :
			rbuf = timetype.FormatBuf()
			attrbuf += self.TypeCodeForm(TYPE_TIMETYPE,rbuf)
			count += 1

		if systime is not None and not isinstance(systime,SysTime):
			raise SdkTimeInvalidError('param systime is not SysTime class')
		elif systime:
			rbuf = systime.FormatBuf()
			attrbuf += self.TypeCodeForm(TYPE_SYSTIME,rbuf)
			count += 1

			
		if ntpserver is not None and not isinstance(ntpserver,NtpServer):
			raise SdkTimeInvalidError('param ntpserver is not NtpServer class')
		elif ntpserver:
			rbuf = ntpserver.FormatBuf()
			attrbuf += self.TypeCodeForm(TYPE_NTPSERVER,rbuf)
			count += 1
 		if timezone is not None and not isinstance(timezone,TimeZone):
 			raise SdkTimeInvalidError('param timezone is not TimeZone class')
 		elif timezone:
			rbuf = timezone.FormatBuf()
			attrbuf += self.TypeCodeForm(TYPE_TIMEZONE,rbuf)
			count += 1

		if count == 0:
			raise SdkTimeInvalidError('timetype systime ntpserver timezone must specify at least 1')
		# now we should type code
		return self.FormatSysCp(SYSCODE_SET_TIME_REQ,count,attrbuf,sesid,seqid)


	def ParseSetTimeResp(self,buf):
		attrbuf = self.UnPackSysCp(buf)
		if self.Code() != SYSCODE_SET_TIME_RSP:
			raise SdkTimeInvalidError('code (%d) != (%d)'%(self.Code(),SYSCODE_SET_TIME_RSP))

		if self.AttrCount() != 1:
			raise SdkTimeInvalidError('attrcount (%d) != (1)'%(self.AttrCount()))

		self.MessageCodeParse(attrbuf)
		return 