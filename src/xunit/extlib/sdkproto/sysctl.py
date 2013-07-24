#! python

'''
	this is the file for the sysctl
'''

import struct

import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..')))
import xunit.utils.exception
import syscp


SYSCODE_CTL_SYSTEM_REQ=1091
SYSCODE_CTL_SYSTEM_RSP=1092

class SdkSysCtlInvalidError(xunit.utils.exception.XUnitException):
	pass


class SdkSysCtl(syscp.SysCP):
	def __init__(self):
		syscp.SysCP.__init__(self)
		return

	def __del__(self):
		syscp.SysCP.__del__(self)
		return

	def __FormatSysCtl(self,code):
		rbuf = ''
		rbuf += struct.pack('>HHI',syscp.TYPE_INTVALUE,(syscp.TYPE_INTVALUE_LENGTH + syscp.TYPE_INFO_LENGTH),code)
		return rbuf

	def RebootReq(self,sesid=None,seqid=None):
		reqbuf = self.__FormatSysCtl(1)
		return self.FormatSysCp(SYSCODE_CTL_SYSTEM_REQ,1,reqbuf,sesid,seqid)

	def RebootResp(self,rbuf):
		reqbuf = self.UnPackSysCp(rbuf)
		if self.Code() != SYSCODE_CTL_SYSTEM_RSP:
			raise SdkSysCtlInvalidError('code (%d) != (%d)'%(self.Code(),SYSCODE_CTL_SYSTEM_RSP))
		if self.AttrCount() != 1:
			raise SdkSysCtlInvalidError('code (%d) != (1)'%(self.AttrCount()))

		resbuf = self.MessageCodeParse(reqbuf,'reboot response')
		return 