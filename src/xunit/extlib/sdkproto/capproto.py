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


TYPE_CAPABILITIES=113
SYSCODE_GET_CAPABILITIES_REQ=1197
SYSCODE_GET_CAPABILITIES_RSP=1198


class CapProtoInvalidError(xunit.utils.exception.XUnitException):
	pass


class CapProto:
	def __init__(self):
		self.__enc = 0
		self.__len = 0
		self.__cap = ''
		return

	def __del__(self):
		self.__enc = 0
		self.__len = 0
		self.__cap = ''
		return

	def __Format(self):
		rbuf = ''
		rbuf += 'enc             : %d\n'%(self.__enc)
		rbuf += 'len             : %d\n'%(self.__len)
		rbuf += 'capabilities    : (%s)\n'%(self.__cap)
		return rbuf

	def __str__(self):
		return self.__Format()

	def __repr__(self):
		return self.__Format()

	def ParseBuf(self,buf):
		if len(buf) < 4:
			raise CapProtoInvalidError('len(%d) < 4'%(len(buf)))
		self.__enc , self.__len = struct.unpack('>HH',buf[:4])
		if len(buf) < (4 + self.__len):
			raise CapProtoInvalidError('len(%d) < (4 + %d)'%(len(buf),self.__len))

		self.__cap = buf[4:(4+self.__len)]
		return buf[(4+self.__len):]

	def FormatBuf(self):
		rbuf = ''
		rbuf += struct.pack('>HH',self.__enc,self.__len)
		rbuf += self.__cap
		return rbuf

	def Enc(self,val=None):
		ov = self.__enc
		if val is not None:
			self.__enc = val
		return ov

	def Cap(self,val=None):
		ov = self.__cap
		if val is not None:
			self.__len = len(val)+1
			self.__cap = val
			self.__cap += chr(0x0)
		return ov



class SdkCapProto(syscp.SysCP):
	def __init__(self):
		syscp.SysCP.__init__(self)
		self.__capproto = None
		return
	def __del__(self):
		syscp.SysCP.__del__(self)
		self.__capproto = None
		return

	def FormatCapProtoGetReq(self,sesid=None,seqid=None):
		return self.FormatSysCp(SYSCODE_GET_CAPABILITIES_REQ,0,'',sesid,seqid)
		

	def ParseCapProtoGetRsp(self,buf):
		attrbuf = self.UnPackSysCp(buf)
		if self.Code() != SYSCODE_GET_CAPABILITIES_RSP:
			raise CapProtoInvalidError('Code (%d) != (%d)'%(self.Code(),SYSCODE_GET_CAPABILITIES_RSP))
		if self.AttrCount() != 1:
			raise CapProtoInvalidError('attrcount (%d) != 1'%(self.AttrCount()))

		attrbuf = self.ParseTypeCode(attrbuf)
		if self.TypeCode() != TYPE_CAPABILITIES:
			raise CapProtoInvalidError('typecode (%d) != (%d)'%(self.TypeCode(),TYPE_CAPABILITIES))
		if self.TypeLen() != (len(attrbuf) + 4):
			raise CapProtoInvalidError('typelen(%d) != (%d +4)'%(self.TypeLen() , len(attrbuf)))
		self.__capproto = None
		self.__capproto.ParseBuf(attrbuf)
		return self.__capproto
		
