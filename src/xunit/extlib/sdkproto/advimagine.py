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


SYSCODE_GET_ADVANCED_IMAGING_REQ=1177
SYSCODE_GET_ADVANCED_IMAGING_RSP=1178
SYSCODE_SET_ADVANCED_IMAGING_REQ=1179
SYSCODE_SET_ADVANCED_IMAGING_RSP=1180

TYPE_ADVANCED_IMAGING=110
TYPE_ADVANCED_IMAGING_STRUCT_LENGTH=36
TYPE_ADVANCED_IMAGING_LENGTH=(TYPE_ADVANCED_IMAGING_STRUCT_LENGTH+4)

class AdvImagineInvalidError(xunit.utils.exception.XUnitException):
	pass


class AdvImagine:
	def __init__(self):
		self.__videoid = 1
		self.__meteringmode = 0
		self.__backlightcompflag = 0
		self.__dcirisflag = 0
		self.__reserv1 = '\0' * 5
		self.__localexposure = 0
		self.__mctfstrength = 0
		self.__dcirisduty = 100
		self.__aetargetratio = 25
		self.__reserv2 = '\0' * 16
		return

	def __del__(self):
		self.__videoid = 1
		self.__meteringmode = 0
		self.__backlightcompflag = 0
		self.__dcirisflag = 0
		self.__reserv1 = '\0' * 5
		self.__localexposure = 0
		self.__mctfstrength = 0
		self.__dcirisduty = 100
		self.__aetargetratio = 25
		self.__reserv2 = '\0' * 16
		return

	def __Format(self):
		rbuf = ''
		rbuf += 'videoid                : %d\n'%(self.__videoid)
		rbuf += 'meteringmode           : %d\n'%(self.__meteringmode)
		rbuf += 'backlightcompflag      : %d\n'%(self.__backlightcompflag)
		rbuf += 'dcirisflag             : %d\n'%(self.__dcirisflag)
		rbuf += 'reserv1                : (%s)\n'%(repr(self.__reserv1))
		rbuf += 'localexposure          : %d\n'%(self.__localexposure)
		rbuf += 'mctfstrength           : %d\n'%(self.__mctfstrength)
		rbuf += 'dcirisduty             : %d\n'%(self.__dcirisduty)
		rbuf += 'aetargetratio          : %d\n'%(self.__aetargetratio)
		rbuf += 'reserv2                : (%s)\n'%(repr(self.__reserv2))
		return rbuf

	def __str__(self):
		return self.__Format()

	def __repr__(self):
		return self.__Format()


	def ParseBuf(self,buf):
		if len(buf) < TYPE_ADVANCED_IMAGING_STRUCT_LENGTH:
			raise AdvImagineInvalidError('len(%d) < (%d)'%(len(buf),TYPE_ADVANCED_IMAGING_STRUCT_LENGTH))

		self.__videoid = struct.unpack('>I',buf[:4])[0]
		self.__meteringmode = ord(buf[4])
		self.__backlightcompflag = ord(buf[5])
		self.__dcirisflag = ord(buf[6])
		self.__reserv1 = buf[7:12]
		self.__localexposure,self.__mctfstrength,self.__dcirisduty,self.__aetargetratio = struct.unpack('>HHHH',buf[12:20])
		self.__reserv2 = buf[20:TYPE_ADVANCED_IMAGING_STRUCT_LENGTH]

		return buf[TYPE_ADVANCED_IMAGING_STRUCT_LENGTH:]

	def FormatBuf(self):
		rbuf = ''
		rbuf += struct.pack('>I',self.__videoid)
		rbuf += chr(self.__meteringmode)
		rbuf += chr(self.__backlightcompflag)
		rbuf += chr(self.__dcirisflag)
		rbuf += self.__reserv1
		rbuf += struct.pack('>HHHH',self.__localexposure,self.__mctfstrength,self.__dcirisduty,self.__aetargetratio)
		rbuf += self.__reserv2
		return rbuf

	def VideoId(self,val=None):
		ov = self.__videoid
		if val is not None:
			self.__videoid = val
		return ov

	def MeteringMode(self,val=None):
		ov = self.__meteringmode
		if val is not None:
			self.__meteringmode = val
		return ov

	def BackLightCompFlag(self,val=None):
		ov = self.__backlightcompflag
		if val is not None:
			self.__backlightcompflag = val
		return ov
		
	def DcIrisFlag(self,val=None):
		ov = self.__dcirisflag
		if val is not None:
			self.__dcirisflag = val
		return ov
	def LocalExposure(self,val=None):
		ov = self.__localexposure
		if val is not None:
			self.__localexposure = val
		return ov
	def MctfStrength(self,val=None):
		ov = self.__mctfstrength
		if val is not None:
			self.__mctfstrength = val
		return ov
	def DcIrisDuty(self,val=None):
		ov = self.__dcirisduty
		if val is not None:
			self.__dcirisduty = val
		return ov
	def AeTargetRatio(self,val=None):
		ov = self.__aetargetratio
		if val is not None:
			self.__aetargetratio = val
		return ov


class SdkAdvImage(syscp.SysCP):
	def __init__(self):
		syscp.SysCP.__init__(self)
		self.__advimagine = None
		return
	def __del__(self):
		syscp.SysCP.__del__(self)
		self.__advimagine = None
		return

	def FormGetReq(self,sesid=None,seqid=None):
		rbuf = struct.pack('>I',1)
		reqbuf = self.TypeCodeForm(syscp.TYPE_INTVALUE,rbuf)
		return self.FormatSysCp(SYSCODE_GET_ADVANCED_IMAGING_REQ,1,reqbuf,sesid,seqid)

	def ParseGetRsp(self,buf):
		attrbuf = self.UnPackSysCp(buf)
		if self.Code() != SYSCODE_GET_ADVANCED_IMAGING_RSP:
			raise SdkShowCfgInvalidError('code (%d) != (%d)'%(self.Code(),SYSCODE_GET_ADVANCED_IMAGING_RSP))
		if self.AttrCount() != 1:
			raise SdkShowCfgInvalidError('attrcount (%d) != (1)'%(self.AttrCount()))

		self.__advimagine = None
		attrbuf = self.ParseTypeCode(attrbuf)
		if self.TypeCode() != TYPE_ADVANCED_IMAGING:
			raise SdkShowCfgInvalidError('typecode (%d) != (%d)'%(self.TypeCode(),TYPE_ADVANCED_IMAGING))
		img = AdvImagine()
		attrbuf = img.ParseBuf(attrbuf)
		self.__advimagine = img
		return self.__advimagine
		
		
	def FormSetReq(self,advimagine,sesid=None,seqid=None):
		if not isinstance(advimagine,AdvImagine):
			raise SdkShowCfgInvalidError('AdvImagine set not type of AdvImagine')

		rbuf = advimagine.FormatBuf()
		reqbuf = self.TypeCodeForm(TYPE_ADVANCED_IMAGING,rbuf)
		return self.FormatSysCp(SYSCODE_SET_ADVANCED_IMAGING_REQ,1,reqbuf,sesid,seqid)

	def ParseSetRsp(self,buf):
		attrbuf = self.UnPackSysCp(buf)
		if self.Code() != SYSCODE_SET_ADVANCED_IMAGING_RSP:
			raise SdkShowCfgInvalidError('code (%d) != (%d)'%(self.Code(),SYSCODE_SET_ADVANCED_IMAGING_RSP))
		if self.AttrCount() != 1:
			raise SdkShowCfgInvalidError('attrcount (%d) != (1)'%(self.AttrCount()))

		self.MessageCodeParse(attrbuf)
		return
	

