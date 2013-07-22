#! python

'''
	this is the file for the ipinfo get and set
'''

import struct

import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..')))
import xunit.utils.exception

SYSCODE_GET_IPINFO_REQ=1013
SYSCODE_GET_IPINFO_RSP=1014

class SdkIpInfoInvalidError(xunit.utils.exception.XUnitException):
	pass


class SdkIpInfo:
	def __init__(self):
		self.__seqid = -1
		self.__sesid = -1
		return

	def __del__(self):
		return

	def FormatQueryInfo(self,seqid,sesid):
		rbuf = ''
		rbuf += 'GSMT'
		# give the version 1 
		rbuf += chr(1)
		# header length 16
		rbuf += chr(16)
		#code is SYSCODE_GET_IPINFO_REQ
		rbuf += struct.pack('>H',SYSCODE_GET_IPINFO_REQ)
		# attribute is 0
		# seqid sesid and totallength is body length 0
		rbuf += struct.pack('>HHHH',0,seqid,sesid,16)
		return rbuf

	def ParseQueryInfo(self,buf):
		if buf[:4] != 'GSMT':
			raise SdkIpInfoInvalidError('tag (%s) != (GSMT)'%(repr(buf[:4])))

		if buf[4] != chr(1):
			raise SdkIpInfoInvalidError('version (%d) != 1'%(ord(buf[4])))

		if buf[5] != chr(16):
			raise SdkIpInfoInvalidError('hdrlen (%d) != 16'%(ord(buf[5])))

		code = struct.unpack('>H',buf[6:8])[0]
		if code != SYSCODE_GET_IPINFO_RSP:
			raise SdkIpInfoInvalidError('code (%d) != (%d)'%(code,SYSCODE_GET_IPINFO_RSP))
		
