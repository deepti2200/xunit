#! python

'''
	this is the file for capabilities get
'''

import struct

import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..')))
import xunit.utils.exception
import xunit.extlib.sdkproto.syscp as syscp

import typexml



SYSCODE_GET_CAPABILITIES_REQ=1197
SYSCODE_GET_CAPABILITIES_RSP=1198


class CapProtoInvalidError(xunit.utils.exception.XUnitException):
	pass



class SdkCapProto(syscp.SysCP):
	def __init__(self):
		syscp.SysCP.__init__(self)
		self.__capproto = None
		return
	def __del__(self):
		syscp.SysCP.__del__(self)
		self.__capproto = None
		return

	def FormatCapProtoGetReq(self,val=0,sesid=None,seqid=None):
		rbuf = struct.pack('>I',val)
		reqbuf = self.TypeCodeForm(syscp.TYPE_INTVALUE,rbuf)
		return self.FormatSysCp(SYSCODE_GET_CAPABILITIES_REQ,1,reqbuf,sesid,seqid)
		

	def ParseCapProtoGetRsp(self,buf):
		attrbuf = self.UnPackSysCp(buf)
		if self.Code() != SYSCODE_GET_CAPABILITIES_RSP:
			raise CapProtoInvalidError('Code (%d) != (%d)'%(self.Code(),SYSCODE_GET_CAPABILITIES_RSP))
		if self.AttrCount() != 1:
			raise CapProtoInvalidError('attrcount (%d) != 1'%(self.AttrCount()))

		attrbuf = self.ParseTypeCode(attrbuf)
		if self.TypeCode() != typexml.TYPE_XML:
			raise CapProtoInvalidError('typecode (%d) != (%d)'%(self.TypeCode(),typexml.TYPE_XML))
		if self.TypeLen() != (len(attrbuf) + 4):
			raise CapProtoInvalidError('typelen(%d) != (%d +4)'%(self.TypeLen() , len(attrbuf)))
		self.__capproto = typexml.XmlPackage()
		self.__capproto.ParseBuf(attrbuf)
		return self.__capproto
		
