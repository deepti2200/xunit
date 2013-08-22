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

TYPE_XML=113

class TypeXmlInvalidError(xunit.utils.exception.XUnitException):
	pass


class XmlPackage:
	def __init__(self):
		self.__enc = 0
		self.__len = 0
		self.__xml = ''
		return

	def __del__(self):
		self.__enc = 0
		self.__len = 0
		self.__xml = ''
		return

	def __Format(self):
		rbuf = ''
		rbuf += 'enc             : %d\n'%(self.__enc)
		rbuf += 'len             : %d\n'%(self.__len)
		rbuf += 'xml             : (%s)(%d)\n'%(self.__xml,len(self.__xml))
		return rbuf

	def __str__(self):
		return self.__Format()

	def __repr__(self):
		return self.__Format()

	def ParseBuf(self,buf):
		if len(buf) < 8:
			raise TypeXmlInvalidError('len(%d) < 4'%(len(buf)))
		self.__enc , self.__len = struct.unpack('>II',buf[:8])
		if len(buf) < (8 + self.__len):
			raise TypeXmlInvalidError('len(%d) < (8 + %d)'%(len(buf),self.__len))

		self.__xml = buf[8:(8+self.__len)]
		return buf[(8+self.__len):]

	def FormatBuf(self):
		rbuf = ''
		rbuf += struct.pack('>II',self.__enc,self.__len)
		rbuf += self.__xml
		return rbuf

	def Enc(self,val=None):
		ov = self.__enc
		if val is not None:
			self.__enc = val
		return ov

	def Xml(self,val=None):
		ov = self.__xml
		if val is not None:
			self.__len = len(val)+1
			self.__xml = val
			self.__xml += chr(0x0)
		return ov
	



