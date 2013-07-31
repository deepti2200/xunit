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
import syscp

SYSCODE_SET_IPINFO_REQ=1011
SYSCODE_SET_IPINFO_RESP=1012
SYSCODE_GET_IPINFO_REQ=1013
SYSCODE_GET_IPINFO_RSP=1014


NET_INFO_STRUCT_LENGTH=296

class SdkIpInfoInvalidError(xunit.utils.exception.XUnitException):
	pass

class SdkIpInfoOutRangeError(xunit.utils.exception.XUnitException):
	pass

class NetInfoInvalidError(xunit.utils.exception.XUnitException):
	pass



class NetInfo:
	def __init__(self):
		self.__netid = -1
		self.__ifname = ''
		self.__ipaddr = ''
		self.__submask = ''
		self.__gateway = ''
		self.__dns = ''
		self.__hwaddr = ''
		self.__dhcp = -1
		return

	def __del__(self):
		self.__netid = -1
		self.__ifname = ''
		self.__ipaddr = ''
		self.__submask = ''
		self.__gateway = ''
		self.__dns = ''
		self.__hwaddr = ''
		self.__dhcp = -1
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
		
	

	def NetId(self,val=None):
		ov = self.__netid
		if val is not None:
			self.__netid = val
		return ov

	def IfName(self,val=None):
		ov = self.__ifname
		if val is not None:
			self.__ifname = val
		return ov
	def IpAddr(self,val=None):
		ov = self.__ipaddr
		if val is not None:
			self.__ipaddr = val
		return ov
	def SubMask(self,val=None):
		ov = self.__submask
		if val is not None:
			self.__submask = val
		return ov
	def Gateway(self,val=None):
		ov = self.__gateway
		if val is not None:
			self.__gateway = val
		return ov
	def Dns(self,val=None):
		ov = self.__dns
		if val is not None:
			self.__dns = val
		return ov
	def HwAddr(self,val=None):
		ov = self.__hwaddr
		if val is not None:
			self.__hwaddr = val
		return ov

	def Dhcp(self,val=None):
		ov = self.__dhcp
		if val is not None:
			self.__dhcp = val
		return ov




	def ParseBuffer(self,buf):
		if len(buf) < NET_INFO_STRUCT_LENGTH:
			raise NetInfoInvalidError('len(%d) < (%d)'%(len(buf),NET_INFO_STRUCT_LENGTH))
		self.__netid = struct.unpack('>I',buf[:4])[0]
		self.__ifname = self.GetString(buf[4:36],32)
		self.__ipaddr = self.GetString(buf[36:68],32)
		self.__submask = self.GetString(buf[68:100],32)
		self.__gateway = self.GetString(buf[100:132],32)
		self.__dns = self.GetString(buf[132:260],128)
		self.__hwaddr = self.GetString(buf[260:292],32)
		self.__dhcp = ord(buf[292])
		return

	def FormatBuffer(self):
		rbuf = ''
		rbuf += struct.pack('>I',self.__netid)
		rbuf += self.FormatString(self.__ifname,32)
		rbuf += self.FormatString(self.__ipaddr,32)
		rbuf += self.FormatString(self.__submask,32)
		rbuf += self.FormatString(self.__gateway,32)
		rbuf += self.FormatString(self.__dns,128)
		rbuf += self.FormatString(self.__hwaddr,32)
		rbuf += chr(self.__dhcp)
		rbuf += chr(0)
		rbuf += chr(0)
		rbuf += chr(0)

		return rbuf

	def __Format(self):
		rbuf = ''
		rbuf += 'netid        : %d\n'%(self.__netid)
		rbuf += 'ifname       : %s\n'%(self.__ifname)
		rbuf += 'submask      : %s\n'%(self.__submask)
		rbuf += 'gateway      : %s\n'%(self.__gateway)
		rbuf += 'dns          : %s\n'%(self.__dns)
		rbuf += 'hwaddr       : %s\n'%(self.__hwaddr)
		rbuf += 'dhcp         : %d\n'%(self.__dhcp)
		return rbuf

	def __str__(self):
		return self.__Format()

	def __repr__(self):
		return self.__Format()

class SdkIpInfo(syscp.SysCP):
	def __init__(self):
		syscp.SysCP.__init__(self)
		self.__res = -1
		self.__netinfos = []
		return

	def __del__(self):
		syscp.SysCP.__del__(self)
		self.__res = -1
		self.__netinfos = []
		return

	def FormatQueryInfo(self,seqid,sesid):
		return self.FormatSysCp(SYSCODE_GET_IPINFO_REQ,0,'',sesid,seqid)

	def ParseQueryInfo(self,buf):
		respbuf = self.UnPackSysCp(buf)

		if self.Code() != SYSCODE_GET_IPINFO_RSP:
			raise SdkIpInfoInvalidError('code (%d) != (%d)'%(self.Code(),SYSCODE_GET_IPINFO_RSP))

		if self.AttrCount() < 1:
			raise SdkIpInfoInvalidError('attrcount (%d) < 1'%(self.AttrCount()))


		attrbuf = self.PackedBuf()
		self.__netinfos = []
		for i in xrange(self.AttrCount()):
			typebuf = attrbuf[:syscp.TYPE_INFO_LENGTH]			
			typecode,typelen = struct.unpack('>HH',typebuf[:syscp.TYPE_INFO_LENGTH])
			if typecode != syscp.TYPE_IPINFOR:
				raise SdkIpInfoInvalidError('typecode (%d) != (%d)'%(typecode,syscp.TYPE_IPINFOR))
			if (typelen ) > len(attrbuf):
				raise SdkIpInfoInvalidError('left len (%d) < (%d + %d)'%(len(attrbuf),typelen , syscp.TYPE_INFO_LENGTH))
			pbuf = attrbuf[syscp.TYPE_INFO_LENGTH:(typelen)]
			attrbuf = attrbuf[(typelen):]
			netinfo = NetInfo()
			netinfo.ParseBuffer(pbuf)
			self.__netinfos.append(netinfo)
		return self.__netinfos

	def GetIpInfo(self,idx):
		if idx >= len(self.__netinfos):
			raise SdkIpInfoOutRangeError('(%d) >= (%d)'%(idx,len(self.__netinfos)))
		return self.__netinfos[idx]

	def __FormatSetIpInfo(self,netinfo):
		rbuf = ''
		# first we should format type info
		rbuf += struct.pack('>HH',syscp.TYPE_IPINFOR,NET_INFO_STRUCT_LENGTH+syscp.TYPE_INFO_LENGTH)
		rbuf += netinfo.FormatBuffer()
		return rbuf

	def FormatSetIpInfo(self,netinfo,sesid=None,seqid=None):
		passok = 0
		if isinstance(netinfo,NetInfo) :
			passok = 1
		if isinstance(netinfo,list) :
			passok = 1
			for ni in netinfo:
				if not isinstance(ni,NetInfo):
					passok = 0
					break
		if passok == 0:
			raise SdkIpInfoInvalidError('netinfo must be NetInfo instance')

		# now to form the set info
		reqbuf = ''
		if isinstance(netinfo,list):
			attrcount = len(netinfo)
			for ni in netinfo:
				reqbuf += self.__FormatSetIpInfo(ni)
		else:
			attrcount =1
			reqbuf += self.__FormatSetIpInfo(netinfo)
		return self.FormatSysCp(SYSCODE_SET_IPINFO_REQ,attrcount,reqbuf,sesid,seqid)

	def ParseSetIpInfoResp(self,buf):
		attrbuf = self.UnPackSysCp(buf)
		if len(attrbuf) < (syscp.TYPE_MESSAGE_CODE_LENGTH + syscp.TYPE_INFO_LENGTH ):
			raise SdkIpInfoInvalidError('len(%d) < (%d + %d )'%(len(buf),syscp.MESSAGE_CODE_LENGTH,syscp.TYPE_INFO_LENGTH))
		if self.AttrCount() != 1:
			raise SdkIpInfoInvalidError('attrcount (%d) != 1'%(self.AttrCount()))

		if self.Code() != SYSCODE_SET_IPINFO_RESP:
			raise SdkIpInfoInvalidError('code (%d) != (%d)'%(self.Code(),SYSCODE_SET_IPINFO_RESP))

		typecode,typelen = struct.unpack('>HH',attrbuf[:syscp.TYPE_INFO_LENGTH])
		if typecode != syscp.TYPE_MESSAGECODE:
			raise SdkIpInfoInvalidError('typecode (%d) != (%d)'%(typecode,syscp.TYPE_MESSAGECODE))

		if typelen < (syscp.TYPE_INFO_LENGTH + syscp.TYPE_MESSAGE_CODE_LENGTH):
			raise SdkIpInfoInvalidError('typelen (%d) < (%d + %d)'%(typelen,syscp.TYPE_INFO_LENGTH,syscp.TYPE_MESSAGE_CODE_LENGTH))
		
		mesgcodebuf = attrbuf[syscp.TYPE_INFO_LENGTH:]
		res,reslen = struct.unpack('>II',mesgcodebuf[:8])
		if res != 0:
			raise SdkIpInfoInvalidError('set ipinfo res (%d)'%(res))
		if typelen != (syscp.TYPE_INFO_LENGTH + syscp.TYPE_MESSAGE_CODE_LENGTH + reslen):
			raise SdkIpInfoInvalidError('typelen (%d) != (%d + %d + %d)'(typelen,syscp.TYPE_INFO_LENGTH,syscp.TYPE_MESSAGE_CODE_LENGTH,reslen))
		return res
