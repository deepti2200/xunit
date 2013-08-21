#! python


'''
	this file is for the sdk server login handle
'''

import struct

import sys
import os
import hashlib
import logging
import pyDes
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..')))
import xunit.utils.exception
import xunit.extlib.xDES as xDES


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
			rbuf += s[:(size-1)]
			rbuf += '\0'
		return rbuf
	def __UnPackStringSize(self,s,size):
		rbuf = ''
		lasti  = -1
		for i in xrange(size):
			if s[i] == '\0':
				lasti = i
				break

		if lasti >= 0:
			rbuf = s[:lasti]
		else:
			rbuf = s[:-2]
		return rbuf
	def PackLoginRequest(self,sesid,username,password,exptime,keeptime):
		self.__buf = ''
		# for login request
		self.__buf += struct.pack('>I',1)
		self.__buf += struct.pack('>H',sesid)
		self.__buf += struct.pack('>H',3)
		self.__buf += self.__PackStringSize(username,64)		
		self.__buf += self.__PackStringSize(password,64)
		self.__buf += struct.pack('>I',exptime)
		keeptime *= 1000000
		self.__buf += struct.pack('>I',keeptime)
		return self.__buf

	def PackLoginSaltRequest(self,seqid,authcode,username,password,salt,exptime,keeptime):
		self.__buf = ''
		# for login request
		self.__buf += struct.pack('>I',1)
		self.__buf += struct.pack('>H',0)
		self.__buf += struct.pack('>H',authcode)
		self.__buf += self.__PackStringSize(username,64)		
		m = self.__GetDes(password,salt)
		#logging.info('passkey %s(%d) password[%s] %s(%d)'%(repr(salt),len(salt),repr(password),repr(m),len(m)))
		if len(m) < 64:
			m += '\0' * (64 - len(m))
		self.__buf += m
		self.__buf += struct.pack('>I',exptime)
		keeptime *= 1000000
		self.__buf += struct.pack('>I',keeptime)
		return self.__buf
		

	def UnPackUnAuthorized(self,buf):
		# now to return the return string
		if len(buf) < 76:
			raise LoginRespHeaderTooShort('%s login header too short'%(repr(buf)))
		respcode = struct.unpack('>I',buf[:4])[0]
		#logging.info('respcode %s'%(respcode))
		if respcode != 2:
			raise LoginRespErrorCode('%s login header error %s'%(repr(buf[:4]),repr(respcode)))

		authcode = struct.unpack('>I',buf[4:8])[0]
		if authcode != 1:
			raise LoginRespAuthNotMd5('%s not unauth %d'%(repr(buf[:8]),authcode))
		
		sesid = struct.unpack('>H',buf[8:10])[0]
		#logging.info('sesid %s'%(sesid))
		if sesid != 0 :
			raise LoginRespErrorCode('%s not sesid 0 (%d)'%(repr(buf[9:10]),sesid))
		
		authcode = struct.unpack('>H',buf[10:12])[0]
		if authcode != 4:
			raise LoginRespAuthNotMd5('%s not authmd5 %d'%(repr(buf[:8]),authcode))

		# we get the 8 bytes
		deskey = buf[16:24]
		#logging.info('md5 %s'%(repr(deskey)))

		return authcode,deskey

	def UnPackSession(self,buf):
		if len(buf) < 80:
			raise LoginRespHeaderTooShort('%s login header too short'%(repr(buf)))

		respcode = struct.unpack('>I',buf[:4])[0]
		if respcode != 2:
			raise LoginRespErrorCode('(%s)response code (%d) != (2)'%(repr(buf[:4]),respcode))

		result = struct.unpack('>I',buf[4:8])[0]
		if result != 0:
			raise LoginRespErrorCode('(%s)response result (%d) != 0'%(repr(buf[:9]),result))

		sesid = struct.unpack('>H',buf[8:10])[0]
		keeptimems = struct.unpack('>I',buf[12:16])[0]
		#logging.info('keeptimems %d'%(keeptimems))
		return sesid

	def __GetDes(self,password,key):
		p = password
		if len(p) < 32:
			p += '\0' * (32 - len(password))
		else:
			p = p[:32]
		
		kd = xDES.DES(key)
		return kd.Encrypt(p)

	def __GetMd5(self,password,salt):
		m = hashlib.md5()
		m.update(password)
		pmd5 = m.hexdigest()
		m2 = hashlib.md5()
		md5pwd = pmd5
		pmd5 += salt
		m2.update(pmd5)
		#logging.info('password %s hash %s salt %s return %s'%(password,md5pwd,salt,m2.hexdigest()))
		return m2.hexdigest()

	def LoginPackSession(self,sesid):
		# nothing to pack for the session id handle
		return ''

