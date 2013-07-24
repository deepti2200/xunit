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

SYSCODE_GET_IPINFO_REQ=1013
SYSCODE_GET_IPINFO_RSP=1014

NET_INFO_STRUCT_LENGTH=296
MESSAGE_CODE_LENGTH=8

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

	def __GetString(self,s,size):
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
	def __FormatString(self,s,size):
		rbuf = ''
		if len(s) < size:
			rbuf += s
			lsize = size - len(s)
			rbuf += '\0' * lsize
		else:
			rbuf += s[:(size-1)]
			rbuf += '\0'
		return rbuf
		
	

	def GetNetId(self):
		return self.__netid

	def GetIfName(self):
		return self.__ifname

	def GetIpAddr(self):
		return self.__ipaddr

	def GetSubMask(self):
		return self.__submask

	def GetGateway(self):
		return self.__gateway

	def GetDns(self):
		return self.__dns

	def GetHwAddr(self):
		return self.__hwaddr

	def GetDhcp(self):
		return self.__dhcp

	def SetNetId(self,val):
		ov = self.__netid
		self.__netid = val
		return ov

	def SetIfName(self,val):
		ov = self.__ifname
		self.__ifname = val
		return ov

	def SetIpAddr(self,val):
		ov = self.__ipaddr
		self.__ipaddr = val
		return ov

	def SetSubMask(self,val):
		ov = self.__submask
		self.__submask = ov
		return ov

	def SetGateway(self,val):
		ov = self.__gateway
		self.__gateway = val
		return ov

	def SetDns(self,val):
		ov = self.__dns
		self.__dns = val
		return ov

	def SetHwAddr(self,val):
		ov = self.__hwaddr
		self.__hwaddr =val
		return ov

	def SetDhcp(self,val):
		ov = self.__dhcp
		self.__dhcp = val
		return ov

	def ParseBuffer(self,buf):
		if len(buf) < NET_INFO_STRUCT_LENGTH:
			raise NetInfoInvalidError('len(%d) < (%d)'%(len(buf),NET_INFO_STRUCT_LENGTH))
		self.__netid = struct.unpack('>I',buf[:4])[0]
		self.__ifname = self.__GetString(buf[4:36],32)
		self.__ipaddr = self.__GetString(buf[36:68],32)
		self.__submask = self.__GetString(buf[68:100],32)
		self.__gateway = self.__GetString(buf[100:132],32)
		self.__dns = self.__GetString(buf[132:260],128)
		self.__hwaddr = self.__GetString(buf[260:292],32)
		self.__dhcp = ord(buf[292])
		return

	def FormatBuffer(self):
		rbuf = ''
		rbuf += struct.pack('>I',self.__netid)
		rbuf += self.__FormatString(self.__ifname,32)
		rbuf += self.__FormatString(self.__ipaddr,32)
		rbuf += self.__FormatString(self.__submask,32)
		rbuf += self.__FormatString(self.__gateway,32)
		rbuf += self.__FormatString(self.__dns,128)
		rbuf += self.__FormatString(self.__hwaddr,32)
		rbuf += chr(self.__dhcp)
		rubf += chr(0)
		rubf += chr(0)
		rubf += chr(0)

		return rbuf

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
		return self.FormatSysCp(SYSCODE_GET_IPINFO_REQ,'',sesid,seqid)

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
			logging.info('ip %s hwaddr %s dns %s'%(netinfo.GetIpAddr(),netinfo.GetHwAddr(),netinfo.GetDns()))
			logging.info('ifname %s submask %s'%(netinfo.GetIfName(),netinfo.GetSubMask()))
			logging.info('netid %d'%(netinfo.GetNetId()))
			self.__netinfos.append(netinfo)

		
		return len(self.__netinfos)

	def GetIpInfo(self,idx):
		if idx >= len(self.__netinfos):
			raise SdkIpInfoOutRangeError('(%d) >= (%d)'%(idx,len(self.__netinfos)))
		return self.__netinfos[idx]
