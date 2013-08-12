#! python

'''
	this is the file for workstate get
'''

import struct

import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..')))
import xunit.utils.exception
import xunit.extlib.sdkproto.syscp as syscp

TYPE_WORK_STATE=111
TYPE_WORK_STATE_STRUCT_LENGTH=376
TYPE_WORK_STATE_LENGTH=(TYPE_WORK_STATE_STRUCT_LENGTH+4)

SYSCODE_GET_DEVICE_WORK_STATE_REQ=1191
SYSCODE_GET_DEVICE_WORK_STATE_RSP=1192

STREAM_CONNECT_MAX_NUM=16
MAX_STREAM_IDS=4
MAX_ALARM_OUT=16
MAX_ALARM_IN=16

class WorkStateInvalidError(xunit.utils.exception.XUnitException):
	pass


class ClientIp:
	def __init__(self,num):
		self.__ip = 0
		self.__num = num
		return

	def __del__(self):
		self.__ip = 0
		self.__num = 0
		return

	def __Format(self):
		rbuf = ''
		rbuf += '[%d]ip      : (0x%08x)\n'%(self.__num,self.__ip)
		return rbuf

	def __str__(self):
		return self.__Format()

	def __repr__(self):
		return self.__Format()

	def ParseBuf(self,buf):
		if len(buf) < 4:
			raise WorkStateInvalidError('at[%d] len(%d) < 4'%(self.__num,len(buf)))

		self.__ip = struct.unpack('>I',buf[:4])[0]
		return buf[4:]

	def FormatBuf(self):
		rbuf = ''
		rbuf += struct.pack('>I',self.__ip)
		return rbuf

class StreamState:
	def __init__(self,streamid):
		self.__streamid = streamid
		self.__recordstatic = 1
		self.__videosignalstatic = 0
		self.__reserv1 = 0
		self.__reserv2 = 0
		self.__bitrate = 0
		self.__linknum = 0
		self.__ips = []
		for i in xrange(STREAM_CONNECT_MAX_NUM):
			self.__ips.append(ClientIp(i))
		return

	def __del__(self):
		self.__streamid = streamid
		self.__recordstatic = 1
		self.__videosignalstatic = 0
		self.__reserv1 = 0
		self.__reserv2 = 0
		self.__bitrate = 0
		self.__linknum = 0
		self.__ips = []
		for i in xrange(STREAM_CONNECT_MAX_NUM):
			self.__ips.append(ClientIp(i))
		return

	def __Format(self):
		rbuf = ''
		rbuf += 'streamid             : (%d)\n'%(self.__streamid)
		rbuf += 'recordstatic         : (%d)\n'%(self.__recordstatic)
		rbuf += 'videosignalstatic    : (%d)\n'%(self.__videosignalstatic)
		rbuf += 'reserv1              : (%d)\n'%(self.__reserv1)
		rbuf += 'reserv2              : (%d)\n'%(self.__reserv2)
		rbuf += 'bitrate              : (%d)\n'%(self.__bitrate)
		rbuf += 'linknum              : (%d)\n'%(self.__linknum)
		for i in xrange(len(self.__ips)):
			rbuf += str(self.__ips[i])
		return rbuf

	def __str__(self):
		return self.__Format()
	def __repr__(self):
		return self.__Format()

	def ParseBuf(self,buf):
		if len(buf) < 80:
			raise WorkStateInvalidError('len(%d) < 80'%(len(buf)))
		self.__streamid = struct.unpack('>III',buf[:4])[0]
		self.__recordstatic=ord(buf[4])
		self.__videosignalstatic=ord(buf[5])
		self.__reserv1 = ord(buf[6])
		self.__reserv2 = ord(buf[7])
		self.__bitrate ,self.__linknum = struct.unpack('>II',buf[8:12])
		rbuf = buf[12:]
		self.__ips = []
		for i in xrange(STREAM_CONNECT_MAX_NUM):
			cip = ClientIp(i)
			rbuf = cip.ParseBuf(rbuf)
			self.__ips.append(cip)
		return rbuf

class DiskState:
	def __init__(self):
		self.__volume = 0
		self.__freespace = 0
		self.__diskstatic = 0
		return

	def __del__(self):
		self.__volume = 0
		self.__freespace = 0
		self.__diskstatic = 0
		return

	def __Format(self):
		rbuf = ''
		rbuf += 'volume               : (%d)\n'%(self.__volume)
		rbuf += 'freespace            : (%d)\n'%(self.__freespace)
		rbuf += 'diskstatic           : (%d)\n'%(self.__diskstatic)
		return rbuf

	def __str__(self):
		return self.__Format()
	def __repr__(self):
		return self.__Format()

	def ParseBuf(self,buf):
		if len(buf) < 12:
			raise WorkStateInvalidError('len(%d) < 12'%(len(buf)))
		self.__volume,self.__freespace,self.__diskstatic = struct.unpack('>III',buf[:12])
		return buf[12:]

class AlarmInState:
	def __init__(self,num):
		self.__num = num
		self.__static = 0
		return

	def __del__(self):
		self.__num = 0
		self.__static = 0
		return

	def __Format(self):
		rbuf = ''
		rbuf += '[%d]alarmin          : (%d)\n'%(self.__num,self._static)
		return rbuf

	def __str__(self):
		return self.__Format()
	def __repr__(self):
		return self.__Format()

	def ParseBuf(self,buf):
		if len(buf) < 4:
			raise WorkStateInvalidError('len(%d) < 4'%(len(buf)))
		self.__static = struct.unpack('>I',buf[:4])[0]
		return buf[4:]


class AlarmOutState:
	def __init__(self,num):
		self.__num = num
		self.__static = 0
		return

	def __del__(self):
		self.__num = 0
		self.__static = 0
		return

	def __Format(self):
		rbuf = ''
		rbuf += '[%d]alarmout         : (%d)\n'%(self.__num,self._static)
		return rbuf

	def __str__(self):
		return self.__Format()
	def __repr__(self):
		return self.__Format()

	def ParseBuf(self,buf):
		if len(buf) < 4:
			raise WorkStateInvalidError('len(%d) < 4'%(len(buf)))
		self.__static = struct.unpack('>I',buf[:4])[0]
		return buf[4:]


class WorkState:
	def __init__(self):
		self.__devicestatic = 0
		self.__streams = []
		for i in xrange(MAX_STREAM_IDS):
			self.__streams.append(StreamState(i))
		self.__diskstate = DiskState()
		self.__ins = []
		for i in xrange(MAX_ALARM_IN):
			self.__ins.append(AlarmInState(i))

		self.__outs = []
		for i in xrange(MAX_ALARM_OUT):
			self.__outs.append(AlarmOutState(i))
		self.__localdisplay = 0
		return

	def __del__(self):
		self.__devicestatic = 0
		self.__streams = []
		for i in xrange(MAX_STREAM_IDS):
			self.__streams.append(StreamState(i))
		self.__diskstate = DiskState()
		self.__ins = []
		for i in xrange(MAX_ALARM_IN):
			self.__ins.append(AlarmInState(i))

		self.__outs = []
		for i in xrange(MAX_ALARM_OUT):
			self.__outs.append(AlarmOutState(i))
		self.__localdisplay = 0
		return

	def __Format(self):
		rbuf = ''
		rbuf += 'devicestatic         : (%d)\n'%(self.__devicestatic)
		for i in xrange(len(self.__streams)):
			rbuf += str(self.__streams[i])

		rbuf += str(self.__diskstate)
		for i in xrange(len(self.__ins)):
			rbuf += str(self.__ins[i])

		for i in xrange(len(self.__outs)):
			rbuf += str(self.__outs[i])

		rbuf += 'localdisplay         : (%d)\n'%(self.__localdisplay)
		return rbuf
	def __str__(self):
		return self.__Format()
	def __repr__(self):
		return self.__Format()

	def ParseBuf(self,buf):
		if len(buf) < TYPE_WORK_STATE_STRUCT_LENGTH:
			raise WorkStateInvalidError('len(%d) < (%d)'%(len(buf),TYPE_WORK_STATE_STRUCT_LENGTH))
		self.__devicestatic = struct.unpack('>I',buf[:4])[0]
		rbuf = buf[4:]
		self.__streams = []
		for i in xrange(MAX_STREAM_IDS):
			sstate = StreamState(i)
			rbuf = sstate.ParseBuf(rbuf)
			self.__streams.append(sstate)

		self.__diskstate = DiskState()
		rbuf = self.__diskstate.ParseBuf(rbuf)
		self.__ins = []
		for i in xrange(MAX_ALARM_IN):
			alarmin = AlarmInState(i)
			rbuf = alarmin.ParseBuf(rbuf)
			self.__ins.append(alarmin)

		self.__outs = []
		for i in xrange(MAX_ALARAM_OUT):
			alarmout = AlarmOutState(i)
			rbuf = alarmout.ParseBuf(rbuf)
			self.__outs.append(alarmout)
		self.__localdisplay = struct.unpack('>I',rbuf[:4])[0]		
		return rbuf[4:]


class SdkWorkState(syscp.SysCP):
	def __init__(self):
		syscp.SysCP.__init__(self)
		self.__workstate = None
		return
	def __del__(self):
		syscp.SysCP.__del__(self)
		self.__workstate = None
		return

	def FormGetWorkStateReq(self,sesid=None,seqid=None):
		return self.FormatSysCp(SYSCODE_GET_DEVICE_WORK_STATE_REQ,0,'',sesid,seqid)

	def ParseGetWorkStateRsp(self,buf):
		attrbuf = self.UnPackSysCp(buf)
		if self.Code() != SYSCODE_GET_DEVICE_WORK_STATE_RSP:
			raise NetworkPortInvalidError('Code (%d) != (%d)'%(self.Code(),SYSCODE_GET_DEVICE_WORK_STATE_RSP))
		if self.AttrCount() != 1:
			raise NetworkPortInvalidError('attrcount (%d) != 1'%(self.AttrCount()))

		attrbuf = self.ParseTypeCode(attrbuf)
		if self.TypeCode() != TYPE_WORK_STATE:
			raise NetworkPortInvalidError('typecode (%d) != (%d)'%(self.TypeCode(),TYPE_WORK_STATE))
		self.__workstate = WorkState()
		self.__workstate.ParseBuf(attrbuf)
		return self.__workstate
		
	
