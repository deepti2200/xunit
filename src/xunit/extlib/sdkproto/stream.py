#! python


'''
	this is the file for handling of the stream packet handle
'''
import struct

import sys
import os
import hashlib
import logging
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..')))
import xunit.utils.exception

class SdkStreamInvalidHeader(xunit.utils.exception.XUnitException):
	pass

SDK_STREAM_OV_REQUEST=0x1
SDK_STREAM_OV_RESPONSE=0x2

class StreamPack:
	def __init__(self):
		self.__vcount = 0
		self.__vinfo = []
		self.__frametype = -1
		self.__frameid = -1
		self.__framefreq = -1
		self.__frameenctype = -1
		self.__frameFop = -1
		self.__framePts = -1
		self.__frameidx = -1
		self.__framewidth = -1
		self.__frameheight = -1
		self.__framedata = None
		return

	def __del__(self):
		return


	def __UnPackIFrame(self,buf):
		self.__frametype = 1
		self.__frameid = ord(buf[1])
		self.__framefreq = ord(buf[2])
		self.__frameenctype = ord(buf[3])
		self.__framefop = ord(buf[4])
		ptsh,ptsl = struct.unpack('>II',buf[8:16])
		self.__framepts = (ptsh << 32) + (ptsl)
		self.__frameidx = struct.unpack('>I',buf[16:20])[0]
		self.__framewidth = struct.unpack('>H',buf[20:22])[0]
		self.__frameheight = struct.unpack('>H',buf[22:24])[0]
		self.__framedata = buf[24:]
		return 

	def __UnPackPFrame(self,buf):
		self.__frametype = 0
		self.__frameid = ord(buf[1])
		self.__frameidx = struct.unpack('>I',buf[4:8])[0]
		ptsh,ptsl = struct.unpack('>II',buf[8:16])
		self.__framepts = (ptsh << 32) + ptsl
		self.__framedata = buf[16:]
		return 

	def UnPackStream(self,buf):
		# now unpack for the streams first to test for the type of frame
		frametype = buf[0]

		if frametype != 'I' and frametype != 'P':
			raise SdkStreamInvalidHeader('not recognize type %s'%(repr(frametype)))

		if frametype == 'I':
			self.__UnPackIFrame(buf)
		else:
			self.__UnPackPFrame(buf)

		return frametype == 'I' and 1 or 0

	def UnPackCtrl(self,buf):
		# now to unpacket the ctrl information
		opcode=struct.unpack('>I',buf[:4])[0]

		if opcode != SDK_STREAM_OV_RESPONSE:
			raise SdkStreamInvalidHeader('opcode (%d) != (%d)'%(opcode,SDK_STREAM_OV_RESPONSE))

		result = struct.unpack('>I',buf[4:8])[0]
		count = struct.unpack('>I',buf[8:12])[0]
		if result != 0 and count == 0:
			raise SdkStreamInvalidHeader('result (%d) and count (%d)'(result,count))

		if count > 4:
			raise SdkStreamInvalidHeader('count (%d) > 4'%(count))
		sizeofvinfo = 12
		self.__vinfo = []
		for i in xrange(count):
			part = buf[(12+i*sizeofvinfo):]
			vinfo = part[:12]
			vres = struct.unpack('>I',vinfo[:4])[0]
			if vres == 0:
				vstreamid = ord(vinfo[4])
				vrate = ord(vinfo[5])
				vfop = ord(vinfo[6])
				vtype = ord(vinfo[7])
				vwidth = struct.unpack('>H',vinfo[8:10])[0]
				vheight = struct.unpack('>H',vinfo[10:12])[0]
				vcontrolblock = [vstreamid,vrate,vfop,vtype,vtype,vwidth,vheight]
				if vtype != 1:
					raise SdkStreamInvalidHeader('only support h264 but type (%d)'%(vtype))
				self.__vinfo.append(vcontrolblock)
		self.__vcount = len(self.__vinfo)
		return self.__vcount

	def GetFrameData(self):
		return self.__framedata

	def GetFrameIdx(self):
		return self.__frameidx

	def GetFrameType(self):
		return self.__frametype

	def GetFramePts(self):
		return self.__framepts;

	def GetVInfo(self):
		return self.__vinfo

	def PackOpenVideo(self,streamflags):
		buf = struct.pack('>I',SDK_STREAM_OV_REQUEST)
		buf += struct.pack('>H',streamflags)
		# packet for the  reserved
		buf += struct.pack('>H',0)
		return buf

	def GetFrameId(self):
		return self.__frameid