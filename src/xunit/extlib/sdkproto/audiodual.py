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

START_TALK_REQUEST_LENGTH=64

class AudioInInvalidError(xunit.utils.exception.XUnitException):
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
		if len(rbuf) < START_TALK_REQUEST_LENGTH:
			raise AudioInInvalidError('len(%d) < (%d)'%(len(rbuf),START_TALK_REQUEST_LENGTH))

		self.__transtype = ord(rbuf[0])
		self.__broadcast = ord(rbuf[1])
		self.__reserv1 = struct.unpack('>H',rbuf[2:4])[0]
		self.__dstaddr = self.GetString(rbuf[4:36],32)
		self.__dstport = struct.unpack('>I',rbuf[36:40])[0]
		self.__encodetype = ord(rbuf[40])
		self.__channel = ord(rbuf[41])
		self.__bitpersample = ord(rbuf[42])
		self.__reserv2 = ord(rbuf[43])
		self.__samplepersec , self.__avgbytespersec = struct.unpack('>II',rbuf[44:52])
		self.__framerate , self.__bitrate , self.__volume , self.__aecflag , self.__aecdelaytime,self.__reserv3 = struct.unpack('>HHHHHH',rbuf[52:64])
		return rbuf[START_TALK_REQUEST_LENGTH:]

	def FormatBuf(self):
		rbuf = ''
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


class AudioOutPack:
	def __ResetVar(self):
		return

	def __init__(self):
		self.__ResetVar()
		return

	def __del__(self):
		self.__ResetVar()
		return



	def PackStream(self,data):
		sdata =
		return sdata

class AudioInPack:
	def __ResetVar(self):
		self.__frameidx = None
		self.__framedata = None
		return

	def __init__(self):
		self.__ResetVar()
		return

	def __del__(self):
		self.__ResetVar()
		return

	def UnPackStream(self,rbuf):
		return len(self.__framedata)

