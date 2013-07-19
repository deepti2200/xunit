#! python

'''
	this file is for the sdk server protocol pack
'''

import struct

import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..')))
import xunit.utils.exception

class SdkProtoHeaderTooShort(xunit.utils.exception.XUnitException):
	pass

class SdkProtoHeaderNotGssp(xunit.utils.exception.XUnitException):
	pass



class SdkProtoBufferLengthError(xunit.utils.exception.XUnitException):
	pass


class SdkProtoPack:
	def __InitParam(self):
		self.__buf = ''
		self.__seqid = 0
		self.__sesid = 0
		self.__typeid = 0
		self.__body = ''
		self.__bodylen = 0
		self.__fraglen = 0
		return
	def __init__(self):
		self.__InitParam()
		return

	def Pack(self,sesid,seqnum,typeid,buf):
		self.__InitParam()
		self.__seqid = seqnum
		self.__sesid = sesid
		self.__typeid = typeid
		self.__body = buf
		self.__bodylen = len(buf)
		self.__fraglen = 0
		# magic header
		self.__buf += 'GSSP'
		# for no dataid 
		self.__buf += '\0'
		# for major 1 minor 0
		self.__buf += chr(0x1)
		# this is for sequence number
		self.__buf += struct.pack('>H',seqnum)
		# this is for session id
		self.__buf += struct.pack('>H',sesid)
		# length of the header 20
		self.__buf += chr(20)
		self.__buf += chr(typeid)
		self.__buf += struct.pack('>I',len(buf))
		self.__buf += struct.pack('>I',0)
		self.__buf += buf
		return self.__buf

	def ParseHeader(self,buf):
		if len(buf) < 20:
			raise SdkProtoHeaderTooShort('%s too short'%(repr(buf)))	

		if buf[0] != 'G' or buf[1] != 'S':
			raise SdkProtoHeaderNotGssp('%s not GSSP header'%(repr(buf[:4])))
		if buf[2] != 'S' or buf[3] != 'P':
			raise SdkProtoHeaderNotGssp('%s not GSSP header'%(repr(buf[:4])))


		self.__sesid = struct.unpack('>H',buf[8:10])[0]
		self.__seqid = struct.unpack('>H',buf[6:8])[0]
		logging.info('seqid %s'%(repr(self.__seqid)))
		headerlen  = ord(buf[10])
		fraglen = headerlen - 20
		self.__fraglen = headerlen - 20
		self.__bodylen = struct.unpack('>I',buf[12:16])[0]
		self.__typeid = ord(buf[11])

		bodylen = self.__bodylen
		return  fraglen ,bodylen

	def TypeId(self):
		return self.__typeid

	def SeqId(self):
		return self.__seqid

	def SesId(self):
		return self.__sesid
		

		


		 
