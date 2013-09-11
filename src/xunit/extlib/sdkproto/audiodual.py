#! python


'''
this is the file for handling of audio dual packet handling
'''
import struct

        import sys
        import os
        import hashlib
        import logging
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..')))
import xunit.utils.exception

START_TALK_REQUEST_LENGTH=68
START_TALK_RESPONSE_LENGTH=68
AUDIO_FRAME_BASIC_LENGTH=24
AUDIO_FRAME_CMD=0x6
AUDIO_DUAL_START_REQUEST=0x9
AUDIO_DUAL_START_RESPONSE=0xa

class AudioInInvalidError(xunit.utils.exception.XUnitException):
	pass

class AudioOutInvalidError(xunit.utils.exception.XUnitException):
	pass

class StartTalkRequest:
	def __ResetVar(self):
		self.__transtype = 0
		self.__broadcast = 0
		self.__reserv1 = 0
		self.__dstaddr = ''
		self.__dstport = 0
		self.__encodetype = 1
		self.__channel = 1
		self.__bitspersample = 16
		self.__reserv2 = 0
		self.__samplepersec = 8000
		self.__avgbytespersec = self.__channel * self.__bitspersample * self.__samplepersec / 8
		self.__framerate = 50
		self.__bitrate = self.__samplepersec
		self.__volume = 50
		self.__aecflag = 0
		self.__aecdelaytime = 0
		self.__reserv3 = 0
		return
		
	def __init__(self):
		self.__ResetVar()
		return

	def __del__(self):
		self.__ResetVar()
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

	def ParseBuf(self,rbuf):
		if len(rbuf) < (START_TALK_REQUEST_LENGTH ):
			raise AudioInInvalidError('len(%d) < (%d )'%(len(rbuf),START_TALK_REQUEST_LENGTH))
		code = struct.unpack('>I',rbuf[:4])[0]
		if code != AUDIO_DUAL_START_REQUEST:
			raise AudioInInvalidError('startrequest code (%d) != (%d)'%(code,AUDIO_DUAL_START_REQUEST))
		self.__transtype = ord(rbuf[4])
		self.__broadcast = ord(rbuf[5])
		self.__reserv1 = struct.unpack('>H',rbuf[6:8])[0]
		self.__dstaddr = self.GetString(rbuf[8:40],32)
		self.__dstport = struct.unpack('>I',rbuf[40:44])[0]
		self.__encodetype = ord(rbuf[44])
		self.__channel = ord(rbuf[45])
		self.__bitpersample = ord(rbuf[46])
		self.__reserv2 = ord(rbuf[47])
		self.__samplepersec , self.__avgbytespersec = struct.unpack('>II',rbuf[48:56])
		self.__framerate , self.__bitrate , self.__volume , self.__aecflag , self.__aecdelaytime,self.__reserv3 = struct.unpack('>HHHHHH',rbuf[56:68])
		return rbuf[START_TALK_REQUEST_LENGTH:]

	def FormatBuf(self):
		rbuf = ''
		rbuf += struct.pack('>I',AUDIO_DUAL_START_REQUEST)
		rbuf += chr(self.__transtype)
		rbuf += chr(self.__broadcast)
		rbuf += struct.pack('>H',self.__reserv1)
		rbuf += self.FormatString(self.dstaddr,32)
		rbuf += struct.pack('>I',self.__dstport)
		rbuf += chr(self.__encodetype)
		rbuf += chr(self.__channel)
		rbuf += chr(self.__bitpersample)
		rbuf += chr(self.__reserv2)
		rbuf += struct.pack('>II',self.__samplepersec,self.__avgbytespersec)
		rbuf += struct.pack('>HHHHHH',self.__framerate,self.__bitrate,self.__volume,self__aecflag,self.__aecdelaytime,self.__reserv3)
		return rbuf

	def __Format(self):
		rbuf = ''
		rbuf += 'transtype               : %d\n'%(self.__transtype)
		rbuf += 'broadcast               : %d\n'%(self.__broadcast)
		rbuf += 'reserv1                 : %d\n'%(self.__reserv1)
		rbuf += 'dstaddr                 : (%s)\n'%(self.__dstaddr)
		rbuf += 'dstport                 : %d\n'%(self.__dstport)
		rbuf += 'encodetype              : %d\n'%(self.__encodetype)
		rbuf += 'channel                 : %d\n'%(self.__channel)
		rbuf += 'bitpersample            : %d\n'%(self.__bitpersample)
		rbuf += 'reserv2                 : %d\n'%(self.__reserv2)
		rbuf += 'samplepersec            : %d\n'%(self.__samplepersec)
		rbuf += 'avgbytespersec          : %d\n'%(self.__avgbytespersec)
		rbuf += 'framerate               : %d\n'%(self.__framerate)
		rbuf += 'bitrate                 : %d\n'%(self.__bitrate)
		rbuf += 'volume                  : %d\n'%(self.__volume)
		rbuf += 'aecflag                 : %d\n'%(self.__aecflag)
		rbuf += 'aecdelaytime            : %d\n'%(self.__aecdelaytime)
		rbuf += 'reserv3                 : %d\n'%(self.__reserv3)
		return rbuf

	def __str__(self):
		return self.__Format()

	def __expr__(self):
		return self.__Format()

	def TransType(self,val=None):
		ov = self.__transtype
		if val is not None:
			self.__transtype = val
		return ov

	def Broadcase(self,val=None):
		ov = self.__broadcast
		if val is not None:
			self.__broadcast = val
		return ov

	def Reserv1(self,val=None):
		ov = self.__reserv1
		if val is not None:
			self.__reserv1 = val
		return ov

	def DstAddr(self,val=None):
		ov = self.__dstaddr
		if val is not None:
			self.__dstaddr = val
		return ov

	def DstPort(self,val=None):
		ov = self.__dstport
		if val is not None:
			self.__dstport = val
		return ov
		
	def EncodeType(self,val=None):
		ov = self.__encodetype
		if val is not None:
			self.__encodetype = val
		return ov
	def Channel(self,val=None):
		ov = self.__channel
		if val is not None:
			self.__channel = val
		return ov

	def BitPerSample(self,val=None):
		ov = self.__bitpersample
		if val is not None:
			self.__bitpersample = val
		return ov

	def Reserv2(self,val=None):
		ov = self.__reserv2
		if val is not None:
			self.__reserv2 = val
		return ov

	def SamplePerSec(self,val=None):
		ov = self.__samplepersec
		if val is not None:
			self.__samplepersec = val
		return ov

	def AvgBytesPerSec(self,val=None):
		ov = self.__avgbytespersec
		if val is not None:
			self.__avgbytespersec = val
		return ov

	def FrameRate(self,val=None):
		ov = self.__framerate
		if val is not None:
			self.__framerate = val
		return ov

	def BitRate(self,val=None):
		ov = self.__bitrate
		if val is not None:
			self.__bitrate = val
		return ov

	def Volume(self,val=None):
		ov = self.__volume
		if val is not None:
			self.__volume = val
		return ov

	def AecFlag(self,val=None):
		ov = self.__aecflag
		if val is not None:
			self.__aecflag = val
		return ov

	def AecDelayTime(self,val=None):
		ov = self.__aecdelaytime
		if val is not None:
			self.__aecdelaytime = val
		return ov

	def Reserv3(self,val=None):
		ov = self.__reserv3
		if val is not None:
			self.__reserv3 = val
		return ov


class StartTalkResponse:
	def __ResetVar(self):
		self.__result = 0
		self.__dstaddr = ''
		self.__dstport = 0
		self.__encodetype = 1
		self.__channel = 1
		self.__bitspersample = 16
		self.__reserv1 = 0
		self.__samplepersec = 8000
		self.__avgbytespersec = self.__channel * self.__bitspersample * self.__samplepersec / 8
		self.__framerate = 50
		self.__bitrate = self.__samplepersec
		self.__volume = 50
		self.__aecflag = 0
		self.__aecdelaytime = 0
		self.__reserv2 = 0
		return
		
	def __init__(self):
		self.__ResetVar()
		return

	def __del__(self):
		self.__ResetVar()
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

	def ParseBuf(self,rbuf):
		if len(rbuf) < START_TALK_RESPONSE_LENGTH:
			raise AudioInInvalidError('len(%d) < (%d)'%(len(rbuf),START_TALK_RESPONSE_LENGTH))
		code,self.__result = struct.unpack('>II',rbuf[:8])
		if code != AUDIO_DUAL_START_RESPONSE:
			raise AudioInInvalidError('code (%d) != (%d)'%(code,AUDIO_DUAL_START_RESPONSE))
		if self.__result != 0:
			raise AudioInInvalidError('result (%d) != 0'%(self.__result))
		self.__dstaddr = self.GetString(rbuf[8:40],32)
		self.__dstport = struct.unpack('>I',rbuf[40:44])[0]
		self.__encodetype = ord(rbuf[44])
		self.__channel = ord(rbuf[45])
		self.__bitpersample = ord(rbuf[46])
		self.__reserv1 = ord(rbuf[47])
		self.__samplepersec , self.__avgbytespersec = struct.unpack('>II',rbuf[48:56])
		if self.__avgbytespersec != (self.__samplepersec * self.__bitspersample * self.__channel / 8):
			raise AudioInInvalidError('avgbytes (%d) != (%d * %d *%d /8)'%(self.__avgbytespersec,\
				self.__channel,self.__bitspersample,self.__samplepersec))
		self.__framerate , self.__bitrate , self.__volume , self.__aecflag , self.__aecdelaytime,self.__reserv3 = struct.unpack('>HHHHHH',rbuf[56:68])
		return rbuf[START_TALK_RESPONSE_LENGTH:]

	def FormatBuf(self):
		rbuf = ''
		rbuf += struct.pack('>II',AUDIO_DUAL_START_RESPONSE,self.__result)
		rbuf += self.FormatString(self.dstaddr,32)
		rbuf += struct.pack('>I',self.__dstport)
		rbuf += chr(self.__encodetype)
		rbuf += chr(self.__channel)
		rbuf += chr(self.__bitpersample)
		rbuf += chr(self.__reserv1)
		rbuf += struct.pack('>II',self.__samplepersec,self.__avgbytespersec)
		rbuf += struct.pack('>HHHHHH',self.__framerate,self.__bitrate,self.__volume,self__aecflag,self.__aecdelaytime,self.__reserv2)
		return rbuf

	def __Format(self):
		rbuf = ''
		rbuf += 'result                  : %d\n'%(self.__result)
		rbuf += 'dstaddr                 : (%s)\n'%(self.__dstaddr)
		rbuf += 'dstport                 : %d\n'%(self.__dstport)
		rbuf += 'encodetype              : %d\n'%(self.__encodetype)
		rbuf += 'channel                 : %d\n'%(self.__channel)
		rbuf += 'bitpersample            : %d\n'%(self.__bitpersample)
		rbuf += 'reserv1                 : %d\n'%(self.__reserv1)
		rbuf += 'samplepersec            : %d\n'%(self.__samplepersec)
		rbuf += 'avgbytespersec          : %d\n'%(self.__avgbytespersec)
		rbuf += 'framerate               : %d\n'%(self.__framerate)
		rbuf += 'bitrate                 : %d\n'%(self.__bitrate)
		rbuf += 'volume                  : %d\n'%(self.__volume)
		rbuf += 'aecflag                 : %d\n'%(self.__aecflag)
		rbuf += 'aecdelaytime            : %d\n'%(self.__aecdelaytime)
		rbuf += 'reserv2                 : %d\n'%(self.__reserv2)
		return rbuf

	def __str__(self):
		return self.__Format()

	def __expr__(self):
		return self.__Format()


	def Reserv1(self,val=None):
		ov = self.__reserv1
		if val is not None:
			self.__reserv1 = val
		return ov

	def DstAddr(self,val=None):
		ov = self.__dstaddr
		if val is not None:
			self.__dstaddr = val
		return ov

	def DstPort(self,val=None):
		ov = self.__dstport
		if val is not None:
			self.__dstport = val
		return ov
		
	def EncodeType(self,val=None):
		ov = self.__encodetype
		if val is not None:
			self.__encodetype = val
		return ov
	def Channel(self,val=None):
		ov = self.__channel
		if val is not None:
			self.__channel = val
		return ov

	def BitPerSample(self,val=None):
		ov = self.__bitpersample
		if val is not None:
			self.__bitpersample = val
		return ov

	def Reserv2(self,val=None):
		ov = self.__reserv2
		if val is not None:
			self.__reserv2 = val
		return ov

	def SamplePerSec(self,val=None):
		ov = self.__samplepersec
		if val is not None:
			self.__samplepersec = val
		return ov

	def AvgBytesPerSec(self,val=None):
		ov = self.__avgbytespersec
		if val is not None:
			self.__avgbytespersec = val
		return ov

	def FrameRate(self,val=None):
		ov = self.__framerate
		if val is not None:
			self.__framerate = val
		return ov

	def BitRate(self,val=None):
		ov = self.__bitrate
		if val is not None:
			self.__bitrate = val
		return ov

	def Volume(self,val=None):
		ov = self.__volume
		if val is not None:
			self.__volume = val
		return ov

	def AecFlag(self,val=None):
		ov = self.__aecflag
		if val is not None:
			self.__aecflag = val
		return ov

	def AecDelayTime(self,val=None):
		ov = self.__aecdelaytime
		if val is not None:
			self.__aecdelaytime = val
		return ov




class AudioFramePack:
	def __ResetVar(self):
		self.__frametype = 'A'
		self.__encodetype = 1
		self.__channel = 1
		self.__bitspersample = 16
		self.__samplepersec = 8000
		self.__frameid = 0
		self.__pts = 0
		self.__avgbytespersec = self.__channel * self.__bitspersample * self.__samplepersec / 8
		return

	def __init__(self):
		self.__ResetVar()
		return

	def __del__(self):
		self.__ResetVar()
		return

	def ParseBuf(self,rbuf):
		if len(rbuf) < AUDIO_FRAME_BASIC_LENGTH:
			raise AudioInInvalidError('len(%d) < (%d)'%(len(rbuf),AUDIO_FRAME_BASIC_LENGTH))
		if rbuf[0] != 'A':
			raise AudioInInvalidError('rbuf[0] %s not (A)'%(repr(rbuf[0])))

		self.__frametype = rbuf[0]
		self.__encodetype = ord(rbuf[1])
		self.__channel = ord(rbuf[2])
		self.__bitspersample = ord(rbuf[3])
		self.__samplepersec ,self.__frameid = struct.unpack('>II',rbuf[4:12])
		ptsh,ptsl = struct.unpack('>II',rbuf[12:20])
		self.__pts = (ptsh << 32) + ptsl
		self.__avgbytespersec = struct.unpack('>I',rbuf[20:24])[0]

		if self.__avgbytespersec != (self.__channel * self.__bitspersample * self.__samplepersec / 8):
			raise AudioInInvalidError('avgbytespersec (%d) != (%d * %d *%d / 8)'%(self.__avgbytespersec,\
				self.__channel,self.__bitspersample,self.__samplepersec))
		return rbuf[AUDIO_FRAME_BASIC_LENGTH:]

	def FormatBuf(self):
		rbuf = ''
		rbuf += self.__frametype
		rbuf += chr(self.__encodetype)
		rbuf += chr(self.__channel)
		rbuf += chr(self.__bitspersample)

		rbuf += struct.pack('>II',self.__samplepersec,self.__frameid)
		ptsh = (self.__pts >> 32) & 0xffffffff
		ptsl = (self.__pts ) & 0xffffffff
		rbuf += struct.pack('>III',ptsh,ptsl,self.__avgbytespersec)
		return rbuf

	def __Format(self):
		rbuf  = ''
		rbuf += 'frametype             : (%s)\n'%(repr(self.__frametype))
		rbuf += 'encodetype            : %d\n'%(self.__encodetype)
		rbuf += 'channel               : %d\n'%(self.__channel)
		rbuf += 'bitspersample         : %d\n'%(self.__bitspersample)
		rbuf += 'samplepersec          : %d\n'%(self.__samplepersec)
		rbuf += 'frameid               : %d\n'%(self.__frameid)
		rbuf += 'pts                   : 0x%x\n'%(self.__pts)
		rbuf += 'avgbytespersec        : %d\n'%(self.__avgbytespersec)
		return rbuf

	def __str__(self):
		return self.__Format()


	def __repr__(self):
		return self.__Format()

	def FrameType(self,val=None):
		ov = self.__frametype
		if val is not None:
			self.__frametype = val
		return ov

	def EncodeType(self,val=None):
		ov = self.__encodetype
		if val is not None:
			self.__encodetype = val
		return ov

	def Channel(self,val=None):
		ov = self.__channel
		if val is not None:
			self.__channel = val
		return ov

	def BitsPerSample(self,val=None):
		ov = self.__bitspersample
		if val is not None:
			self.__bitspersample = val
		return ov

	def SamplePerSec(self,val=None):
		ov = self.__samplepersec
		if val is not None:
			self.__samplepersec = val
		return ov

	def FrameId(self,val=None):
		ov = self.__frameid
		if val is not None:
			self.__frameid = val
		return ov

	def Pts(self,val=None):
		ov = self.__pts
		if val is not None:
			self.__pts = val
		return ov

	def AvgBytesPerSec(self,val=None):
		ov = self.__avgbytespersec
		if val is not None:
			self.__avgbytespersec = val
		return ov



class AudioOutPack:
	def __ResetVar(self):
		return

	def __init__(self):
		self.__ResetVar()
		return

	def __del__(self):
		self.__ResetVar()
		return



	def PackStream(self,framepack,data):
		if not isinstance(framepack,AudioFramePack) :
			raise AudioOutInvalidError('framepack parameter must AudioFramePack class')
		sdata = struct.pack('>I',AUDIO_FRAME_CMD)
		sdata += framepack.FormatBuf()
		sdata += data
		return sdata

class AudioInPack:
	def __ResetVar(self):
		self.__framepack = None
		self.__framedata = None
		return

	def __init__(self):
		self.__ResetVar()
		return

	def __del__(self):
		self.__ResetVar()
		return

	def UnPackStream(self,rbuf):
		if len(rbuf) < (4 + AUDIO_FRAME_BASIC_LENGTH):
			raise AudioInInvalidError('len(%d) < (4 + %d)'%(len(rbuf),AUDIO_FRAME_BASIC_LENGTH))
		cmd = struct.unpack('>I',rbuf[:4])[0]
		if cmd != AUDIO_FRAME_CMD:
			raise AudioInInvalidError('cmd (%d) != (%d)'%(cmd,AUDIO_FRAME_CMD))
		self.__framepack = AudioFramePack()
		self.__framedata = self.__framepack.ParseBuf(rbuf[4:])		
		return len(self.__framedata)

	def FramePack(self):
		return self.__framepack

	def FrameData(self):
		return self.__framedata

