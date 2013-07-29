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

SYSCODE_GET_IMAGING_REQ=1171
SYSCODE_GET_IMAGING_RSP=1172
SYSCODE_SET_IMAGING_REQ=1173
SYSCODE_SET_IMAGING_RSP=1174

TYPE_IMAGING=40
TYPE_IMAGING_STRUCT_LENGTH=40
TYPE_IMAGING_LENGTH=(TYPE_IMAGING_STRUCT_LENGTH+4)

class ImagineInvalidError(xunit.utils.exception.XUnitException):
	pass


class Imagine:
	def __init__(self):
		self.__videoid = 1
		self.__brightness = 0
		self.__contrast = 0
		self.__saturation = 0
		self.__hue = 0
		self.__sharpness = 0
		self.__exposuremode = 0
		self.__exposurevaluemin = 0
		self.__exposurevaluemax = 0
		self.__gainmax = 0
		return

	def __del__(self):
		self.__videoid = 1
		self.__brightness = 0
		self.__contrast = 0
		self.__saturation = 0
		self.__hue = 0
		self.__sharpness = 0
		self.__exposuremode = 0
		self.__exposurevaluemin = 0
		self.__exposurevaluemax = 0
		self.__gainmax = 0
		return

	def __Format(self):
		rbuf = ''
		rbuf += 'videoid         : %d\n'%(self.__videoid)
		rbuf += 'brightness      : %d\n'%(self.__brightness)
		rbuf += 'contrast        : %d\n'%(self.__contrast)
		rbuf += 'saturation      : %d\n'%(self.__saturation)
		rbuf += 'hue             : %d\n'%(self.__hue)
		rbuf += 'sharpness       : %d\n'%(self.__sharpness)
		rbuf += 'exposuremode    : %d\n'%(self.__exposuremode)
		rbuf += 'exposurevaluemin: %d\n'%(self.__exposurevaluemin)
		rbuf += 'exposurevaluemax: %d\n'%(self.__exposurevaluemax)
		rbuf += 'gainmax         : %d\n'%(self.__gainmax)
		return rbuf

	def __str__(self):
		return self.__Format()

	def __repr__(self):
		return self.__Format()


	def ParseBuf(self,buf):
		if len(buf) < TYPE_IMAGING_STRUCT_LENGTH:
			raise ImagineInvalidError('len(%d) < (%d)'%(len(buf),TYPE_IMAGING_STRUCT_LENGTH))

		self.__videoid , self.__brightness,self.__contrast , self.__saturation ,\
		self.__hue , self.__sharpness , self.__exposuremode , self.__exposurevaluemin ,\
		self.__exposurevaluemax , self.__gainmax = struct.unpack('>IIIIIIIIII',buf[:TYPE_IMAGING_STRUCT_LENGTH])
		return buf[TYPE_IMAGING_STRUCT_LENGTH:]

	def FormatBuf(self):
		rbuf = ''
		rbuf += struct.pack('>IIIIIIIIII',self.__videoid , self.__brightness,self.__contrast , self.__saturation ,\
			self.__hue , self.__sharpness , self.__exposuremode , self.__exposurevaluemin ,\
			self.__exposurevaluemax , self.__gainmax)
		return rbuf

	def VideoId(self,val=None):
		ov = self.__videoid
		if val is not None:
			self.__videoid = val
		return ov

	def Brightness(self,val=None):
		ov = self.__brightness
		if val is not None:
			self.__brightness = val
		return ov

	def Contrast(self,val=None):
		ov = self.__contrast
		if val is not None:
			self.__contrast = val
		return ov
		
	def Saturation(self,val=None):
		ov = self.__saturation
		if val is not None:
			self.__saturation = val
		return ov
	def Hue(self,val=None):
		ov = self.__hue
		if val is not None:
			self.__hue = val
		return ov
	def Sharpness(self,val=None):
		ov = self.__sharpness
		if val is not None:
			self.__sharpness = val
		return ov
	def ExposureMode(self,val=None):
		ov = self.__exposuremode
		if val is not None:
			self.__exposuremode = val
		return ov
	def ExposureValueMin(self,val=None):
		ov = self.__exposurevaluemin
		if val is not None:
			self.__exposurevaluemin = val
		return ov

	def ExposureValueMax(self,val=None):
		ov = self.__exposurevaluemax
		if val is not None:
			self.__exposurevaluemax = val
		return ov

	def GainMax(self,val=None):
		ov = self.__gainmax
		if val is not None:
			self.__gainmax = val
		return ov


class SdkImagineInvalidError(xunit.utils.exception.XUnitException):
	pass


class SdkImagine(syscp.SysCP):
	def __init__(self):
		syscp.SysCP.__init__(self)
		self.__imagine = None
		return
	def __del__(self):
		syscp.SysCP.__del__(self)
		self.__imagine = None
		return

	def FormGetReq(self,sesid=None,seqid=None):
		rbuf = struct.pack('>I',1)
		reqbuf = self.TypeCodeForm(syscp.TYPE_INTVALUE,rbuf)
		return self.FormatSysCp(SYSCODE_GET_IMAGING_REQ,1,reqbuf,sesid,seqid)

	def ParseGetRsp(self,buf):
		attrbuf = self.UnPackSysCp(buf)
		if self.Code() != SYSCODE_GET_IMAGING_RSP:
			raise SdkShowCfgInvalidError('code (%d) != (%d)'%(self.Code(),SYSCODE_GET_IMAGING_RSP))
		if self.AttrCount() != 1:
			raise SdkShowCfgInvalidError('attrcount (%d) != (1)'%(self.AttrCount()))

		self.__imagine = None
		attrbuf = self.ParseTypeCode(attrbuf)
		if self.TypeCode() != TYPE_IMAGING:
			raise SdkShowCfgInvalidError('typecode (%d) != (%d)'%(self.TypeCode(),TYPE_IMAGING))
		img = Imagine()
		attrbuf = img.ParseBuf(attrbuf)
		self.__imagine = img
		return self.__imagine
		
		
	def FormSetReq(self,imagine,sesid=None,seqid=None):
		if not isinstance(imagine,Imagine):
			raise SdkShowCfgInvalidError('showcfg param not type of Imagine')

		rbuf = imagine.FormatBuf()
		reqbuf = self.TypeCodeForm(TYPE_IMAGING,rbuf)
		return self.FormatSysCp(SYSCODE_SET_IMAGING_REQ,1,reqbuf,sesid,seqid)

	def ParseSetRsp(self,buf):
		attrbuf = self.UnPackSysCp(buf)
		if self.Code() != SYSCODE_SET_IMAGING_RSP:
			raise SdkShowCfgInvalidError('code (%d) != (%d)'%(self.Code(),SYSCODE_SET_IMAGING_RSP))
		if self.AttrCount() != 1:
			raise SdkShowCfgInvalidError('attrcount (%d) != (1)'%(self.AttrCount()))

		self.MessageCodeParse(attrbuf)
		return

	
	
