#! python

'''
	this is the file for video encode
'''

import struct

import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..')))
import xunit.utils.exception
import syscp

SYSCODE_SET_ENCODECFG_REQ=1031
SYSCODE_SET_ENCODECFG_RSP=1032
SYSCODE_GET_ENCODECFG_REQ=1033
SYSCODE_GET_ENCODECFG_RSP=1034


class SdkVideoCfgInvalidError(xunit.utils.exception.XUnitException):
	pass

class EncodeCfgInvalidError(xunit.utils.exception.XUnitException):
	pass

ENCODE_CFG_LENGTH=52
TYPE_ENCODECFG=12

class EncodeCfg:

	def __InitEncodeCfg(self):
		self.__videoid = 0
		self.__compression = 0
		self.__picwidth = 0
		self.__picheight = 0
		self.__bitratectrl = 0
		self.__quality = 0
		self.__fps = 0
		self.__bitrateaverage = 0
		self.__bitrateup = 0
		self.__bitratedown = 0
		self.__gop = 0
		self.__rotate = 0
		self.__flag = 0
		return

	def VideoId(self,val=None):
		ov = self.__videoid
		if val is not None:
			self.__videoid = val
		return ov

	def Compression(self,val=None):
		ov = self.__compression
		if val is not None:
			self.__compression = val
		return ov
	def PicWidth(self,val=None):
		ov = self.__picwidth
		if val is not None:
			self.__picwidth = val
		return ov
		
	def PicHeight(self,val=None):
		ov = self.__picheight
		if val is not None:
			self.__picheight = val
		return ov

	def BitrateCtrl(self,val=None):
		ov = self.__bitratectrl
		if val is not None:
			self.__bitratectrl = val
		return ov
	def Quality(self,val=None):
		ov = self.__quality
		if val is not None:
			self.__quality = val
		return ov
	def Fps(self,val=None):
		ov = self.__fps
		if val is not None:
			self.__fps = val
		return ov

	def BitrateAverage(self,val=None):
		ov = self.__bitrateaverage
		if val is not None:
			self.__bitrateaverage = val
		return ov

		
	def BitrateUp(self,val=None):
		ov = self.__bitrateup
		if val is not None:
			self.__bitrateup = val
		return ov
	def BitrateDown(self,val=None):
		ov = self.__bitratedown
		if val is not None:
			self.__bitratedown = val
		return ov
	def Gop(self,val=None):
		ov = self.__gop
		if val is not None:
			self.__gop = val
		return ov
	def Rotate(self,val=None):
		ov = self.__rotate
		if val is not None:
			self.__rotate = val
		return ov
	def Flag(self,val=None):
		ov = self.__flag
		if val is not None:
			self.__flag = val
		return ov



	def __ParseEncodeCfg(self,buf):
		if len(buf) < ENCODE_CFG_LENGTH:
			raise EncodeCfgInvalidError('len(%d) < (%d)'%(len(buf),ENCODE_CFG_LENGTH))

		self.__videoid,self.__compression,self.__picwidth,self.__picheight, \
		self.__bitratectrl,self.__quality,self.__fps,self.__bitrateaverage ,\
		self.__bitrateup,self.__bitratedown,self.__gop,self.__roate,\
		self.__flag = struct.unpack('>IIIIIIIIIIIII',buf[:ENCODE_CFG_LENGTH])
		lbuf = buf[ENCODE_CFG_LENGTH:]
		return lbuf

	def __FormatEncodeCfg(self):
		rbuf = ''
		rbuf += struct.pack('>IIIIIIIIIIIII',self.__videoid,self.__compression,self.__picwidth,self.__picheight, \
		self.__bitratectrl,self.__quality,self.__fps,self.__bitrateaverage ,\
		self.__bitrateup,self.__bitratedown,self.__gop,self.__roate,\
		self.__flag)
		return rbuf

	def Format(self):
		return self.__FormatEncodeCfg()

	def __init__(self,buf=''):
		self.__InitEncodeCfg()
		if buf and len(buf) > 0:
			self.__ParseEncodeCfg(buf)
		return
	def __del__(self):
		return

	def ParseVideoEncode(self,buf):
		return self.__ParseEncodeCfg(buf)

class SdkVideoCfg(syscp.SysCP):
	def __init__(self):
		syscp.SysCP.__init__(self)
		self.__videocount = 0
		self.__videocfgs = []
		return

	def __del__(self):
		syscp.SysCP.__del__(self)
		self.__videocount = 0
		self.__videocfgs = []
		return

	def __FormatQuery(self):
		ibuf = ''
		ibuf = struct.pack('>I',1)
		rbuf = self.TypeCodeForm(syscp.TYPE_INTVALUE,ibuf)
		return rbuf
	
	def FormatQuery(self,sesid=None,seqid=None):
		reqbuf = self.__FormatQuery()
		return self.FormatSysCp(SYSCODE_GET_ENCODECFG_REQ,1,reqbuf,sesid,seqid)

	def ParseQuery(self,buf):
		attrbuf = self.UnPackSysCp(buf)
		if self.Code() != SYSCODE_GET_ENCODECFG_RSP:
			raise SdkVideoCfgInvalidError('code (%d) != (%d)'%(self.Code(),SYSCODE_GET_ENCODECFG_RSP))
		if self.AttrCount() < 2:
			raise SdkVideoCfgInvalidError('attrcount (%d) < 2'%(self.AttrCount()))

		# now first to parse
		self.__videocount = 0
		self.__videocfgs = []
		for i in xrange(self.AttrCount()):
			if i == 0:
				attrbuf = self.MessageCodeParse(attrbuf)
			else:
				attrbuf = self.ParseTypeCode(attrbuf,'video encode')
				if self.TypeCode() != TYPE_ENCODECFG:
					raise SdkVideoCfgInvalidError('typecode (%d) != (%d)'%(self.TypeCode(),TYPE_ENCODECFG))
				vcfg = EncodeCfg()
				attrbuf = vcfg.ParseVideoEncode(attrbuf)
				self.__videocount += 1
				self.__videocfgs.append(vcfg)
		return self.__videocount

	def FormatSetVideoCfg(self,vcfg,sesid=None,seqid=None):
		if vcfg is None or not isinstance(vcfg,EncodeCfg):
			raise SdkVideoCfgInvalidError('vcfg not EncodeCfg class')
		reqbuf = vcfg.Format()
		rbuf = self.TypeCodeForm(TYPE_ENCODECFG,reqbuf)
		return self.FormatSysCp(SYSCODE_SET_ENCODECFG_REQ,1,rbuf,sesid,seqid)

	def ParseSetVideoCfg(self,buf):
		rbuf = self.UnPackSysCp()
		if self.Code() != SYSCODE_SET_ENCODECFG_RSP:
			raise SdkVideoCfgInvalidError('code (%d) != (%d)'%(self.Code(),SYSCODE_SET_ENCODECFG_RSP))
		rbuf = self.MessageCodeParse(rbuf)
		return rbuf
		
	def VideoCfgCount(self):
		return self.__videocount

	def VideoCfg(self):
		return self.__videocfgs
