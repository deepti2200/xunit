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

SDK_STREAM_OA_RESPONSE=0x4

SDK_STREAM_VD_SEND=5
SDK_STREAM_AD_SEND=6
class StreamPack:
	def __init__(self):
		self.__vcount = 0
		self.__vinfo = []
		self.__ainfo = None
		self.__ctrlcode = 0
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
		# now check for the framedata
		checkdata = self.__framedata[:10]
		if checkdata[0] != chr(0x0) or checkdata[1] != chr(0x0) :
			raise SdkStreamInvalidHeader('not valid i-frame data(%s)'%(repr(checkdata)))			
		if checkdata[2] != chr(0x0) or checkdata[3] != chr(0x1) :
			raise SdkStreamInvalidHeader('not valid i-frame data(%s)'%(repr(checkdata)))
		if checkdata[4] != chr(0x9) or checkdata[5] != chr(0x10):
			raise SdkStreamInvalidHeader('not valid i-frame data(%s)'%(repr(checkdata)))
		if checkdata[6] != chr(0x0) or checkdata[7] != chr(0x0):
			raise SdkStreamInvalidHeader('not valid i-frame data(%s)'%(repr(checkdata)))
		if checkdata[8] != chr(0x0) or checkdata[9] != chr(0x1):
			raise SdkStreamInvalidHeader('not valid i-frame data(%s)'%(repr(checkdata)))
		return 

	def __UnPackPFrame(self,buf):
		self.__frametype = 0
		self.__frameid = ord(buf[1])
		self.__frameidx = struct.unpack('>I',buf[4:8])[0]
		ptsh,ptsl = struct.unpack('>II',buf[8:16])
		self.__framepts = (ptsh << 32) + ptsl
		self.__framedata = buf[16:]
		checkdata = self.__framedata[:10]
		if checkdata[0] != chr(0x0) or checkdata[1] != chr(0x0) or\
			checkdata[2] != chr(0x0) or checkdata[3] != chr(0x1) or \
			checkdata[4] != chr(0x9) or checkdata[5] != chr(0x30) or \
			checkdata[6] != chr(0x0) or checkdata[7] != chr(0x0) or\
			checkdata[8] != chr(0x0) or checkdata[9] != chr(0x1):
			raise SdkStreamInvalidHeader('not valid p-frame data(%s)'%(repr(checkdata)))
		return 

	def __UnPackVideoFrame(self,buf):
		frametype = buf[4]
		if frametype == 'I':
			self.__UnPackIFrame(buf[4:])
		elif frametype == 'P':
			self.__UnPackPFrame(buf[4:])
		else:
			raise SdkStreamInvalidHeader('not recognize video type %s'%(repr(frametype)))
		return frametype == 'I' and 1 or 0

	def __UnPackAudioFrame(self,buf):
		if len(buf) < 28:
			raise SdkStreamInvalidHeader('buffer (%d) < 28 length'%(len(buf)))
		frametype = buf[4]
		if frametype != 'A':
			raise SdkStreamInvalidHeader('not recognize audio type %s'%(repr(frametype)))

		self.__framedata = buf[28:]		
		self.__frametype = frametype
		self.__frameidx = struct.unpack('>I',buf[12:16])[0]
		ptsh,ptsl =struct.unpack('>II', buf[16:24])
		self.__framepts = (ptsh << 32) + ptsl
		return frametype

	def UnPackStream(self,buf):
		# now unpack for the streams first to test for the type of frame
		vcode = struct.unpack('>I',buf[:4])[0]
		if vcode != SDK_STREAM_VD_SEND and vcode != SDK_STREAM_OD_SEND :
			raise SdkStreamInvalidHeader('vcode (%d) != (%d)'%(vcode,SDK_STREAM_VD_SEND))

		if vcode == SDK_STREAM_VD_SEND:
			return self.__UnPackVideoFrame(buf)
		else:
			return self.__UnPackAudioFrame(buf)

	def __UnPackVideoCtrl(self,buf):
		# now to unpacket the ctrl information
		opcode=struct.unpack('>I',buf[:4])[0]

		if opcode != SDK_STREAM_OV_RESPONSE :
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
		self.__ctrlcode = SDK_STREAM_OV_RESPONSE
		return SDK_STREAM_OV_RESPONSE

	def __UnPackAudioCtrl(self,buf):
		opcode=struct.unpack('>I',buf[:4])[0]
		assert(opcode == SDK_STREAM_OA_RESPONSE)
		self.__ainfo = None
		result = struct.unpack('>I',buf[4:8])[0]
		if result != 0:
			logging.error('open audio failed')
			return 0
		encodetype,rsvd,channel,bitpersample,samplepersec = struct.unpack('>CCCCI',buf[8:16])
		self.__ainfo = [encodetype,channel,bitpersample,samplepersec]
		self.__ctrlcode = SDK_STREAM_OA_RESPONSE
		return SDK_STREAM_OA_RESPONSE
		

	def UnPackCtrl(self,buf):
		opcode=struct.unpack('>I',buf[:4])[0]

		if opcode != SDK_STREAM_OV_RESPONSE and opcode != SDK_STREAM_OA_RESPONSE:
			raise SdkStreamInvalidHeader('can not recognize ctrl code %d'%(opcode))

		if opcode == SDK_STREAM_OV_RESPONSE:
			return self.__UnPackVideoCtrl(buf)
		elif opcode == SDK_STREAM_OA_RESPONSE:
			return self.__UnPackAudioCtrl(buf)
			

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

	def GetAInfo(self):
		return self.__ainfo
	def GetCtrlCode(self):
		return self.__ctrlcode

	def PackOpenVideo(self,streamflags):
		buf = struct.pack('>I',SDK_STREAM_OV_REQUEST)
		buf += struct.pack('>H',streamflags)
		# packet for the  reserved
		buf += struct.pack('>H',0)
		return buf

	def GetFrameId(self):
		return self.__frameid
