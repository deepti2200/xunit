#! python

'''
	this is the file for get and set userinfo
'''

import struct

import sys
import os
import logging
import pyDes
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..')))
import xunit.utils.exception
import xunit.extlib.sdkproto.syscp as syscp

TYPE_USERINFOR=11
TYPE_USERINFOR_STRUCT_LENGTH=260
TYPE_USERINFOR_LENGTH=(TYPE_USERINFOR_STRUCT_LENGTH+4)

SYSCODE_SET_USERINFO_REQ=1021
SYSCODE_SET_USERINFO_RSP=1022
SYSCODE_GET_USERINFO_REQ=1023
SYSCODE_GET_USERINFO_RSP=1024
SYSCODE_DEL_USERINFO_REQ=1025
SYSCODE_DEL_USERINFO_RSP=1026

class UserInfoInvalidError(xunit.utils.exception.XUnitException):
	pass


class UserInfo:
	def __init__(self,passkey=None):
		if passkey is None or len(passkey) != 8:
			raise Exception('can not be passkey none')
		self.__username = ''
		self.__userpass = ''
		self.__userflag = 0
		self.__userlevel = 0
		self.__passkey = passkey
		return

	def __del__(self):
		self.__username = ''
		self.__userpass = ''
		self.__userflag = 0
		self.__userlevel = 0
		self.__passkey = '\0' * 8
		return

	def GetString(self,s,size):
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
	def FormatString(self,s,size):
		rbuf = ''
		if len(s) < size:
			rbuf += s
			lsize = size - len(s)
			rbuf += '\0' * lsize
		else:
			rbuf += s[:(size-1)]
			rbuf += '\0'
		return rbuf

	def GetPass(self,s,size):
		rbuf = ''
		kd = pyDes.des(self.__passkey,pyDes.ECB,None,pad=None,padmode=pyDes.PAD_PKCS5)
		rbuf = kd.decrypt(s,padmode=pyDes.PAD_PKCS5)
		return self.GetString(rbuf,len(rbuf))

	def FormatPass(self,s,size):
		rbuf = ''
		ps = s 
		if len(ps) < 32:
			ps += '\0' * (32 - len(ps))
		else:
			ps = ps[:32]
		kd = pyDes.des(self.__passkey,pyDes.ECB,None,pad=None,padmode=pyDes.PAD_PKCS5)
		rbuf = kd.encrypt(ps)
		return self.FormatString(rbuf,size)

	def ParseBuf(self,buf):
		if len(buf) < TYPE_USERINFOR_STRUCT_LENGTH:
			raise UserInfoInvalidError('len (%d) < (%d)'%(len(buf),TYPE_USERINFOR_STRUCT_LENGTH))
		self.__username = self.GetString(buf,128)
		self.__userpass = self.GetPass(buf[128:],32)
		self.__userflag,self.__userlevel = struct.unpack('>HH',buf[256:260])
		return buf[TYPE_USERINFOR_STRUCT_LENGTH:]

	def FormatBuf(self):
		rbuf = ''
		rbuf += self.FormatString(self.__username,128)
		rbuf += self.FormatPass(self.__userpass,128)
		rbuf += struct.pack('>HH',self.__userflag,self.__userlevel)
		return rbuf

	def __Format(self):
		rbuf = ''
		rbuf += 'username     : (%s)\n'%(self.__username)
		rbuf += 'userpass     : (%s)\n'%(self.__userpass)
		rbuf += 'userflag     : (%d)\n'%(self.__userflag)
		rbuf += 'userlevel    : (%d)\n'%(self.__userlevel)
		return rbuf
	
	def __str__(self):
		return self.__Format()

	def __repr__(self):
		return self.__Format()


	def UserName(self,val=None):
		ov = self.__username
		if val is not None:
			self.__username = val
		return ov
	
	def UserPass(self,val=None):
		ov = self.__userpass
		if val is not None:
			self.__userpass = val
		return ov

	def UserFlag(self,val=None):
		ov = self.__userflag
		if val is not None:
			self.__userflag = val
		return ov

	def UserLevel(self,val=None):
		ov = self.__userlevel
		if val is not None:
			self.__userlevel = val
		return ov


class SdkUserInfo(syscp.SysCP):
	def __init__(self):
		syscp.SysCP.__init__(self)
		self.__userinfos = []
		return
	def __del__(self):
		syscp.SysCP.__del__(self)
		self.__userinfos = []
		return

	def FormatUserInfoSetReq(self,userinfo,sesid=None,seqid=None):
		if not isinstance(userinfo,UserInfo):
			raise UserInfoInvalidError('typeof(userinfo) not UserInfo')

		seqbuf = userinfo.FormatBuf()
		seqbuf = self.TypeCodeForm(TYPE_USERINFOR,seqbuf)
		sbuf =  self.FormatSysCp(SYSCODE_SET_USERINFO_REQ,1,seqbuf,sesid,seqid)
		logging.info('sbuf (%s)'%(repr(sbuf)))
		return sbuf

	def FormatUserInfoGetReq(self,sesid=None,seqid=None):
		sbuf= self.FormatSysCp(SYSCODE_GET_USERINFO_REQ,0,'',sesid,seqid)
		logging.info('sbuf (%s)'%(repr(sbuf)))
		return sbuf

	def FormatUserInfoDelReq(self,userinfo,sesid=None,seqid=None):
		if not isinstance(userinfo,UserInfo):
			raise UserInfoInvalidError('typeof(userinfo) not UserInfo')

		seqbuf = userinfo.FormatBuf()
		seqbuf = self.TypeCodeForm(TYPE_USERINFOR,seqbuf)
		sbuf = self.FormatSysCp(SYSCODE_DEL_USERINFO_REQ,1,seqbuf,sesid,seqid)
		#logging.info('sbuf (%s)'%(repr(sbuf)))
		return sbuf
		

	def ParseUserInfoSetRsp(self,buf):
		logging.info('buf %s'%(repr(buf)))
		attrbuf = self.UnPackSysCp(buf)
		if self.Code() != SYSCODE_SET_USERINFO_RSP:
			raise UserInfoInvalidError('Code (%d) != (%d)'%(self.Code(),SYSCODE_SET_USERINFO_RSP))
		if self.AttrCount() != 1:
			raise UserInfoInvalidError('attrcount (%d) != 1'%(self.AttrCount()))

		self.MessageCodeParse(attrbuf,'UserInfo Set Resp')
		return

	def ParseUserInfoGetRsp(self,buf,passkey):
		logging.info('buf %s'%(repr(buf)))
		attrbuf = self.UnPackSysCp(buf)
		if self.Code() != SYSCODE_GET_USERINFO_RSP:
			raise UserInfoInvalidError('Code (%d) != (%d)'%(self.Code(),SYSCODE_GET_USERINFO_RSP))

		if self.AttrCount() < 1:
			raise UserInfoInvalidError('attrcount (%d) < 1'%(self.AttrCount()))

		self.__userinfos = []
		for i in xrange(self.AttrCount()):
			attrbuf = self.ParseTypeCode(attrbuf)
			if self.TypeCode() != TYPE_USERINFOR:
				raise UserInfoInvalidError('typecode (%d) != (%d)'%(self.TypeCode(),TYPE_USERINFOR))
			userinfo = UserInfo(passkey)
			attrbuf = userinfo.ParseBuf(attrbuf)
			self.__userinfos.append(userinfo)
		return self.__userinfos

	def ParseUserInfoDelRsp(self,buf):
		#logging.info('buf %s'%(repr(buf)))
		attrbuf = self.UnPackSysCp(buf)
		if self.Code() != SYSCODE_DEL_USERINFO_RSP:
			raise UserInfoInvalidError('Code (%d) != (%d)'%(self.Code(),SYSCODE_DEL_USERINFO_RSP))
		if self.AttrCount() != 1:
			raise UserInfoInvalidError('attrcount (%d) != 1'%(self.AttrCount()))

		self.MessageCodeParse(attrbuf,'UserInfo Set Resp')
		return

