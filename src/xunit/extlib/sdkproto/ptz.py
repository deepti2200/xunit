#! python

'''
	this is the file for the ptz get and set
'''

import struct

import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..')))
import xunit.utils.exception
import xunit.extlib.sdkproto.syscp as syscp

class SdkPtzInvalidError(xunit.utils.exception.XUnitException):
	pass

class SdkPtzOutRangeError(xunit.utils.exception.XUnitException):
	pass

SYSCODE_CTL_PTZ_REQ=1077
SYSCODE_CTL_PTZ_RSP=1078

SYSCODE_SET_PTZPRESET_REQ=1081
SYSCODE_SET_PTZPRESET_RSP=1082
SYSCODE_GET_PTZPRESET_REQ=1083
SYSCODE_GET_PTZPRESET_RSP=1084

SYS_PTZCMD_STOP=0
SYS_PTZCMD_ZOOM_TELE=1
SYS_PTZCMD_ZOOM_WIDE=2
SYS_PTZCMD_FOCUS_NEAR=3
SYS_PTZCMD_IRIS_LARGE=4
SYS_PTZCMD_IRIS_SMALL=5
SYS_PTZCMD_AUXON=6
SYS_PTZCMD_AUXOFF=7
SYS_PTZCMD_AUTOPANON=8
SYS_PTZCMD_AUTOPANOFF=9
SYS_PTZCMD_UP=10
SYS_PTZCMD_DOWN=11
SYS_PTZCMD_LEFT=12
SYS_PTZCMD_RIGHT=13
SYS_PTZCMD_RIGHTUP=14
SYS_PTZCMD_LEFTUP=15
SYS_PTZCMD_RIGHTDOWN=16
SYS_PTZCMD_LEFTDOWN=17
SYS_PTZCMD_GOTOPRESET=18
SYS_PTZCMD_SETPRESET=19
SYS_PTZCMD_CLEARPRESET=20
SYS_PTZCMD_LIGHT_ON=21
SYS_PTZCMD_LIGHT_OFF=22
SYS_PTZCMD_STARTTOUR=23
SYS_PTZCMD_STOPTOUR=24
SYS_PTZCMD_3DCONTROL=200
SYS_PTZCMD_NR=255

TYPE_CTLPTZ=17
TYPE_CTLPTZ_LENGTH=24

class SdkPtzInvalidError(xunit.utils.exception.XUnitException):
	pass


TYPE_PTZPRESET=18
PRESET_NAME_LENGTH=128
TYPE_PTZPRESET_LENGTH=(PRESET_NAME_LENGTH+4)
PRESET_PTZ_STRUCT_LENGTH=(PRESET_NAME_LENGTH+8)

class PtzPresetInvalidError(xunit.utils.exception.XUnitException):
	pass
class PtzPreset:
	def __init__(self):
		self.__ptzid = 1
		self.__presetidx = 0
		self.__presetname = ''
		return

	def __del__(self):
		self.__ptzid = 1
		self.__presetidx = 0
		self.__presetname = ''
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
		if len(buf) < PRESET_PTZ_STRUCT_LENGTH:
			raise PtzPresetInvalidError('len (%d) < (%d)'%(len(buf),PRESET_PTZ_STRUCT_LENGTH))

		self.__ptzid,self.__presetidx = struct.unpack('>II',buf[:8])
		self.__presetname = self.GetString(buf[8:],PRESET_NAME_LENGTH)			
		return buf[PRESET_PTZ_STRUCT_LENGTH:]

	def FormatBuf(self):
		rbuf = struct.pack('>II',self,__ptzid,self.__presetidx)
		rbuf += self.FormatString(self.__presetname,PRESET_NAME_LENGTH)
		return rbuf

	def __Format(self):
		rbuf = ''
		rbuf += 'ptzid     : %d\n'%(self.__ptzid)
		rbuf += 'presetidx : %d\n'%(self.__preseetidx)
		rbuf += 'presetname: %s\n'%(self.__presetname)
		return rbuf
	
	def __str__(self):
		return self.__Format()

	def __repr__(self):
		return self.__Format()

	def PtzId(self,val=None):
		ov = self.__ptzid
		if val:
			self.__ptzid = val
		return ov

	def PresetIdx(self,val=None):
		ov = self.__presetidx
		if val:
			self.__presetidx = val
		return ov

	def PresetName(self,val=None):
		ov = self.__presetname
		if val:
			self.__presetname = val
		return ov

class SdkPtz(syscp.SysCP):
	def __init__(self):
		syscp.SysCP.__init__(self)
		self.__presets = []
		return
	def __del__(self):
		syscp.SysCP.__del__(self)
		self.__presets = []
		return

	def __FormatPtzCommand(self,ptzid,cmd,param1=0,param2=0,param3=0,param4=0):
		bbuf = ''
		bbuf += struct.pack('>II',ptzid,cmd)
		bbuf += struct.pack('>IIII',param1,param2,param3,param4)
		rbuf = self.TypeCodeForm(TYPE_CTLPTZ,bbuf)
		return rbuf

	def UpPtz(self,ptzid,speed,sesid=None,seqid=None):
		seqbuf = self.__FormatPtzCommand(ptzid,SYS_PTZCMD_UP,speed)
		return self.FormatSysCp(SYSCODE_CTL_PTZ_REQ,1,seqbuf,sesid,seqid)

	def DownPtz(self,ptzid,speed,sesid=None,seqid=None):
		seqbuf = self.__FormatPtzCommand(ptzid,SYS_PTZCMD_DOWN,speed)
		return self.FormatSysCp(SYSCODE_CTL_PTZ_REQ,1,seqbuf,sesid,seqid)

	def RightPtz(self,ptzid,speed,sesid=None,seqid=None):
		seqbuf = self.__FormatPtzCommand(ptzid,SYS_PTZCMD_RIGHT,speed)
		return self.FormatSysCp(SYSCODE_CTL_PTZ_REQ,1,seqbuf,sesid,seqid)
		
	def LeftPtz(self,ptzid,speed,sesid=None,seqid=None):
		seqbuf = self.__FormatPtzCommand(ptzid,SYS_PTZCMD_LEFT,speed)
		return self.FormatSysCp(SYSCODE_CTL_PTZ_REQ,1,seqbuf,sesid,seqid)

	def UpLeftPtz(self,ptzid,speed,sesid=None,seqid=None):
		seqbuf = self.__FormatPtzCommand(ptzid,SYS_PTZCMD_LEFTUP,speed)
		return self.FormatSysCp(SYSCODE_CTL_PTZ_REQ,1,seqbuf,sesid,seqid)
		
	def UpRightPtz(self,ptzid,speed,sesid=None,seqid=None):
		seqbuf = self.__FormatPtzCommand(ptzid,SYS_PTZCMD_RIGHTUP,speed)
		return self.FormatSysCp(SYSCODE_CTL_PTZ_REQ,1,seqbuf,sesid,seqid)

	def DownLeftPtz(self,ptzid,speed,sesid=None,seqid=None):
		seqbuf = self.__FormatPtzCommand(ptzid,SYS_PTZCMD_LEFTDOWN,speed)
		return self.FormatSysCp(SYSCODE_CTL_PTZ_REQ,1,seqbuf,sesid,seqid)
		
	def DownRightPtz(self,ptzid,speed,sesid=None,seqid=None):
		seqbuf = self.__FormatPtzCommand(ptzid,SYS_PTZCMD_RIGHTDOWN,speed)
		return self.FormatSysCp(SYSCODE_CTL_PTZ_REQ,1,seqbuf,sesid,seqid)

	def StopPtz(self,ptzid,sesid=None,seqid=None):
		seqbuf = self.__FormatPtzCommand(ptzid,SYS_PTZCMD_STOP)
		return self.FormatSysCp(SYSCODE_CTL_PTZ_REQ,1,seqbuf,sesid,seqid)

	def SetPresetPtz(self,ptzid,presetidx,sesid=None,seqid=None):
		seqbuf = self.__FormatPtzCommand(ptzid,SYS_PTZCMD_SETPRESET,presetidx)
		return self.FormatSysCp(SYSCODE_CTL_PTZ_REQ,1,seqbuf,sesid,seqid)


	def GotoPresetPtz(self,ptzid,presetidx,sesid=None,seqid=None):
		seqbuf = self.__FormatPtzCommand(ptzid,SYS_PTZCMD_GOTOPRESET,presetidx)
		return self.FormatSysCp(SYSCODE_CTL_PTZ_REQ,1,seqbuf,sesid,seqid)

	def ClearPresetPtz(self,ptzid,presetidx,sesid=None,seqid=None):
		seqbuf = self.__FormatPtzCommand(ptzid,SYS_PTZCMD_CLEARPRESET,presetidx)
		return self.FormatSysCp(SYSCODE_CTL_PTZ_REQ,1,seqbuf,sesid,seqid)


	def PtzCtrlResp(self,buf):
		attrbuf = self.UnPackSysCp(buf)
		if self.Code() != SYSCODE_CTL_PTZ_RSP:
			raise SdkPtzInvalidError('code (%d) != (%d)'%(self.Code(),SYSCODE_CTL_PTZ_RSP))
		if self.AttrCount() != 1:
			raise SdkPtzInvalidError('attrcount (%d) != (1)'%(self.AttrCount()))

		self.MessageCodeParse(attrbuf,'Ptz cmd')
		return


	def PtzPresetSetReq(self,ptzpreset,sesid=None,seqid=None):
		if not isinstance(ptzpreset,PtzPreset):
			raise SdkPtzInvalidError('param not sdkproto.ptz.PtzPreset class')
		rbuf = ptzpreset.FormatBuf()
		reqbuf = self.TypeCodeForm(TYPE_PTZPRESET,rbuf)
		return self.FormatSysCp(SYSCODE_SET_PTZPRESET_REQ,1,reqbuf,sesid,seqid)

	def PtzPresetSetResp(self,buf):
		attrbuf = self.UnPackSysCp(buf)
		if self.Code() != SYSCODE_SET_PTZPRESET_RSP:
			raise SdkPtzInvalidError('code (%d) != (%d)'%(self.Code(),SYSCODE_SET_PTZPRESET_RE))

		if self.AttrCount() != 1:
			raise SdkPtzInvalidError('attrcount (%d) != (1)'%(self.AttrCount()))

		self.MessageCodeParse(attrbuf,'PtzPreset Set Resp')
		return

	def PtzPresetGetReq(self,ptzid,sesid=None,seqid=None):
		rbuf = struct.pack('>I',ptzid)
		reqbuf = self.TypeCodeForm(syscp.TYPE_INTVALUE,rbuf)
		return self.FormatSysCp(SYSCODE_GET_PTZPRESET_REQ,1,reqbuf,sesid,seqid)

	def PtzPresetGetResp(self,buf):
		attrbuf = self.UnPackSysCp(buf)
		if self.Code() != SYSCODE_GET_PTZPRESET_RSP:
			raise SdkPtzInvalidError('code (%d) != (%d)'%(self.Code(),SYSCODE_GET_PTZPRESET_RE))

		self.__presets = []
		for i in xrange(self.AttrCount()):
			attrbuf = self.ParseTypeCode(attrbuf)
			if self.TypeCode() != TYPE_PTZPRESET:
				raise SdkPtzInvalidError('typecode (%d) != (%d)'%(self.TypeCode(),TYPE_PTZPRESET))
			if self.TypeLen() != TYPE_PTZPRESET_LENGTH:
				raise SdkPtzInvalidError('typelen (%d) != (%d)'%(self.TypeLen(),TYPE_PTZPRESET_LENGTH))
			ptzpreset = PtzPreset()
			attrbuf = ptzpreset.ParseBuf(attrbuf)
			self.__presets.append(ptzpreset)

		return self.__presets
