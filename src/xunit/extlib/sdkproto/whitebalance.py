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


TYPE_WHITE_BALANCE=117
WHITE_BALANCE_STRUCT_LENGTH=16

SYSCODE_GET_WHITEBALANCE_REQ=1215
SYSCODE_GET_WHITEBALANCE_RSP=1216
SYSCODE_SET_WHITEBALANCE_REQ=1217
SYSCODE_SET_WHITEBALANCE_RSP=1218

class WhiteBalanceInvalidError(xunit.utils.exception.XUnitException):
	pass



class WhiteBalance:
	def __ResetVar(self):
		self.__mode = 0
		self.__rgrain = 512
		self.__bgrain = 512
		self.__reserv1 = 0
		return

	def __init__(self):
		self.__ResetVar()
		return 

	def __del__(self):
		self.__ResetVar()
		return

	def ParseBuf(self,buf):
		if len(buf) < WHITE_BALANCE_STRUCT_LENGTH:
			raise WhiteBalanceInvalidError('len(%d) < WHITE_BALANCE_STRUCT_LENGTH(%d)'%(len(buf),WHITE_BALANCE_STRUCT_LENGTH))

		self.__mode , self.__rgrain,self.__bgrain ,self.__reserv1 = struct.unpack('>IIII',buf[:WHITE_BALANCE_STRUCT_LENGTH])
		return buf[WHITE_BALANCE_STRUCT_LENGTH:]

	def FormatBuf(self):
		rbuf = ''
		rbuf += struct.pack('>IIII',self.__mode,self.__rgrain,self.__bgrain,self.__reserv1)
		return rbuf

	def Mode(self,val=None):
		ov = self.__mode
		if val is not None:
			self.__mode = val
		return ov

	def RGrain(self,val=None):
		ov = self.__rgrain
		if val is not None:
			self.__rgrain = val
		return ov
	def BGrain(self,val=None):
		ov = self.__bgrain
		if val is not None:
			self.__bgrain = val
		return ov	
	def Reserv1(self,val=None):
		ov = self.__reserv1
		if val is not None:
			self.__reserv1 = val
		return ov

	def __Format(self):
		rbuf = ''
		rbuf += 'mode        :(%d)\n'%(self.__mode)
		rbuf += 'rgrain      :(%d)\n'%(self.__rgrain)
		rbuf += 'bgrain      :(%d)\n'%(self.__bgrain)
		rbuf += 'reserv1     :(%d)\n'%(self.__reserv1)
		return rbuf

	def __str__(self):
		return self.__Format()

	def __repr__(self):
		return self.__Format()


class SdkWhiteBalance(syscp.SysCP):
	def __init__(self):
		syscp.SysCP.__init__(self)
		self.__whitebalance = None
		return

	def __del__(self):
		syscp.SysCP.__del__(self)
		self.__whitebalance = None
		return

	def FormatQuery(self,sesid=None,seqid=None):
		reqbuf = ''
		return self.FormatSysCp(SYSCODE_GET_WHITEBALANCE_REQ,0,reqbuf,sesid,seqid)

	def ParseQuery(self,buf):
		attrbuf = self.UnPackSysCp(buf)
		if self.Code() != SYSCODE_GET_WHITEBALANCE_RSP:
			raise WhiteBalanceInvalidError('code (%d) != SYSCODE_GET_WHITEBALANCE_RSP(%d)'%(self.Code(),SYSCODE_GET_WHITEBALANCE_RSP))

		if self.AttrCount() != 1:
			raise WhiteBalanceInvalidError('count (%d) != 1'%(self.AttrCount()))
		self.__whitebalance = None
		wb = WhiteBalance()
		attrbuf = self.ParseTypeCode(attrbuf,'white balance')
		if self.TypeCode() != TYPE_WHITE_BALANCE:
			raise WhiteBalanceInvalidError('typecode(%d) != TYPE_WHITE_BALANCE(%d)'%(self.TypeCode(),TYPE_WHITE_BALANCE))
		wb.ParseBuf(attrbuf)
		self.__whitebalance = wb
		return wb

	def FormatSet(self,wb,sesid=None,seqid=None):
		if not isinstance(wb,WhiteBalance):
			raise WhiteBalanceInvalidError('param not whitebalance ')

		reqbuf = wb.FormatBuf()
		rbuf = self.TypeCodeForm(TYPE_WHITE_BALANCE,reqbuf)
		return self.FormatSysCp(SYSCODE_SET_WHITEBALANCE_REQ,1,rbuf,sesid,seqid)

	def ParseSet(self,buf):
		rbuf = self.UnPackSysCp(buf)
		if self.Code() != SYSCODE_SET_WHITEBALANCE_RSP:
			raise SdkVideoCfgInvalidError('code (%d) != (%d)'%(self.Code(),SYSCODE_SET_WHITEBALANCE_RSP))
		rbuf = self.MessageCodeParse(rbuf)
		return rbuf

	

