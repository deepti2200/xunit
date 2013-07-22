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


class SdkPtzInvalidError(xunit.utils.exception.XUnitException):
	pass

class SdkPtzOutRangeError(xunit.utils.exception.XUnitException):
	pass



class SdkPtz:
	def __init__(self):
		self.__seqid = -1
		self.__sesid = -1
		self.__res = -1
		return
	def __del__(self):
		self.__seqid = -1
		self.__sesid = -1
		self.__res = -1
		self.__netinfos = []
		return

	def __FormatPtzCommand(self,ptzid,cmd,param1=0,param2=0,param3=0,param4=0):
		rbuf = ''
		rbuf += struct.pack('>II',ptzid,cmd)
		rbuf += struct.pack('>IIII',param1,param2,param3,param4)
		return rbuf

	def __FormatHeader(self,sesid,seqid,cmdid,attrcount,buf):
		rbuf = ''
		rbuf += 'GSMT'
		


	
