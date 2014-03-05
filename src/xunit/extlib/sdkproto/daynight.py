'''
this is the file for day night
'''

import struct

import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..')))
import xunit.utils.exception
import xunit.extlib.sdkproto.syscp as syscp
from types import *

DAY_NIGHT_SCHED_WEEKS=8
DAY_NIGHT_SIZE=116

TYPE_DAY_NIGHT=118

SYSCODE_GET_DAY_NIGHT_REQ=1223
SYSCODE_GET_DAY_NIGHT_RSP=1224
SYSCODE_SET_DAY_NIGHT_REQ=1225
SYSCODE_SET_DAY_NIGHT_RSP=1226

class DayNightInvalidError(xunit.utils.exception.XUnitException):
	pass


class DayNight:
	def __ResetVar(self):
		self.__mode = 0
		self.__durationtime = 5
		self.__nighttodaythr = 60
		self.__daytonightthr = 40
		self.__schedenable = []
		self.__schedstarttime = []
		self.__schedstoptime = []
		for i in xrange(DAY_NIGHT_SCHED_WEEKS):
			self.__schedenable.append(0)
			self.__schedstarttime.append(0)
			self.__schedstoptime.append(0)
		self.__reserv1 = '\0' * 4
		return

	def __init__(self):
		self.__ResetVar()
		return

	def __del__(self):
		self.__ResetVar()
		return

	def ParseBuf(self,buf):
		if len(buf) < DAY_NIGHT_SIZE:
			raise DayNightInvalidError('len(%d) < DAY_NIGHT_SIZE(%d)'(len(buf),DAY_NIGHT_SIZE))
		self.__mode,self.__durationtime,self.__nighttodaythr,self.__daytonightthr = struct.unpack('>IIII',buf[:16])
		rbuf = buf[16:]
		for i in xrange(DAY_NIGHT_SCHED_WEEKS):
			self.__schedenable[i] = struct.unpack('>I',rbuf[:4])[0]
			rbuf = rbuf[4:]
		for i in xrange(DAY_NIGHT_SCHED_WEEKS):
			self.__schedstarttime[i] = struct.unpack('>I',rbuf[:4])[0]
			rbuf = rbuf[4:]
		
		for i in xrange(DAY_NIGHT_SCHED_WEEKS):
			self.__schedstoptime[i] = struct.unpack('>I',rbuf[:4])[0]
			rbuf = rbuf[4:]

		self.__reserv1 = rbuf[:4]
		return rbuf[4:]

	def FormatBuf(self):
		rbuf = ''
		rbuf += struct.pack('>IIII',self.__mode,self.__durationtime,self.__nighttodaythr,self.__daytonightthr)
		for i in xrange(DAY_NIGHT_SCHED_WEEKS):
			rbuf += struct.pack('>I',self.__schedenable[i])
		for i in xrange(DAY_NIGHT_SCHED_WEEKS):
			rbuf += struct.pack('>I',self.__schedstarttime[i])
		for i in xrange(DAY_NIGHT_SCHED_WEEKS):
			rbuf += struct.pack('>I',self.__schedstoptime[i])
		rbuf += self.__reserv1
		return rbuf

	def __Format(self):
		rbuf = ''
		rbuf += 'mode                    :(%d)\n'%(self.__mode)
		rbuf += 'durationtime            :(%d)\n'%(self.__durationtime)
		rbuf += 'nighttodaythr           :(%d)\n'%(self.__nighttodaythr)
		rbuf += 'daytonightthr           :(%d)\n'%(self.__daytonightthr)
		for i in xrange(DAY_NIGHT_SCHED_WEEKS):
			rbuf += 'sched[%d]                :enable(%d) start-stop(%d-%d)\n'%(i,self.__schedenable[i],self.__schedstarttime[i],self.__schedstoptime[i])
		rbuf += 'reserv1                 :(%s)\n'%(repr(self.__reserv1))
		return rbuf

	def __str__(self):
		return self.__Format()

	def __repr__(self):
		return self.__Format()
		
	
	def Mode(self,val=None):
		ov = self.__mode
		if val is not None:
			self.__mode = val
		return ov

	def DurationTime(self,val=None):
		ov = self.__durationtime
		if val is not None:
			self.__durationtime = val
		return ov

	def NightToDayThr(self,val=None):
		ov = self.__nighttodaythr
		if val is not None:
			self.__nighttodaythr = val
		return ov
	def DayToNightThr(self,val=None):
		ov = self.__daytonightthr
		if val is not None:
			self.__daytonightthr = val
		return ov
	def Reserv1(self,val=None):
		ov = self.__reserv1
		if val is not None:
			self.__reserv1 = val
		return ov
	def __ValidIdx(self,idx):
		if type(idx) is not IntType:
			raise DayNightInvalidError('idx not inttype')
		if idx < 0 or idx >= DAY_NIGHT_SCHED_WEEKS:
			raise DayNightInvalidError('idx(%d) not valid'%(idx))
		return 
	def SchedEnableIdx(self,idx,val=None):
		self.__ValidIdx(idx)
		ov = self.__schedenable[idx]
		if val is not None:
			self.__schedenable[idx] = val
		return ov

	def SchedStartTimeIdx(self,idx,val=None):
		self.__ValidIdx(idx)
		ov = self.__schedstarttime[idx]
		if val is not None:
			self.__schedstarttime[idx] = val
		return ov
	def SchedStopTimeIdx(self,idx,val=None):
		self.__ValidIdx(idx)
		ov = self.__schedstoptime[idx]
		if val is not None:
			self.__schedstoptime[idx] = val
		return ov

class SdkDayNight(syscp.SysCP):
	def __init__(self):
		syscp.SysCP.__init__(self)
		self.__daynight = None
		return
	def __del__(self):
		syscp.SysCP.__del__(self)
		self.__daynight = None
		return

	def FormGetReq(self,sesid=None,seqid=None):
		return self.FormatSysCp(SYSCODE_GET_DAY_NIGHT_REQ,0,'',sesid,seqid)

	def ParseGetRsp(self,buf):
		attrbuf = self.UnPackSysCp(buf)
		if self.Code() != SYSCODE_GET_DAY_NIGHT_RSP:
			raise DayNightInvalidError('Code (%d) != SYSCODE_GET_DAY_NIGHT_RSP(%d)'%(self.Code(),SYSCODE_GET_DAY_NIGHT_RSP))

		if self.AttrCount() < 1:
			raise DayNightInvalidError('attrcount (%d) < 1'%(self.AttrCount()))
		attrbuf = self.ParseTypeCode(attrbuf)
		if self.TypeCode() != TYPE_DAY_NIGHT:
			raise DayNightInvalidError('type(%d) != TYPE_DAY_NIGHT(%d)'%(self.TypeCode(),TYPE_DAY_NIGHT))
		self.__daynight= DayNight()
		self.__daynight.ParseBuf(attrbuf)
		return self.__daynight

	def FormSetReq(self,dn,sesid=None,seqid=None):
		if not isinstance(dn,DayNight):
			raise DayNightInvalidError('parameter not DayNight type')
		reqbuf = self.TypeCodeForm(TYPE_DAY_NIGHT,dn.FormatBuf())
		return self.FormatSysCp(SYSCODE_SET_DAY_NIGHT_REQ,1,reqbuf,sesid,seqid)

	def ParseSetRsp(self,buf):
		attrbuf = self.UnPackSysCp(buf)
		if self.Code() != SYSCODE_SET_DAY_NIGHT_RSP:
			raise DayNightInvalidError('Code (%d) != SYSCODE_SET_DAY_NIGHT_RSP(%d)'%(self.Code(),SYSCODE_SET_DAY_NIGHT_RSP))

		if self.AttrCount() < 1:
			raise DayNightInvalidError('attrcount (%d) < 1'%(self.AttrCount()))
		self.MessageCodeParse(attrbuf,'DayNight Set Resp')
		return

