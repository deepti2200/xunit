#! python

'''
this is the file for capabilities get
'''

import struct

import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..')))
import xunit.utils.exception
import xunit.extlib.sdkproto.syscp as syscp


ALARM_INFO_SIZE=252
SYSCODE_GET_ALARM_RSP=1230
TYPE_WARNING_INFO=122

class AlarmInfoInvalidError(xunit.utils.exception.XUnitException):
	pass

class AlarmInfoPackInvalidError(xunit.utils.exception.XUnitException):
	pass


class AlarmInfo:
	def __Reset(self):
		self.__warningid= 0
		self.__warningtype = 0
		self.__warninglevel = 0
		self.__onoff = 0
		self.__time = ''
		self.__devid = ''
		self.__description = ''
		self.__extrainfo = ''
		return
		
	def __init__(self):
		self.__Reset()
		return

	def __del__(self):
		self.__Reset()
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
			rbuf = s[:(size-1)]
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

	def ParseBuf(self,sbuf):
		if len(sbuf) < ALARM_INFO_SIZE:
			raise AlarmInfoInvalidError('len(%d) < ALARM_INFO_SIZE(%d)'%(len(sbuf),ALARM_INFO_SIZE))
		hll,lll = struct.unpack('>II',sbuf[:8])
		self.__warningid = (hll << 32) | lll
		self.__warningtype ,self.__warninglevel,self.__onoff = struct.unpack('>III',sbuf[8:20])
		self.__time = self.GetString(sbuf[20:],36)
		self.__devid = self.GetString(sbuf[56:],64)
		self.__description = self.GetString(sbuf[120:],128)
		self.__extrainfo = sbuf[248:ALARM_INFO_SIZE]
		return sbuf[ALARM_INFO_SIZE:]

	def __Format(self):
		rbuf = ''
		rbuf += 'warningid        : (%d)\n'%(self.__warningid)
		rbuf += 'warningtype      : (%d)\n'%(self.__warningtype)
		rbuf += 'warninglevel     : (%d)\n'%(self.__warninglevel)
		rbuf += 'warningonoff     : (%d)\n'%(self.__onoff)
		rbuf += 'time             : (%s)\n'%(self.__time)
		rbuf += 'devid            : (%s)\n'%(self.__devid)
		rbuf += 'description      : (%s)\n'%(self.__description)
		rbuf += 'extrainfo        : (%s)\n'%(repr(self.__extrainfo))
		return rbuf

	def FormatBuf(self):
		hll = (self.__warningid >> 32)
		lll = self.__warningid & 0xffffffff
		rbuf = ''
		rbuf += struct.pack('>II',hll,lll)
		rbuf += struct.pack('>III',self.__warningtype,self.__warninglevel,self.__onoff)
		rbuf += self.FormatString(self.__time,36)
		rbuf += self.FormatString(self.__devid,64)
		rbuf += self.FormatString(self.__description,128)
		rbuf += self.__extrainfo
		return rbuf


	def __str__(self):
		return self.__Format()

	def __repr__(self):
		return self.__Format()

class AlarmInfoPack(syscp.SysCP):
	def __init__(self):
		syscp.SysCP.__init__(self)
		self.__alarminfos = []
		return
	def __del__(self):
		syscp.SysCP.__del__(self)
		self.__alarminfos = []
		return

	def ParseAlarmInfo(self,rbuf):
		respbuf = self.UnPackSysCp(rbuf)

		if self.Code() != SYSCODE_GET_ALARM_RSP:
			raise AlarmInfoPackInvalidError('Code(%d) != SYSCODE_GET_ALARM_RSP(%d)'%(self.Code(),SYSCODE_GET_ALARM_RSP))
		if self.AttrCount() < 1:
			raise AlarmInfoPackInvalidError('AttrCount(%d) < 1'%(self.AttrCount()))

		self.__alarminfos = []
		attrbuf = self.PackedBuf()
		for i in xrange(self.AttrCount()):
			typebuf = attrbuf[:syscp.TYPE_INFO_LENGTH]
			typecode,typelen = struct.unpack('>HH',typebuf[:syscp.TYPE_INFO_LENGTH])
			if typecode != TYPE_WARNING_INFO:
				raise AlarmInfoPackInvalidError('typecode (%d) != (%d)'%(typecode,TYPE_WARNING_INFO))
			if(typelen) > len(attrbuf):
				raise AlarmInfoPackInvalidError('left len (%d) < (%d + %d)'%(len(attrbuf),typelen ,syscp.TYPE_INFO_LENGTH))
			pbuf = attrbuf[syscp.TYPE_INFO_LENGTH:(typelen)]
			attrbuf = attrbuf[(typelen):]
			alarm = AlarmInfo()
			alarm.ParseBuf(pbuf)
			self.__alarminfos.append(alarm)

		return self.__alarminfos




