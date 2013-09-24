#! python

'''
	this is the file for encode parameter 
'''

import struct

import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..')))
import xunit.utils.exception
import xunit.extlib.sdkproto.syscp as syscp


SYSCODE_GET_ENCSTREAM_COMBINE_REQ=1201
SYSCODE_GET_ENCSTREAM_COMBINE_RSP=1202
SYSCODE_SET_ENCSTREAM_COMBINE_REQ=1203
SYSCODE_SET_ENCSTREAM_COMBINE_RSP=1204

ENCSTREAM_COMBINE_STRUCT_LENGTH=16
TYPE_ENCSTREAM_COMBINE=114

class EncParamInvalidError(xunit.utils.exception.XUnitException):
	pass


class EncParam:
	def __Reset(self):
		self.__videoid = 1
		self.__enablestreamnum = 1
		self.__streamcombineno = 0
		self.__reserv1 = 0
		return
		
	def __init__(self):
		self.__Reset()
		return

	def __del__(self):
		self.__Reset()
		return

	def __Format(self):
		rbuf = ''
		rbuf += 'videoid           :%d\n'%(self.__videoid)
		rbuf += 'enablestreamnum   :%d\n'%(self.__enablestreamnum)
		rbuf += 'streamcombineno   :%d\n'%(self.__streamcombineno)
		rbuf += 'reserv1           :%d\n'%(self.__reserv1)
		return rbuf

	def __str__(self):
		return self.__Format()

	def __repr__(self):
		return self.__Format()

	def ParseBuf(self,buf):
		if len(buf) < ENCSTREAM_COMBINE_STRUCT_LENGTH:
			raise EncParamInvalidError('len(%d) < %d'%(len(buf),ENCSTREAM_COMBINE_STRUCT_LENGTH))

		self.__videoid ,self.__enablestreamnum,self.__streamcombineno,self.__reserv1 = struct.unpack('>IIII',buf[:ENCSTREAM_COMBINE_STRUCT_LENGTH])
		return buf[ENCSTREAM_COMBINE_STRUCT_LENGTH:]

	def FormatBuf(self):
		rbuf = ''
		rbuf += struct.pack('>IIII',self.__videoid ,self.__enablestreamnum,self.__streamcombineno,self.__reserv1)
		return rbuf

	def VideoId(self,val=None):
		ov = self.__videoid
		if val is not None:
			self.__videoid = val
		return ov

	def EnableStreamNum(self,val=None):
		ov = self.__enablestreamnum
		if val is not None:
			self.__enablestreamnum = val
		return ov

	def StreamCombineNo(self,val=None):
		ov = self.__streamcombineno
		if val is not None:
			self.__streamcombineno = val
		return ov

	def Reserv1(self,val=None):
		ov = self.__reserv1
		if val is not None:
			self.__reserv1 = val
		return ov


class SdkEncParam(syscp.SysCP):
	def __init__(self):
		syscp.SysCP.__init__(self)
		self.__encparam = None
		return

	def __del__(self):
		syscp.SysCP.__del__(self)
		self.__encparam = None
		return

	def FormatEncParamGetReq(self,sesid=None,seqid=None):
		return self.FormatSysCp(SYSCODE_GET_ENCSTREAM_COMBINE_REQ,0,'',sesid,seqid)
		

	def ParseEncParamGetRsp(self,buf):
		attrbuf = self.UnPackSysCp(buf)
		if self.Code() != SYSCODE_GET_ENCSTREAM_COMBINE_RSP:
			raise EncParamInvalidError('Code (%d) != (%d)'%(self.Code(),SYSCODE_GET_ENCSTREAM_COMBINE_RSP))
		if self.AttrCount() != 1:
			raise EncParamInvalidError('attrcount (%d) != 1'%(self.AttrCount()))

		attrbuf = self.ParseTypeCode(attrbuf)
		if self.TypeCode() != TYPE_ENCSTREAM_COMBINE:
			raise EncParamInvalidError('typecode (%d) != (%d)'%(self.TypeCode(),TYPE_ENCSTREAM_COMBINE))
		if self.TypeLen() != (len(attrbuf) + 4):
			raise EncParamInvalidError('typelen(%d) != (%d +4)'%(self.TypeLen() , len(attrbuf)))
		self.__encparam = EncParam()
		self.__encparam.ParseBuf(attrbuf)
		return self.__encparam

	def FormatEncParamSetReq(self,encparam,sesid=None,seqid=None):
		if not isinstance(encparam,EncParam):
			raise EncParamInvalidError('encparam not EncParam class')
		rbuf = encparam.FormatBuf()
		reqbuf = self.TypeCodeForm(TYPE_ENCSTREAM_COMBINE,rbuf)
		return self.FormatSysCp(SYSCODE_SET_ENCSTREAM_COMBINE_REQ,1,reqbuf,sesid,seqid)
		
	def ParseEncParamSetRsp(self,buf):
		attrbuf = self.UnPackSysCp(buf)
		if self.Code() != SYSCODE_SET_ENCSTREAM_COMBINE_RSP:
			raise EncParamInvalidError('code (%d) != (%d)'%(self.Code(),SYSCODE_SET_ENCSTREAM_COMBINE_RSP))
		if self.AttrCount() != 1:
			raise EncParamInvalidError('attrcount (%d) != (1)'%(self.AttrCount()))

		self.MessageCodeParse(attrbuf)
		return
		
