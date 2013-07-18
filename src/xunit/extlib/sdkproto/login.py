#! python


'''
	this file is for the sdk server login handle
'''

import struct

import sys
import os
import hashlib
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..')))
import xunit.utils.exception

class LoginRespHeaderTooShort(xunit.utils.exception.XUnitException):
	pass

class LoginRespErrorCode(xunit.utils.exception.XUnitException):
	pass


class LoginRespAuthNotMd5(xunit.utils.exception.XUnitException):
	pass


class LoginPack:
	def __init__(self):
		self.__buf = ''
		return

	def __PackStringSize(self,s,size):
		rbuf = ''
		if len(s) < size:
			rbuf += s
			lsize = size - len(s)
			rbuf += '\0' * lsize
		else:
			rbuf += s[size-1]
			rbuf += '\0'
		return rbuf
	def __UnPackStringSize(self,s,size):
		rbuf = ''
		lasti  = -1
		for i in xrange(size):
			if s[i] == '\0':
				lasti = i-1
				break

		if lasti >= 0:
			rbuf = s[:lasti]
		else:
			rbuf = s[:(size-1)]
		return rbuf
	def PackLoginRequest(self,sesid,username,password,exptime,keeptime):
		self.__buf = ''
		# for login request
		self.__buf += struct.pack('>I',1)
		self.__buf += struct.pack('>H',sesid)
		self.__buf += struct.pack('>H',2)
		self.__buf += self.__PackStringSize(username,64)		
		self.__buf += self.__PackStringSize(password,64)
		self.__buf += struct.pack('>I',exptime)
		keeptime *= 1000000
		self.__buf += struct.pack('>I',keeptime)
		return self.__buf

	def PackLoginSaltRequest(self,sesid,encrypt,username,password,salt,exptime,keeptime):
		self.__buf = ''
		# for login request
		self.__buf += struct.pack('>I',1)
		self.__buf += struct.pack('>H',sesid)
		self.__buf += struct.pack('>H',encrypt)
		self.__buf += self.__PackStringSize(username,64)
		m = self.__GetMd5(password,salt)
		self.__buf += self.__PackStringSize(m,64)
		self.__buf += struct.pack('>I',exptime)
		keeptime *= 1000000
		self.__buf += struct.pack('>I',keeptime)
		return self.__buf
		

	def UnPackUnAuthorized(self,buf):
		# now to return the return string
		if len(buf) < 76:
			raise LoginRespHeaderTooShort('%s login header too short'%(repr(buf)))
		respcode = struct.unpack('>I',buf[:4])
		if respcode != 2:
			raise LoginRespErrorCode('%s login header error %d'%(repr(buf[:4]),respcode))

		authcode = struct.unpack('>I',buf[4:8])
		if authcode != 1:
			raise LoginRespAuthNotMd5('%s not unauth %d'%(repr(buf[:8]),authcode))
		
		sesid = struct.unpack('>H',buf[9:10])
		if sesid != 0 :
			raise LoginRespErrorCode('%s not sesid 0 (%d)'%(repr(buf[9:10]),sesid))
		
		authcode = struct.unpack('>H',buf[11:12])
		if authcode != 2:
			raise LoginRespAuthNotMd5('%s not authmd5 %d'%(repr(buf[:8]),authcode))

		md5salt = self.__UnPackStringSize(buf[12:],64)

		return authcode,md5salt

	def UnPackSession(self,buf):
		if len(buf) < 76:
			raise LoginRespHeaderTooShort('%s login header too short'%(repr(buf)))

		respcode = struct.unpack('>I',buf[:4])
		if respcode != 2:
			raise LoginRespErrorCode('(%s)response code (%d) != (2)'%(repr(buf[:4]),respcode))

		result = struct.unpack('>I',buf[4:8])
		if result != 0:
			raise LoginRespErrorCode('(%s)response result (%d) != 0'%(repr(buf[:9]),result))

		sesid = struct.unpack('>H',buf[8:10])
		return sesid
		

	def __GetMd5(self,password,salt):
		m = hashlib.md5()
		pmd5 =  m.update(password).hexdigest()
		m2 = hashlib.md5()
		pmd5 += salt
		m2.update(pmd5)
		return m2.hexdigest()

	

