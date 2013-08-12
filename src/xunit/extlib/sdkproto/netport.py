#! python

'''
	this is the file for network get and set
'''

import struct

import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..')))
import xunit.utils.exception
import xunit.extlib.sdkproto.syscp as syscp


TYPE_NETWORK_PORT=112
TYPE_NETWORK_PORT_STRUCT_LENGTH=40
TYPE_NETWORK_PORT_LENGTH=(TYPE_NETWORK_PORT_STRUCT_LENGTH+4)
SYSCODE_GET_NETWORK_PORT_REQ=1193
SYSCODE_GET_NETWORK_PORT_RSP=1194
SYSCODE_SET_NETWORK_PORT_REQ=1195
SYSCODE_SET_NETWORK_PORT_RSP=1196

class NetworkPortInvalidError(xunit.utils.exception.XUnitException):
	pass


class NetworkPort:
	def __init__(self):
		self.__httpport = 80
		self.__rtspport = 554
		self.__sdkport = 30000
		return

	def __del__(self):
		self.__httpport = 80
		self.__rtspport = 554
		self.__sdkport = 30000
		return

	def __Format(self):
		rbuf = ''
		rbuf += 'http port         : (%d)\n'%(self.__httpport)
		rbuf += 'rtsp port         : (%d)\n'%(self.__rtspport)
		rbuf += 'sdk  port         : (%d)\n'%(self.__sdkport)
		return rbuf

	def __repr__(self):
		return self.__Format()

	def __str__(self):
		return self.__Format()

	def ParseBuf(self,buf):
		if len(buf) < TYPE_NETWORK_PORT_STRUCT_LENGTH:
			raise NetworkPortInvalidError('len(%d) < (%d)'%(len(buf),TYPE_NETWORK_PORT_STRUCT_LENGTH))

		self.__httpport,self.__rtspport,self.__sdkport = struct.unpack('>III',buf[:12])

		return buf[TYPE_NETWORK_PORT_STRUCT_LENGTH:]

	def FormatBuf(self):
		rbuf = ''
		rbuf += struct.pack('>IIIIIIIIII',self.__httpport,self.__rtspport,self.__sdkport ,0,0,0,0,0,0,0)
		return rbuf

	def HttpPort(self,val=None):
		ov = self.__httpport
		if val is not None:
			self.__httpport = val
		return ov

	def RtspPort(self,val=None):
		ov = self.__rtspport
		if val is not None:
			self.__rtspport = val
		return ov
	def SdkPort(self,val=None):
		ov = self.__sdkport
		if val is not None:
			self.__sdkport = val
		return ov

class SdkNetworkPort(syscp.SysCP):
	def __init__(self):
		syscp.SysCP.__init__(self)
		self.__netport = None
		return
	def __del__(self):
		syscp.SysCP.__del__(self)
		self.__netport = None
		return

	def FormatGetNetworkportReq(self,sesid=None,seqid=None):
		return self.FormatSysCp(SYSCODE_GET_NETWORK_PORT_REQ,0,'',sesid,seqid)

	def ParseGetNetworkPortRsp(self,buf):
		attrbuf = self.UnPackSysCp(buf)
		if self.Code() != SYSCODE_GET_NETWORK_PORT_RSP:
			raise NetworkPortInvalidError('Code (%d) != (%d)'%(self.Code(),SYSCODE_GET_NETWORK_PORT_RSP))
		if self.AttrCount() != 1:
			raise NetworkPortInvalidError('attrcount (%d) != 1'%(self.AttrCount()))

		attrbuf = self.ParseTypeCode(attrbuf)
		if self.TypeCode() != TYPE_NETWORK_PORT:
			raise NetworkPortInvalidError('typecode (%d) != (%d)'%(self.TypeCode(),TYPE_NETWORK_PORT))
		self.__netport = NetworkPort()
		self.__netport.ParseBuf(attrbuf)
		return self.__netport

	def FormatSetNetworkPortReq(self,netport,sesid=None,seqid=None):
		if not isinstance(netport,NetworkPort):
			raise NetworkPortInvalidError('netport param not NetworkPort class instance')

		reqbuf = netport.FormatBuf()
		return self.FormatSysCp(SYSCODE_SET_NETWORK_PORT_REQ,1,reqbuf,sesid,seqid)

	def ParseSetNetworkPortRsp(self,buf):
		attrbuf = self.UnPackSysCp(buf)
		if self.Code() != SYSCODE_SET_NETWORK_PORT_RSP:
			raise NetworkPortInvalidError('Code (%d) != (%d)'%(self.Code(),SYSCODE_SET_NETWORK_PORT_RSP))
		if self.AttrCount() != 1:
			raise NetworkPortInvalidError('attrcount (%d) != 1'%(self.AttrCount()))

		self.MessageCodeParse(attrbuf,'SetNetworkPortRsp')
		return

