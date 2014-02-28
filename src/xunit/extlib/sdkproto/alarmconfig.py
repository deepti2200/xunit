#! python

'''
this is the file for alarm config
'''

import struct

import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..')))
import xunit.utils.exception
import xunit.extlib.sdkproto.syscp as syscp

ALARM_EXT_INFO_SIZE=20
ALARM_IN_CONFIG_SIZE=88
ALARM_OUT_CONFIG_SIZE=64
PIR_DECT_DATA_SIZE=24
ALARM_EVENT_CONFIG_SIZE=76
ALARM_CONFIG_SIZE=16


SYSCODE_SET_ALMCFG_REQ=1151
SYSCODE_SET_ALMCFG_RSP=1152
SYSCODE_GET_ALMCFG_REQ=1153
SYSCODE_GET_ALMCFG_RSP=1154

TYPE_GET_ALMCONFIG=127
TYPE_ALARM_IN=123
TYPE_ALARM_OUT=124
TYPE_ALARM_EVENT=125

class AlarmConfigInvalidError(xunit.utils.exception.XUnitException):
	pass



class AlarmExtInfo:
	def __ResetVar(self):
		self.__ionum = 0
		self.__operatecmd = 0
		self.__operateseqnum = 0
		self.__ptzdelaytime = 0
		self.__delaytime = 0
		self.__reserv1 = '\0' * 12
		return

	def __init__(self):
		self.__ResetVar()
		return

	def __del__(self):
		self.__ResetVar()
		return

	def ParseBuf(self,buf):
		if len(buf) < ALARM_EXT_INFO_SIZE:
			raise AlarmConfigInvalidError('buf(%d) < ALARM_EXT_INFO_SIZE(%d)'%(len(buf),ALARM_EXT_INFO_SIZE))
		logging.info('buf(%s)'%(repr(buf[:ALARM_EXT_INFO_SIZE])))
		self.__ionum = ord(buf[0])
		self.__operatecmd = ord(buf[1])
		self.__operateseqnum,self.__ptzdelaytime,self.__delaytime = struct.unpack('>HHH',buf[2:8])
		self.__reserv1 = buf[8:20]
		return buf[ALARM_EXT_INFO_SIZE:]

	def FormatBuf(self):
		rbuf = ''
		rbuf += chr(self.__ionum)
		rbuf += chr(self.__operatecmd)
		rbuf += struct.pack('>HHH',self.__operateseqnum,self.__ptzdelaytime,self.__delaytime)
		rbuf += self.__reserv1
		logging.info('rbuf(%s)'%(repr(rbuf)))
		return rbuf

	def __Format(self):
		rbuf = 'AlarmExtInfo:\n'
		rbuf += 'ionum                   :(%d)\n'%(self.__ionum)
		rbuf += 'operatecmd          :(%d)\n'%(self.__operatecmd)
		rbuf += 'operateseqnum     :(%d)\n'%(self.__operateseqnum)
		rbuf += 'ptzdelaytime         :(%d)\n'%(self.__ptzdelaytime)
		rbuf += 'delaytime              :(%d)\n'%(self.__delaytime)
		rbuf += 'reserv1                 :(%s)\n'%(repr(self.__reserv1))
		return rbuf

	def __str__(self):
		return self.__Format()

	def __repr__(self):
		return self.__Format()

	def IoNum(self,val=None):
		ov = self.__ionum
		if val is not None:
			self.__ionum = val
		return ov

	def OperateCmd(self,val=None):
		ov = self.__operatecmd
		if val is not None:
			self.__operatecmd = val
		return ov

	def OperateSeqNum(self,val=None):
		ov = self.__operateseqnum
		if val is not None:
			self.__operateseqnum = val
		return ov
	def PtzDelayTime(self,val=None):
		ov = self.__ptzdelaytime
		if val is not None:
			self.__ptzdelaytime = val
		return ov

	def DelayTime(self,val=None):
		ov = self.__delaytime
		if val is not None:
			self.__delaytime = val
		return ov

	def Reserv1(self,val=None):
		ov = self.__reserv1
		if val is not None:
			self.__reserv1 = val
		return ov

class AlarmInConfig:
	def __ResetVar(self):
		self.__enableflag = 0
		self.__inputnumber = 0
		self.__name = ''
		self.__checktime = 0
		self.__normalstatus = 0
		self.__linkalarmstrategy = 0
		self.__linkalarmextinfo = AlarmExtInfo()
		self.__reserv1 = '\0' * 16
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
		if len(buf) < ALARM_IN_CONFIG_SIZE:
			raise AlarmConfigInvalidError('buf(%d) < ALARM_IN_CONFIG_SIZE(%d)'%(len(buf),ALARM_IN_CONFIG_SIZE))
		self.__enableflag,self.__inputnumber = struct.unpack('>II',buf[:8])
		self.__name = self.GetString(buf[8:40],32)
		self.__checktime,self.__normalstatus,self.__linkalarmstrategy = struct.unpack('>III',buf[40:52])
		self.__linkalarmextinfo = AlarmExtInfo()
		self.__linkalarmextinfo.ParseBuf(buf[52:])
		self.__reserv1 = buf[72:ALARM_IN_CONFIG_SIZE]
		return buf[ALARM_IN_CONFIG_SIZE:]

	def FormatBuf(self):
		rbuf = ''
		rbuf += struct.pack('>II',self.__enableflag,self.__inputnumber)
		rbuf += self.FormatString(self.__name,32)
		rbuf += struct.pack('>III',self.__checktime,self.__normalstatus,self.__linkalarmstrategy)
		rbuf += self.__linkalarmextinfo.FormatBuf()
		rbuf += self.__reserv1
		return rbuf

	def __Format(self):
		rbuf = 'AlarmInConfig:\n'
		rbuf += 'enableflag                :(%d)\n'%(self.__enableflag)
		rbuf += 'inputnumber             :(%d)\n'%(self.__inputnumber)
		rbuf += 'name                       :(%s)\n'%(self.__name)
		rbuf += 'checktime                :(%d)\n'%(self.__checktime)
		rbuf += 'normalstatus            :(%d)\n'%(self.__normalstatus)
		rbuf += 'linkalarmstrategy     :(%d)\n'%(self.__linkalarmstrategy)
		rbuf += str(self.__linkalarmextinfo)
		rbuf += 'reserv1                    :(%s)\n'%(repr(self.__reserv1))
		return rbuf

	def __str__(self):
		return self.__Format()

	def __repr__(self):
		return self.__Format()

	def EnableFlag(self,val=None):
		ov = self.__enableflag
		if val is not None:
			self.__enableflag = val
		return ov
	def InputNumber(self,val=None):
		ov = self.__inputnumber
		if val is not None:
			self.__inputnumber = val
		return ov
	def Name(self,val=None):
		ov = self.__name
		if val is not None:
			self.__name = val
		return ov
	def CheckTime(self,val=None):
		ov = self.__checktime
		if val is not None:
			self.__checktime = val
		return ov
	def NormalStatus(self,val=None):
		ov = self.__normalstatus
		if val is not None:
			self.__normalstatus = val
		return ov
	def LinkAlarmStrategy(self,val=None):
		ov = self.__linkalarmstrategy
		if val is not None:
			self.__linkalarmstrategy = val
		return ov
	def ExtInfoIoNum(self,val=None):
		return self.__linkalarmextinfo.IoNum(val)
	def ExtInfoOperateCmd(self,val=None):
		return self.__linkalarmextinfo.OperateCmd(val)
	def ExtInfoOperateSeqNum(self,val=None):
		return self.__linkalarmextinfo.OperateSeqNum(val)
	def ExtInfoPtzDelayTime(self,val=None):
		return self.__linkalarmextinfo.PtzDelayTime(val)
	def ExtInfoDelayTime(self,val=None):
		return self.__linkalarmextinfo.DelayTime(val)
	def ExtInfoReserv1(self,val=None):
		return self.__linkalarmextinfo.Reserv1(val)
	


class AlarmOutConfig:
	def __ResetVar(self):
		self.__enableflag = 0
		self.__outputnumber = 0
		self.__name = ''
		self.__normalstatus = 0
		self.__delaytime = 0
		self.__reserv1 = '\0'*16
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
		if len(buf) < ALARM_OUT_CONFIG_SIZE:
			raise AlarmConfigInvalidError('buf(%d) < ALARM_OUT_CONFIG_SIZE(%d)'%(len(buf),ALARM_OUT_CONFIG_SIZE))
		self.__enableflag ,self.__outputnumber = struct.unpack('>II',buf[:8])
		self.__name = self.GetString(buf[8:40],32)
		self.__normalstatus,self.__delaytime = struct.unpack('>II',buf[40:48])
		self.__reserv1 = buf[48:64]
		return buf[ALARM_OUT_CONFIG_SIZE:]

	def FormatBuf(self):
		rbuf = ''
		rbuf += struct.pack('>II',self.__enableflag,self.__outputnumber)
		rbuf += self.FormatString(self.__name,32)
		rbuf += struct.pack('>II',self.__normalstatus,self.__delaytime)
		rbuf += self.__reserv1
		return rbuf

	def __Format(self):
		rbuf = 'AlarmOutConfig:\n'
		rbuf += 'enableflag          :(%d)\n'%(self.__enableflag)
		rbuf += 'outputnumber    :(%d)\n'%(self.__outputnumber)
		rbuf += 'name                 :(%s)\n'%(self.__name)
		rbuf += 'normalstatus      :(%d)\n'%(self.__normalstatus)
		rbuf += 'delaytime           :(%d)\n'%(self.__delaytime)
		rbuf += 'reserv1              :(%s)\n'%(repr(self.__reserv1))
		return rbuf

	def __str__(self):
		return self.__Format()

	def __repr__(self):
		return self.__Format()

	
	def EnableFlag(self,val=None):
		ov = self.__enableflag
		if val is not None:
			self.__enableflag = val
		return ov
	def OutputNumber(self,val=None):
		ov = self.__outputnumber
		if val is not None:
			self.__outputnumber = val
		return ov
	def Name(self,val=None):
		ov = self.__name
		if val is not None:
			self.__name = val
		return ov
	def NormalStatus(self,val=None):
		ov = self.__normalstatus
		if val is not None:
			self.__normalstatus = val
		return ov
	def DelayTime(self,val=None):
		ov = self.__delaytime
		if val is not None:
			self.__delaytime = val
		return ov
	def Reserv1(self,val=None):
		ov = self.__reserv1
		if val is not None:
			self.__reserv1 = val
		return ov

class PIRDectData:
	def __ResetVar(self):
		self.__sensitive = 0
		self.__reserv1 = '\0' * 20
		return

	def __init__(self):
		self.__ResetVar()
		return

	def __del__(self):
		self.__ResetVar()
		return

	def ParseBuf(self,buf):
		if  len(buf) < PIR_DECT_DATA_SIZE:
			raise AlarmConfigInvalidError('buf(%d) < PIR_DECT_DATA_SIZE(%d)'%(len(buf),PIR_DECT_DATA_SIZE))
		self.__sensitive = struct.unpack('>I',buf[:4])[0]
		self.__reserv1 = buf[4:PIR_DECT_DATA_SIZE]
		return buf[PIR_DECT_DATA_SIZE:]

	def FormatBuf(self):
		rbuf = ''
		rbuf += struct.pack('>I',self.__sensitive)
		rbuf += self.__reserv1
		return rbuf

	def __Format(self):
		rbuf = 'PIDectectData:\n'
		rbuf += 'sensitive          :(%d)\n'%(self.__sensitive)
		rbuf += 'reserv1            :(%s)\n'%(repr(self.__reserv1))
		return rbuf

	def __str__(self):
		return self.__Format()
	def __repr__(self):
		return self.__Format()

	def Sensitive(self,val=None):
		ov = self.__sensitive
		if val is not None:
			self.__sensitive = val
		return ov
	def Reserv1(self,val=None):
		ov = self.__reserv1
		if val is not None:
			self.__reserv1 = val
		return ov

class AlarmEventConfig:
	def __ResetVar(self):
		self.__alarmid = 0
		self.__enableflag = 0
		self.__checktime = 0
		self.__linkalarmstrategy = 0
		self.__alarmunionextdata = PIRDectData()
		self.__linkalarmextinfo = AlarmExtInfo()
		self.__reserv1 = '\0' * 16
		return 

	def __init__(self):
		self.__ResetVar()
		return

	def __del__(self):
		self.__ResetVar()
		return

	def ParseBuf(self,buf):
		if len(buf) < ALARM_EVENT_CONFIG_SIZE:
			raise AlarmConfigInvalidError('buf(%d) < ALARM_EVENT_CONFIG_SIZE(%d)'%(len(buf),ALARM_EVENT_CONFIG_SIZE))
		self.__alarmid,self.__enableflag,self.__checktime,self.__linkalarmstrategy = struct.unpack('>IIII',buf[:16])
		
		rbuf = self.__alarmunionextdata.ParseBuf(buf[16:])
		rbuf = self.__linkalarmextinfo.ParseBuf(rbuf)
		self.__reserv1 = rbuf[:16]
		return rbuf[16:]

	def FormatBuf(self):
		rbuf = ''
		rbuf += struct.pack('>IIII',self.__alarmid,self.__enableflag,self.__checktime,self.__linkalarmstrategy)
		rbuf += self.__alarmunionextdata.FormatBuf()
		rbuf += self.__linkalarmextinfo.FormatBuf()
		rbuf += self.__reserv1
		return rbuf

	def __Format(self):
		rbuf = 'AlarmEventConfig:\n'
		rbuf += 'alarmid                    :(%d)\n'%(self.__alarmid)
		rbuf += 'enableflag                :(%d)\n'%(self.__enableflag)
		rbuf += 'checktime                :(%d)\n'%(self.__checktime)
		rbuf += 'linkalarmstrategy     :(%d)\n'%(self.__linkalarmstrategy)
		rbuf += str(self.__alarmunionextdata)
		rbuf += str(self.__linkalarmextinfo)
		rbuf += 'reserv1                    :(%s)\n'%(repr(self.__reserv1))
		return rbuf

	def __str__(self):
		return self.__Format()

	def __repr__(self):
		return self.__Format()

	def AlarmId(self,val=None):
		ov = self.__alarmid
		if val is not None:
			self.__alarmid = val
		return ov
	def EnableFlag(self,val=None):
		ov = self.__enableflag
		if val is not None:
			self.__enableflag = val
		return ov
	def CheckTime(self,val=None):
		ov = self.__checktime
		if val is not None:
			self.__checktime = val
		return ov
	def LinkAlarmStrategy(self,val=None):
		ov = self.__linkalarmstrategy
		if val is not None:
			self.__linkalarmstrategy = val
		return ov
	def UnionSensitive(self,val=None):
		return self.__alarmunionextdata.Sensitive(val)
	def UnionReserv1(self,val=None):
		return self.__alarmunionextdata.Reserv1(val)
	def ExtInfoIoNum(self,val=None):
		return self.__linkalarmextinfo.IoNum(val)
	def ExtInfoOperateCmd(self,val=None):
		return self.__linkalarmextinfo.OperateCmd(val)
	def ExtInfoOperateSeqNum(self,val=None):
		return self.__linkalarmextinfo.OperateSeqNum(val)
	def ExtInfoPtzDelayTime(self,val=None):
		return self.__linkalarmextinfo.PtzDelayTime(val)
	def ExtInfoDelayTime(self,val=None):
		return self.__linkalarmextinfo.DelayTime(val)
	def ExtInfoReserv1(self,val=None):
		return self.__linkalarmextinfo.Reserv1(val)
	def Reserv1(self,val=None):
		ov = self.__reserv1
		if val is not None:
			self.__reserv1 = val
		return ov
class AlarmConfig:
	def __ResetVar(self):
		self.__alarmid  =0
		self.__idx = 0
		self.__reserv1 = '\0' * 8

	def __init__(self):
		self.__ResetVar()
		return

	def __del__(self):
		self.__ResetVar()
		return

	def ParseBuf(self,buf):
		if len(buf) < ALARM_CONFIG_SIZE:
			raise AlarmConfigInvalidError('buf(%d) < ALARM_CONFIG_SIZE(%d)'%(len(buf),ALARM_CONFIG_SIZE))
		self.__alarmid,self.__idx = struct.unpack('>II',buf[:8])
		self.__reserv1 = buf[8:16]
		return buf[ALARM_CONFIG_SIZE:]

	def FormatBuf(self):
		rbuf = ''
		rbuf += struct.pack('>II',self.__alarmid,self.__idx)
		rbuf += self.__reserv1
		return rbuf

	def __Format(self):
		rbuf = 'AlarmConfig:\n'
		rbuf += 'alarmid                :(%d)\n'%(self.__alarmid)
		rbuf += 'index                   :(%d)\n'%(self.__idx)
		rbuf += 'reserv1                :(%s)\n'%(repr(self.__reserv1))
		return rbuf

	def __str__(self):
		return self.__Format()

	def __repr__(self):
		return self.__Format()

	def AlarmId(self,val=None):
		ov = self.__alarmid
		if val is not None:
			self.__alarmid = val
		return ov
	def Index(self,val=None):
		ov = self.__idx
		if val is not None:
			self.__idx = val
		return ov
	def Reserv1(self,val=None):
		ov = self.__reserv1
		if val is not None:
			self.__reserv1 = val
		return ov
		
		
class SdkAlarmConfig(syscp.SysCP):
	def __init__(self):
		syscp.SysCP.__init__(self)
		self.__alarmconfigs = []
		return
	def __del__(self):
		syscp.SysCP.__del__(self)
		self.__alarmconfigs = []
		return

	def FormGetReq(self,alarmconfig,sesid=None,seqid=None):
		if not isinstance(alarmconfig,AlarmConfig):
			raise AlarmConfigInvalidError('alarmconfig parameter not AlarmConfig type')
		rbuf = alarmconfig.FormatBuf()
		reqbuf = self.TypeCodeForm(TYPE_GET_ALMCONFIG,rbuf)
		return self.FormatSysCp(SYSCODE_GET_ALMCFG_REQ,1,reqbuf,sesid,seqid)

	def ParseGetRsp(self,buf):
		#logging.info('buf (%s)'%(repr(buf)))
		attrbuf = self.UnPackSysCp(buf)
		if self.Code() != SYSCODE_GET_ALMCFG_RSP:
			raise AlarmConfigInvalidError('code(%d) != SYSCODE_GET_ALMCFG_RSP(%d)'%(self.Code(),SYSCODE_GET_ALMCFG_RSP))
		self.__alarmconfigs = []
		#logging.info('attr(%d) attrbuf(%s)'%(self.AttrCount(),repr(attrbuf)))
		for i in xrange(self.AttrCount()):
			attrbuf = self.ParseTypeCode(attrbuf)
			if self.TypeCode() == TYPE_ALARM_IN:
				alarmin = AlarmInConfig()
				attrbuf = alarmin.ParseBuf(attrbuf)
				self.__alarmconfigs.append(alarmin)
			elif self.TypeCode() == TYPE_ALARM_OUT:
				alarmout = AlarmOutConfig()
				attrbuf = alarmout.ParseBuf(attrbuf)
				self.__alarmconfigs.append(alarmout)
			elif self.TypeCode() == TYPE_ALARM_EVENT:
				alarmevent = AlarmEventConfig()
				attrbuf = alarmevent.ParseBuf(attrbuf)
				self.__alarmconfigs.append(alarmevent)
			else:
				raise AlarmConfigInvalidError('[%d]Typecode(%d) not valid'%(i,self.TypeCode()))
		return self.__alarmconfigs

	def FormSetReq(self,configs,sesid=None,seqid=None):
		rbuf = ''
		for c in configs:
			if isinstance(c,AlarmInConfig):
				rbuf += self.TypeCodeForm(TYPE_ALARM_IN,c.FormatBuf())
			elif isinstance(c,AlarmOutConfig):
				rbuf += self.TypeCodeForm(TYPE_ALARM_OUT,c.FormatBuf())
			elif isinstance(c,AlarmEventConfig):
				rbuf += self.TypeCodeForm(TYPE_ALARM_EVENT,c.FormatBuf())
			else:
				raise AlarmConfigInvalidError('config not valid types')
		#logging.info('attr(%d) rbuf(%s)'%(len(configs),repr(rbuf)))
		return self.FormatSysCp(SYSCODE_SET_ALMCFG_REQ,len(configs),rbuf,sesid,seqid)

	def ParseSetRsp(self,buf):
		rbuf = self.UnPackSysCp(buf)
		if self.Code() != SYSCODE_SET_ALMCFG_RSP:
			raise AlarmConfigInvalidError('code (%d) != (%d)'%(self.Code(),SYSCODE_SET_ALMCFG_RSP))
		rbuf = self.MessageCodeParse(rbuf)
		return rbuf

	
