'''
this is the file for alarm deploy
'''

import struct

import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..')))
import xunit.utils.exception
import xunit.extlib.sdkproto.syscp as syscp

ALARM_GET_SCHEDULE_TIME_INFO_SIZE=16
ALARM_SCHEDULE_TIME_SIZE=8
WEEKDAY=7
DAYSPAN=4
ALARM_SCHEDULE_TIME_INFO_SIZE=4*4+(WEEKDAY*DAYSPAN*ALARM_SCHEDULE_TIME_SIZE)

TYPE_GET_ALMDEPLOY=126
TYPE_ALMDEPLOY=66

SYSCODE_SET_ALMDEPLOY_REQ=1141
SYSCODE_SET_ALMDEPLOY_RSP=1142
SYSCODE_GET_ALMDEPLOY_REQ=1143
SYSCODE_GET_ALMDEPLOY_RSP=1144

class AlarmDeployInvalidError(xunit.utils.exception.XUnitException):
	pass


class AlarmGetScheduleTimeInfo:
	def __ResetVar(self):
		self.__scheduleid = 0
		self.__index = 0
		self.__reserv1 = '\0' * 8
		return

	def __init__(self):
		self.__ResetVar()
		return
	def __del__(self):
		self.__ResetVar()
		return

	def ParseBuf(self,buf):
		if len(buf) < ALARM_GET_SCHEDULE_TIME_INFO_SIZE:
			raise AlarmDeployInvalidError('buf(%d) < ALARM_GET_SCHEDULE_TIME_INFO_SIZE(%d)'%(len(buf),ALARM_GET_SCHEDULE_TIME_INFO_SIZE))
		self.__scheduleid,self.__index = struct.unpack('>II',buf[:8])
		self.__reserv1 = buf[8:16]
		return buf[ALARM_GET_SCHEDULE_TIME_INFO_SIZE:]
	def FormatBuf(self):
		rbuf = ''
		rbuf += struct.pack('>II',self.__scheduleid,self.__index)
		rbuf += self.__reserv1
		return rbuf

	def __Format(self):
		rbuf = 'ScheduleTimeInfo:\n'
		rbuf += 'scheduleid                   :(%d)\n'%(self.__scheduleid)
		rbuf += 'index                           :(%d)\n'%(self.__index)
		rbuf += 'reserv1                        :(%s)\n'%(repr(self.__reserv1))
		return rbuf

	def __str__(self):
		return self.__Format()
	def __repr__(self):
		return self.__Format()

	def ScheduleId(self,val=None):
		ov = self.__scheduleid
		if val is not None:
			self.__scheduleid = val
		return ov

	def Index(self,val=None):
		ov = self.__index
		if val is not None:
			self.__index = val
		return ov
	def Reserv1(self,val=None):
		ov = self.__reserv1
		if val is not None:
			self.__reserv1 = val
		return ov


class ScheduleTime:
	def __ResetVar(self):
		self.__starttime = 0
		self.__endtime = 0
		return

	def __init__(self):
		self.__ResetVar()
		return
	def __del__(self):
		self.__ResetVar()
		return

	def ParseBuf(self,buf):
		if len(buf) < ALARM_SCHEDULE_TIME_SIZE:
			raise AlarmDeployInvalidError('buf(%d) < ALARM_SCHEDULE_TIME_SIZE(%d)'%(len(buf),ALARM_SCHEDULE_TIME_SIZE))
		self.__starttime,self.__endtime = struct.unpack('>II',buf[:8])
		return buf[ALARM_SCHEDULE_TIME_SIZE:]
	def FormatBuf(self):
		rbuf = ''
		rbuf += struct.pack('>II',self.__starttime,self.__endtime)
		return rbuf

	def __Format(self):
		rbuf = 'ScheduleTime:\n'
		rbuf += 'StartTime                 :(%d)\n'%(self.__starttime)
		rbuf += 'EndTime                   :(%d)\n'%(self.__endtime)
		return rbuf

	def __str__(self):
		return self.__Format()

	def __repr__(self):
		return self.__Format()

	def StartTime(self,val=None):
		ov = self.__starttime
		if val is not None:
			self.__starttime = val
		return ov
	def EndTime(self,val=None):
		ov = self.__endtime
		if val is not None:
			self.__endtime = val
		return ov


class AlarmScheduleTimeInfo:
	def __ResetVar(self):
		self.__scheduleid = 0
		self.__index = 0
		self.__times = []
		for i in xrange(WEEKDAY):
			for j in xrange(DAYSPAN):
				st = ScheduleTime()
				self.__times.append(st)
		self.__reserv1 = '\0' * 8
		return

	def __init__(self):
		self.__ResetVar()
		return
	def __del__(self):
		self.__ResetVar()
		return


	def ParseBuf(self,buf):
		if len(buf) < ALARM_SCHEDULE_TIME_INFO_SIZE:
			raise AlarmDeployInvalidError('buf(%d) < ALARM_SCHEDULE_TIME_INFO_SIZE(%d)'%(len(buf),ALARM_SCHEDULE_TIME_INFO_SIZE))
		self.__scheduleid,self.__index = struct.unpack('>II',buf[:8])
		rbuf = buf[8:]
		for i in xrange(WEEKDAY):
			for j in xrange(DAYSPAN):
				st = ScheduleTime()
				rbuf = st.ParseBuf(rbuf)
				self.__times[i*DAYSPAN + j] = st
		self.__reserv1 = rbuf[:8]
		return rbuf[8:]

	def FormatBuf(self):
		rbuf = ''
		rbuf += struct.pack('>II',self.__scheduleid,self.__index)
		for i in xrange(WEEKDAY):
			for j in xrange(DAYSPAN):
				rbuf += self.__times[i*DAYSPAN + j].FormatBuf()
		rbuf += self.__reserv1
		return rbuf

	def __Format(self):
		rbuf = 'AlarmScheduleTimeInfo:\n'
		rbuf += 'scheduleid                 :(%d)\n'%(self.__scheduleid)
		rbuf += 'index                         :(%d)\n'%(self.__index)
		for i in xrange(WEEKDAY):
			for j in xrange(DAYSPAN):
				rbuf += 'Time[%d][%d]:\n'%(i,j)
				rbuf += str(self.__times[i*DAYSPAN+j])
		rbuf += 'reserv1                      :(%s)\n'%(self.__reserv1)
		return rbuf

	def __str__(self):
		return self.__Format()

	def __repr__(self):
		return self.__Format()

	def ScheduleId(self,val=None):
		ov = self.__scheduleid
		if val is not None:
			self.__scheduleid = val
		return ov
	def Index(self,val=None):
		ov = self.__index
		if val is not None:
			self.__index = val
		return ov
	def StartTimeIdx(self,i,j,val=None):
		if i >= WEEKDAY:
			raise AlarmDeployInvalidError('i(%d) > WEEKDAY(%d)'%(i,WEEKDAY))
		if j >= DAYSPAN:
			raise AlarmDeployInvalidError('j(%d) > WEEKDAY(%d)'%(j,WEEKDAY))
		return self.__times[i*DAYSPAN+j].StartTime(val)
	def EndTimeIdx(self,i,j,val=None):
		if i >= WEEKDAY:
			raise AlarmDeployInvalidError('i(%d) > WEEKDAY(%d)'%(i,WEEKDAY))
		if j >= DAYSPAN:
			raise AlarmDeployInvalidError('j(%d) > WEEKDAY(%d)'%(j,WEEKDAY))
		return self.__times[i*DAYSPAN+j].EndTime(val)

	def Reserv1(self,val=None):
		ov = self.__reserv1
		if val is not None:
			self.__reserv1 = val
		return ov


class SdkAlarmDeploy(syscp.SysCP):
	def __init__(self):
		syscp.SysCP.__init__(self)
		self.__alarmdeploy = None
		return
	def __del__(self):
		syscp.SysCP.__del__(self)
		self.__alarmdeploy = None
		return

	def FormGetReq(self,getscheduletime,sesid=None,seqid=None):
		if not isinstance(getscheduletime,AlarmGetScheduleTimeInfo):
			raise AlarmDeployInvalidError('getscheduletime parameter not AlarmGetScheduleTimeInfo type')
		rbuf = getscheduletime.FormatBuf()
		reqbuf = self.TypeCodeForm(TYPE_GET_ALMDEPLOY,rbuf)
		return self.FormatSysCp(SYSCODE_GET_ALMDEPLOY_REQ,1,reqbuf,sesid,seqid)

	def ParseGetRsp(self,buf):
		#logging.info('buf (%s)'%(repr(buf)))
		attrbuf = self.UnPackSysCp(buf)
		if self.Code() != SYSCODE_GET_ALMDEPLOY_RSP:
			raise AlarmDeployInvalidError('code(%d) != SYSCODE_GET_ALMDEPLOY_RSP(%d)'%(self.Code(),SYSCODE_GET_ALMDEPLOY_RSP))
		self.__alarmdeploy = AlarmScheduleTimeInfo()
		attrbuf = self.ParseTypeCode(attrbuf)
		if self.TypeCode() != TYPE_ALMDEPLOY:
			raise AlarmDeployInvalidError('TypeCode(%d) != TYPE_ALMDEPLOY(%d)'%(self.TypeCode(),TYPE_ALMDEPLOY))
		self.__alarmdeploy.ParseBuf(attrbuf)
		return self.__alarmdeploy

	def FormSetReq(self,ad,sesid=None,seqid=None):
		if not isinstance(ad,AlarmScheduleTimeInfo):
			raise AlarmDeployInvalidError('ad parameter not AlarmScheduleTimeInfo')
		
		rbuf = ''
		rbuf += self.TypeCodeForm(TYPE_ALMDEPLOY,ad.FormatBuf())
		return self.FormatSysCp(SYSCODE_SET_ALMDEPLOY_REQ,1,rbuf,sesid,seqid)

	def ParseSetRsp(self,buf):
		rbuf = self.UnPackSysCp(buf)
		if self.Code() != SYSCODE_SET_ALMDEPLOY_RSP:
			raise AlarmConfigInvalidError('code (%d) != SYSCODE_SET_ALMDEPLOY_RSP(%d)'%(self.Code(),SYSCODE_SET_ALMDEPLOY_RSP))
		rbuf = self.MessageCodeParse(rbuf)
		return rbuf

