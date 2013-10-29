#! python

'''
	this is the file for the ptzpreset get and set
'''

import struct

import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..')))
import xunit.utils.exception
import xunit.extlib.sdkproto.syscp as syscp

TYPE_PTZPRESET=18
STRUCT_PTZPRESET_SIZE=136

SYSCODE_SET_PTZPRESET_REQ=1081
SYSCODE_SET_PTZPRESET_RSP=1082
SYSCODE_GET_PTZPRESET_REQ=1083
SYSCODE_GET_PTZPRESET_RSP=1084

class SdkPtzPresetInvalidError(xunit.utils.exception.XUnitException):
	pass

class SdkPtzPresetOutRangeError(xunit.utils.exception.XUnitException):
	pass


class PtzPreset:
	def __ResetVar(self):
		self.__ptzid = 1
		# for preset 1 and set 
		self.__presetidx = 0x101 
		self.__presetname = ''
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
		if len(buf) < STRUCT_PTZPRESET_SIZE:
			raise SdkPtzPresetInvalidError('len(%d) < %d'%((len(buf),STRUCT_PTZPRESET_SIZE)))
		self.__ptzid,self.__presetidx = struct.unpack('>II',buf[:8])
		self.__presetname = self.GetString(buf[8:],128)
		return buf[STRUCT_PTZPRESET_SIZE:]

	def FormatBuf(self):
		rbuf = ''
		rbuf = struct.pack('>II',self.__ptzid,self.__presetidx)
		rbuf += self.FormatString(self.__presetname,128)
		return rbuf

	def __Format(self):
		rbuf = ''
		rbuf += 'ptzid         : %d\n'%(self.__ptzid)
		rbuf += 'presetidx     : 0x%x\n'%(self.__presetidx)
		rbuf += 'presetname    : (%s)\n'%(self.__presetname)
		return rbuf

	def __str__(self):
		return self.__Format()

	def __repr__(self):
		return self.__Format()

	def PtzId(self,val=None):
		ov = self.__ptzid
		if val is not None:
			self.__ptzid = val
		return ov

	def PresetIdx(self,val=None):
		ov = self.__presetidx
		if val is not None:
			self.__presetidx = val
		return ov

	def PresetName(self,val=None):
		ov = self.__presetname
		if val is not None:
			self.__presetname = val
		return ov


class SdkPtzPreset(syscp.SysCP):
	def __init__(self):
		syscp.SysCP.__init__(self)
		self.__presets = []
		return
	def __del__(self):
		syscp.SysCP.__del__(self)
		self.__presets = []
		return

	def FormatSetReq(self,preset,sesid=None,seqid=None):
		if preset is None or not isinstance(preset,PtzPreset):
			raise SdkPtzPresetInvalidError('preset parameter not PtzPreset Class')
		rbuf = preset.FormatBuf()
		reqbuf = self.TypeCodeForm(TYPE_PTZPRESET,rbuf)
		return self.FormatSysCp(SYSCODE_SET_PTZPRESET_REQ,1,reqbuf,sesid,seqid)

	def ParseSetRsp(self,rbuf):
		attrbuf = self.UnPackSysCp(buf)
		if self.Code() != SYSCODE_SET_PTZPRESET_RSP:
			raise SdkPtzPresetInvalidError('code (%d) != (%d)'%(self.Code(),SYSCODE_SET_PTZPRESET_RSP))

		if self.AttrCount() != 1:
			raise SdkPtzPresetInvalidError('attrcount (%d) != (1)'%(self.AttrCount()))

		self.MessageCodeParse(attrbuf,'PtzPreset Set Resp')
		return

	def FormatGetReq(self,ptzid,sesid=None,seqid=None):
		rbuf = struct.pack('>I',ptzid)
		reqbuf = self.TypeCodeForm(syscp.TYPE_INTVALUE,rbuf)
		sbuf =  self.FormatSysCp(SYSCODE_GET_PTZPRESET_REQ,1,reqbuf,sesid,seqid)
		return sbuf

	def ParseGetRsp(self,rbuf):
		attrbuf = self.UnPackSysCp(buf)
		if self.Code() != SYSCODE_GET_PTZPRESET_RSP:
			raise SdkPtzPresetInvalidError('code (%d) != (%d)'%(self.Code(),SYSCODE_GET_PTZPRESET_RSP))

		if self.AttrCount() < 1:
			raise SdkPtzPresetInvalidError('attrcount (%d) < 1'%(self.AttrCount()))

		self.__presets = []		
		for i in xrange(self.AttrCount()):
			p = PtzPreset()
			attrbuf = p.ParseBuf(attrbuf)
			self.__presets.append(p)
		return self.__presets

