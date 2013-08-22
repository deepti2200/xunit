#! python

'''
	this is the file for workstate get
'''

import struct

import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..')))
import xunit.utils.exception
import xunit.extlib.sdkproto.syscp as syscp
import typexml

SYSCODE_GET_DEVICE_WORK_STATE_REQ=1191
SYSCODE_GET_DEVICE_WORK_STATE_RSP=1192

STREAM_CONNECT_MAX_NUM=16
MAX_STREAM_IDS=4
MAX_ALARM_OUT=16
MAX_ALARM_IN=16

class WorkStateInvalidError(xunit.utils.exception.XUnitException):
	pass






class SdkWorkState(syscp.SysCP):
	def __init__(self):
		syscp.SysCP.__init__(self)
		self.__workstate = None
		return
	def __del__(self):
		syscp.SysCP.__del__(self)
		self.__workstate = None
		return

	def FormGetWorkStateReq(self,sesid=None,seqid=None):
		return self.FormatSysCp(SYSCODE_GET_DEVICE_WORK_STATE_REQ,0,'',sesid,seqid)

	def ParseGetWorkStateRsp(self,buf):
		attrbuf = self.UnPackSysCp(buf)
		if self.Code() != SYSCODE_GET_DEVICE_WORK_STATE_RSP:
			raise WorkStateInvalidError('Code (%d) != (%d)'%(self.Code(),SYSCODE_GET_DEVICE_WORK_STATE_RSP))
		if self.AttrCount() != 1:
			raise WorkStateInvalidError('attrcount (%d) != 1'%(self.AttrCount()))

		attrbuf = self.ParseTypeCode(attrbuf)
		if self.TypeCode() != typexml.TYPE_XML:
			raise WorkStateInvalidError('typecode (%d) != (%d)'%(self.TypeCode(),typexml.TYPE_XML))
		self.__workstate = typexml.XmlPackage()
		self.__workstate.ParseBuf(attrbuf)
		return self.__workstate
		
	
