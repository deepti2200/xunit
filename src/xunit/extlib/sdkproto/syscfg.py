#! python

'''
	this is the file for the sysctl
'''

import struct

import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..')))
import xunit.utils.exception
import syscp


SYSCODE_SET_SYSCFG_REQ=1051
SYSCODE_SET_SYSCFG_RSP=1052
SYSCODE_GET_SYSCFG_REQ=1053
SYSCODE_GET_SYSCFG_RSP=1054

TYPE_IPCNAME=101
TYPE_IPCNAME_LENGTH=420


class SysCfgInvalidError(xunit.utils.exception.XUnitException):
	pass


class IPCName:
	def __init__(self):
		self.__devicename = ''
		self.__deviceid = 0
		self.__devicemodel=''
		self.__devicemanufactor=''
		self.__devicesn =''
		self.__devicefwver = ''
		self.__devicehwver = ''
		return

	def __del__(self):
		self.__devicename = ''
		self.__deviceid = 0
		self.__devicemodel=''
		self.__devicemanufactor=''
		self.__devicesn =''
		self.__devicefwver = ''
		self.__devicehwver = ''
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

	def ParseSysCfg(self,buf):
		if len(buf) < TYPE_IPCNAME_LENGTH:
			raise SysCfgInvalidError('len(%d) < (%d)'%(len(buf),TYPE_IPCNAME_LENGTH))

		self.__devicename = self.GetString(buf,128)
		self.__deviceid = struct.unpack('>I',buf[128:132])[0]
		self.__devicemodel = self.GetString(buf[132:],32)
		self.__devicemanufactor = self.GetString(buf[164:],64)
		self.__devicesn = self.GetString(buf[228:],64)
		self.__devicefwver = self.GetString(buf[292:],64)
		self.__devicehwver = self.GetString(buf[356:],64)
		return buf[TYPE_IPCNAME_LENGTH:]
	def FormatSysCfg(self):
		rbuf = ''
		rbuf += self.FormatString(self.__devicename,128)
		rbuf += struct.pack('>I',self.__deviceid)
		rbuf += self.FormatString(self.__devicemodel,32)
		rbuf += self.FormatString(self.__devicemanufactor,64)
		rbuf += self.FormatString(self.__devicesn,64)
		rbuf += self.FormatString(self.__devicefwver,64)
		rbuf += self.FormatString(self.__devicehwver,64)
		return rbuf

	def __FormatString(self):
		rbuf = ''
		rbuf += 'Device Name : %s;\n'%(self.__devicename)
		rbuf += 'Device Id   : %d;\n'%(self.__deviceid)
		rbuf += 'Device model: %s;\n'%(self.__devicemod)
		rbuf += 'Device Manu : %s;\n'%(self.__devicemanufactor)
		rbuf += 'Device SN   : %s;\n'%(self.__devicesn)
		rbuf += 'Device FWVer: %s;\n'%(self.__devicefwver)
		rbuf += 'Device HWVer: %s;\n'%(self.__devicehwver)
		return rbuf

	def __str__(self):
		return self.__FormatString()

	def __repr__(self):
		return self.__FormatString()

	def DeviceName(self,val=None):
		ov = self.__devicename
		if val is not None:
			self.__devicename = val
		return ov

	def DeviceId(self,val=None):
		ov = self.__deviceid
		if val is not None:
			self.__deviceid = val
		return ov

	def DeviceModel(self,val=None):
		ov = self.__devicemodel
		if val is not None:
			self.__devicemodel = val
		return ov

	def DeviceManufactor(self,val=None):
		ov = self.__devicemanufactor
		if val is not None:
			self.__devicemanufactor = val
		return ov

	def DeviceSN(self,val=None):
		ov = self.__devicesn
		if val is not None:
			self.__devicesn = val
		return ov

	def DeviceFWVer(self,val=None):
		ov = self.__devicefwver
		if val is not None:
			self.__devicefwver= val
		return ov

	def DeviceHWVer(self,val=None):
		ov = self.__devicehwver
		if val is not None:
			self.__devicehwver = val
		return ov


class SdkSysCfgInvalidError(xunit.utils.exception.XUnitException):
	pass


class SdkSysCfg(syscp.SysCP):
	def __init__(self):
		syscp.SysCP.__init__(self)
		self.__syscfg = None
		return

	def __del__(self):
		syscp.SysCP.__del__(self)
		self.__syscfg = None
		return


	def FormatQuery(self,sesid=None,seqid=None):
		return self.FormatSysCp(SYSCODE_GET_SYSCFG_REQ,0,'',sesid,seqid)

	def ParseQuerySysCfgResp(self,buf):
		attrbuf = self.UnPackSysCp(buf)

		if self.Code() != SYSCODE_GET_SYSCFG_RESP:
			raise SdkSysCfgInvalidError('code (%d) != (%d)'%(self.Code() , SYSCODE_GET_SYSCFG_RESP))
		

