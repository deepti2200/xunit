#! python

'''
	this is the file for the showcfg set and get
'''

import struct

import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..')))
import xunit.utils.exception
import xunit.extlib.sdkproto.syscp as syscp


SYSCODE_SET_SHOWCFG_REQ=1041
SYSCODE_SET_SHOWCFG_RSP=1042
SYSCODE_GET_SHOWCFG_REQ=1043
SYSCODE_GET_SHOWCFG_RSP=1044


TYPE_SHOWCFG=13
TYPE_SHOWCFG_STRUCT_LENGTH=210
TYPE_SHOWCFG_LENGTH=(TYPE_SHOWCFG_STRUCT_LENGTH+4)


class ShowCfgInvalidError(xunit.utils.exception.XUnitException):
	pass


class ShowCfg:
	def __init__(self):
		self.__videoid = 1
		self.__flag = 0
		self.__tm_enable = 0
		self.__tm_language = 0
		self.__tm_displayx = 0
		self.__tm_displayy = 0
		self.__tm_datestyle = 0
		self.__tm_timestyle = 0
		self.__tm_fontcolor = 0
		self.__tm_fontsize = 0
		self.__tm_fontbold = 0
		self.__tm_fontrotate = 0
		self.__tm_fontitalic = 0
		self.__tm_fontoutline = 0

		self.__ch_enable = 0
		self.__ch_displayx = 0
		self.__ch_displayy = 0
		self.__ch_fontcolor = 0
		self.__ch_fontsize = 0
		self.__ch_fontbold = 0
		self.__ch_fontrotate = 0
		self.__ch_fontitalic = 0
		self.__ch_fontoutline = 0
		self.__ch_channelname = ''
		return

	def __del__(self):
		self.__videoid = 1
		self.__flag = 0
		self.__tm_enable = 0
		self.__tm_language = 0
		self.__tm_displayx = 0
		self.__tm_displayy = 0
		self.__tm_datestyle = 0
		self.__tm_timestyle = 0
		self.__tm_fontcolor = 0
		self.__tm_fontsize = 0
		self.__tm_fontbold = 0
		self.__tm_fontrotate = 0
		self.__tm_fontitalic = 0
		self.__tm_fontoutline = 0

		self.__ch_enable = 0
		self.__ch_displayx = 0
		self.__ch_displayy = 0
		self.__ch_fontcolor = 0
		self.__ch_fontsize = 0
		self.__ch_fontbold = 0
		self.__ch_fontrotate = 0
		self.__ch_fontitalic = 0
		self.__ch_fontoutline = 0
		self.__ch_channelname = ''
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
	def ParseBuf(self,buf):
		if len(buf) < TYPE_SHOWCFG_STRUCT_LENGTH:
			raise ShowCfgInvalidError('len(%d) < (%d)'%(len(buf),TYPE_SHOWCFG_STRUCT_LENGTH))


		self.__videoid ,self.__flag,self.__tm_enable ,\
		self.__tm_language ,self.__tm_displayx,	self.__tm_displayy ,\
		self.__tm_datestyle,self.__tm_timestyle,self.__tm_fontcolor,\
		self.__tm_fontsize,self.__tm_fontbold,self.__tm_fontrotate,\
		self.__tm_fontitalic,self.__tm_fontoutline,self.__ch_enable,\
		self.__ch_displayx,self.__ch_displayy,self.__ch_fontcolor,\
		self.__ch_fontsize,self.__ch_fontbold,self.__ch_fontrotate,\
		self.__ch_fontitalic,self.__ch_fontoutline = struct.unpack('>IIIIIIIIIIIIIIIIIIIIIII',buf[:92])

		self.__ch_channelname = self.GetString(buf[92:],128)
		return buf[TYPE_SHOWCFG_STRUCT_LENGTH:]

	def FormatBuf(self):
		rbuf = ''
		rbuf += struct.pack('>IIIIIIIIIIIIIIIIIIIIIII',self.__videoid ,self.__flag,self.__tm_enable ,\
		self.__tm_language ,self.__tm_displayx,	self.__tm_displayy ,\
		self.__tm_datestyle,self.__tm_timestyle,self.__tm_fontcolor,\
		self.__tm_fontsize,self.__tm_fontbold,self.__tm_fontrotate,\
		self.__tm_fontitalic,self.__tm_fontoutline,self.__ch_enable,\
		self.__ch_displayx,self.__ch_displayy,self.__ch_fontcolor,\
		self.__ch_fontsize,self.__ch_fontbold,self.__ch_fontrotate,\
		self.__ch_fontitalic,self.__ch_fontoutline)

		rbuf += self.FormatString(self.__ch_channelname,128)
		return rbuf

	def __Format(self):
		rbuf = ''
		rbuf += 'videoid         : %d\n'%(self.__videoid)
		rbuf += 'flag            : %d\n'%(self.__flag)
		rbuf += 'tm_enable       : %d\n'%(self.__tm_enable)
		rbuf += 'tm_language     : %d\n'%(self.__tm_language)
		rbuf += 'tm_displayx     : %d\n'%(self.__tm_displayx)
		rbuf += 'tm_displayy     : %d\n'%(self.__tm_displayy)
		rbuf += 'tm_datestyle    : %d\n'%(self.__tm_datestyle)
		rbuf += 'tm_timestyle    : %d\n'%(self.__tm_timestyle)
		rbuf += 'tm_fontcolor    : %d\n'%(self.__tm_fontcolor)
		rbuf += 'tm_fontsize     : %d\n'%(self.__tm_fontsize)
		rbuf += 'tm_fontbold     : %d\n'%(self.__tm_fontbold)
		rbuf += 'tm_fontrotate   : %d\n'%(self.__tm_fontroate)
		rbuf += 'tm_fontitalic   : %d\n'%(self.__tm_fontitalic)
		rbuf += 'tm_fontoutline  : %d\n'%(self.__tm_fontoutline)
		rbuf += 'ch_enable       : %d\n'%(self.__ch_enable)
		rbuf += 'ch_displayx     : %d\n'%(self.__ch_displayx)
		rbuf += 'ch_displayy     : %d\n'%(self.__ch_displayy)
		rbuf += 'ch_fontcolor    : %d\n'%(self.__ch_fontcolor)
		rbuf += 'ch_fontsize     : %d\n'%(self.__ch_fontsize)
		rbuf += 'ch_fontbold     : %d\n'%(self.__ch_fontbold)
		rbuf += 'ch_fontrotate   : %d\n'%(self.__ch_fontrotate)
		rbuf += 'ch_fontitalic   : %d\n'%(self.__ch_fontitalic)
		rbuf += 'ch_fontoutline  : %d\n'%(self.__ch_fontoutline)

		rbuf += 'ch_channelname  : %s\n'%(self.__ch_channelname,128)
		return rbuf

	def __str__(self):
		return self.__Format()

	def __repr__(self):
		return self.__Format()

class SdkShowCfg(syscp.SysCP):
	def __init__(self):
		syscp.SysCP.__init__(self)
		self.__showcfg = None
		return
	def __del__(self):
		syscp.SysCP.__del__(self)
		self.__showcfg = None
		return

	def FormGetReq(self,sesid=None,seqid=None):
		pass

	def ParseGetRsp(self,buf):
		pass

