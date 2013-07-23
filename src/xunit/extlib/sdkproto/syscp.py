#! python

'''
	this is the file for syscp protocol
'''

import struct

import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..')))
import xunit.utils.exception


SYS_HDR_LENGTH=16
TYPE_INFO_LENGTH=4
TYPE_IPINFOR=10

class SdkSysCpInvalidError(xunit.utils.exception.XUnitException):
	pass



class SysCP:
	def __init__(self,sesid=0):
		self.__code = 0
		self.__sesid = sesid
		self.__seqid = 0
		self.__attrcount = 0
		self.__buf = None
		return

	def __del__(self):
		self.__code = 0
		self.__sesid = 0
		self.__seqid = 0
		self.__attrcount = 0
		self.__buf = None
		return

	def SeqId(self,seqid=None):
		ov = self.__seqid
		if seqid :
			self.__seqid = seqid
		return ov

	def SesId(self,sesid=None):
		ov = self.__sesid
		if sesid :
			self.__sesid = sesid
		return ov

	def FormatSysCp(self,code,buf,sesid=None,seqid=None):
		rbuf = ''
		rbuf += 'GSMT'
		# give the version 1 
		rbuf += chr(1)
		# header length 16
		rbuf += chr(SYS_HDR_LENGTH)
		#code is SYSCODE_GET_IPINFO_REQ
		rbuf += struct.pack('>H',code)
		# attribute is 0
		# seqid sesid and totallength is body length 0
		self.SesId(sesid)
		self.SeqId(seqid)
		codelen = 0
		if buf:
			codelen = len(buf)
		rbuf += struct.pack('>HHHH',0,self.__sesid,self.__seqid,SYS_HDR_LENGTH+codelen)
		rbuf += buf
		return rbuf

	def UnPackSysCp(self,buf):
		if len(buf) < SYS_HDR_LENGTH:
			raise SdkSysCpInvalidError('len (%d) < (%d)'%(len(buf),SYS_HDR_LENGTH))
		if buf[:4] != 'GSMT':
			raise SdkSysCpInvalidError('tag (%s) != (GSMT)'%(repr(buf[:4])))

		if buf[4] != chr(1):
			raise SdkSysCpInvalidError('version (%d) != 1'%(ord(buf[4])))

		if buf[5] != chr(SYS_HDR_LENGTH):
			raise SdkSysCpInvalidError('hdrlen (%d) != (%d)'%(ord(buf[5]),SYS_HDR_LENGTH))
		code = struct.unpack('>H',buf[6:8])[0]
		attrcount =struct.unpack('>H',buf[8:10])[0]

		sesid,seqid = struct.unpack('>HH',buf[10:14])
		tlen = struct.unpack('>H',buf[14:16])[0]
		if tlen > len(buf):
			raise SdkSysCpInvalidError('total length (%d) > (%d)'%(tlen,len(buf)))

		tlen -= SYS_HDR_LENGTH
		self.__code = code
		self.__sesid = sesid
		self.__seqid = seqid
		self.__attrcount = attrcount
		self.__buf = buf[SYS_HDR_LENGTH:]
		return self.__buf

	def AttrCount(self):
		return self.__attrcount

	def PackedBuf(self):
		return self.__buf

	def Code(self):
		return self.__code
	

