#! python

'''
	this file is for the sdk server protocol pack
'''

import struct

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..')))
import xunit.utils.exception

class SdkProtoHeaderTooShort(xunit.utils.exception.XUnitException):
	pass

class SdkProtoHeaderNotGssp(xunit.utils.exception.XUnitException):
	pass



class SdkProtoBufferLengthError(xunit.utils.exception.XUnitException):
	pass


class SdkProtoPack:
	def __init__(self):
		self.__buf = ''
		return

	def Pack(self,sesid,seqnum,typeid,buf):
		self.__buf = ''
		# magic header
		self.__buf += 'GSSP'
		# for no dataid 
		self.__buf += '\0'
		# for major 1 minor 0
		self.__buf += '\x1'
		# this is for sequence number
		self.__buf += struct.pack('>H',seqnum)
		# this is for session id
		self.__buf += struct.pack('>H',sesid)
		# length of the header 20
		self.__buf += chr(20)
		self.__buf += chr(typeid)
		self.__buf += str uct.pack('>I',len(buf))
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

		flag = ord(buf[4])
		frag = 0
		fraglen = 0
		if flag and 1:
			frag = 1
			fraglen = 12

		bodylen = struct.unpack('>I',buf[12:16])
		return frag , fraglen ,bodylen
	

		


		 
