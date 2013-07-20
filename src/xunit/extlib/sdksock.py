#! python


import socket
import select
import random
import time
import os
import sys
import logging
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))
import xunit.utils.exception
import sdkproto.login
import sdkproto.pack
import sdkproto.stream


class SdkSockInvalidParam(xunit.utils.exception.XUnitException):
	pass

class SdkSockConnectError(xunit.utils.exception.XUnitException):
	pass


class SdkSockSendError(xunit.utils.exception.XUnitException):
	pass

class SdkSockRecvError(xunit.utils.exception.XUnitException):
	pass

class SdkSock:
	def __SeqIdInit(self):
		random.seed(time.time())
		self.__seqid = random.randint(0,((1<<16)-1))
		return

	def IncSeqId(self):
		self.__seqid += 1
		if self.__seqid >= (1<< 16):
			self.__seqid = 0
		return self.__seqid

	def SendBuf(self,buf,msg=None):
		try:
			self.__sock.send(buf)
		except:
			raise SdkSockSendError('could not send %d (%s)'%(len(buf),msg))
		return

	def RcvBuf(self,size,msg=None):
		leftsize = size
		rcved = 0
		rbuf = ''
		while leftsize > 0:
			cbuf = self.__sock.recv(leftsize)
			if cbuf is None or len(cbuf) == 0:
				raise SdkSockSendError('could not receive (%d) (%s)'%(size,msg))
			leftsize -= len(cbuf)
			rcved += len(cbuf)
			rbuf += cbuf
		return rbuf
		
	def __init__(self,host=None,port=0):
		if host is None:
			raise SdkSockInvalidParam('host can not be None')
		if port == 0:
			raise SdkSockInvalidParam('port can not be 0')
		self.__host = host
		self.__port = port
		self.__sesid = None
		self.__SeqIdInit()
		try:
			self.__sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			self.__sock.connect((self.__host,self.__port))
		except:
			self.__sock.close()
			self.__sock = None
			raise SdkSockConnectError('can not connect to(%s:%d)'%(self.__host,self.__port))
		return 

	def CloseSocket(self):
 		if hasattr(self,'__sock') and self.__sock:
 			self.__sock.close()
 		self.__sock = None
 		return

	def __del__(self):
		self.CloseSocket()
		return

	

	def LoginUserPass(self,user,password):
		if self.__sock is None:
			raise SdkSockInvalidParam('Not connect %s:%d'%(self.__host,self.__port))

		# now we should handle for the connect user and password
		sdklogin = sdkproto.login.LoginPack()
		packproto = sdkproto.pack.SdkProtoPack()
		reqbuf = sdklogin.PackLoginRequest(0,user,password,900,10)
		sbuf = packproto.Pack(0,self.IncSeqId(),0x80,reqbuf)
		self.SendBuf(sbuf,'login init')
		rbuf = self.RcvBuf(20,'received login init')

		fraglen,bodylen = packproto.ParseHeader(rbuf)
		if packproto.SeqId() != self.__seqid :
			raise SdkSockRecvError('recv seqid (%d) != seqid (%d)'%(packproto.SeqId(),self.__seqid))

		if packproto.SesId() != 0:
			raise SdkSockRecvError('recv sesid (0x%x) != seqid (0)'%(packproto.SesId()))
		if packproto.TypeId() != 0x80:
			raise SdkSockRecvError('recv typeid (0x%x) != typeid (0x80)'%(packproto.TypeId()))
		rbuf = self.RcvBuf(fraglen + bodylen,'response init login')
		# now we should parse the rbuf for the 
		authcode,md5check = sdklogin.UnPackUnAuthorized(rbuf[fraglen:])
		assert(authcode == 0x2)

		# now we should give the handle
		reqbuf = sdklogin.PackLoginSaltRequest(self.IncSeqId(),authcode,user,password,md5check,900,10)
		sbuf = packproto.Pack(0,self.__seqid,0x80,reqbuf)		
		#logging.info('sending req (%d) %s seqid %d'%(len(reqbuf),repr(reqbuf),self.__seqid))
		self.SendBuf(sbuf,'login check request')

		rbuf = self.RcvBuf(20,'login check response')
		fraglen,bodylen = packproto.ParseHeader(rbuf)
		if packproto.SeqId() != self.__seqid :
			raise SdkSockRecvError('recv seqid (%d) != seqid (%d)'%(packproto.SeqId(),self.__seqid))

		if packproto.SesId() == 0 :
			raise SdkSockRecvError('recv sesid (0x%x) == sesid (0)'%(packproto.SesId()))
		rbuf = self.RcvBuf(fraglen + bodylen,'response init login')
		#logging.info('rbuf [%d] (%s)'%(bodylen,repr(rbuf[fraglen:])))
		getsesid = sdklogin.UnPackSession(rbuf[fraglen:])
		if getsesid != packproto.SesId():
			raise SdkSockRecvError('from packet response sesid(%d) != packet sessionid (%d)'%(getsesid,packproto.SesId()))
		self.__sesid = getsesid
		return getsesid
		
		

	def LoginSessionId(self,sesid):
		if self.__sock is None:
			raise SdkSockInvalidParam('Not connect %s:%d'%(self.__host,self.__port))

		# now we should handle for the connect user and password
		sdklogin = sdkproto.login.LoginPack()
		packproto = sdkproto.pack.SdkProtoPack()
		reqbuf = sdklogin.LoginPackSession(sesid)
		sbuf = packproto.Pack(sesid,self.IncSeqId(),sdkproto.pack.GMIS_PROTOCOL_TYPE_LOGGIN,reqbuf)
		self.SendBuf(sbuf,'session login request')
		rbuf = self.RcvBuf(sdkproto.pack.GMIS_BASE_LEN,'session login response')
		fraglen,bodylen = packproto.ParseHeader(rbuf)
		rbody = self.RcvBuf(fraglen+bodylen,'receive packet')
		if fraglen != 0:
			raise SdkSockRecvError('fraglen %d != 0'%(fraglen))
		if bodylen != 76:
			raise SdkSockRecvError('bodylen %d != 76'%(bodylen))

		if packproto.SeqId() != self.__seqid:
			raise SdkSockRecvError('Recv seqid(%d) != (%d)'%(packproto.SeqId(),self.__seqid))
		logging.info('at [%d] seqid %d sessionid %d'%(time.time(),self.__seqid,sesid))

		getsesid = sdklogin.UnPackSession(rbody[fraglen:])
		if getsesid != sesid:
			raise SdkSockRecvError('getsesid (%d) != (%d)'%(getsesid,sesid))
		self.__sesid = sesid
		return sesid

	def SessionId(self):
		return self.__sesid


class SdkStreamSock(SdkSock):
	def	__init__(self,host,port):
		SdkSock.__init__(self,host,port)
		self.__streampack = sdkproto.stream.StreamPack()
		self.__basepack = sdkproto.pack.SdkProtoPack()
		return

	def StartStream(self,streamids):
		# now first to pack for the sending
		streamflags = 0
		logging.info('streamids %s'%(repr(streamids)))
		for i in streamids:
			logging.info('i %s'%(repr(i)))
			ivalue = (1 << int(i))
			streamflags |= ivalue
		reqbuf = self.__streampack.PackOpenVideo(streamflags)
		sbuf = self.__basepack.Pack(self.SessionId(),self.IncSeqId(),sdkproto.pack.GMIS_PROTOCOL_TYPE_MEDIA_CTRL,reqbuf)
		self.SendBuf(sbuf,'send media ctrl for %s'%(repr(streamids)))
		rbuf = self.RcvBuf(20,'receive open video response')
		fragle,bodylen = self.__basepack.ParseHeader(rbuf)
		if self.__basepack.SeqId() != 0:
			raise SdkSockRecvError('get seqid (%d) != 0'%(self.__basepack.SeqId()))
		rbuf = self.RcvBuf(fraglen+bodylen,'Receive video response')
		count = self.__streampack.UnPackCtrl(rbuf[fraglen:])

		if count == 0 :
			raise SdkSockRecvError('parse response with 0 count')
		
		return

	def StopStream(self):
		return

	def GetStreamPacket(self):
		rbuf = self.RcvBuf(20,'')
		sdkpack = sdkproto.stream.StreamPack()
		packproto = sdkproto.pack.SdkProtoPack()

		# now to give the socket packet
		fraglen,bodylen = self.__basepack.ParseHeader(rbuf)
		if fraglen != 0 :
			raise SdkSockRecvError('fraglen %d != 0'%(fraglen))
		rbuf = self.RcvBuf(fraglen+bodylen,'read stream packet')
		if self.__basepack.TypeId() == sdkproto.pack.GMIS_PROTOCOL_TYPE_MEDIA_CTRL:
			self.__streampack.UnPackCtrl(rbuf[fraglen:])
			return sdkproto.pack.GMIS_PROTOCOL_TYPE_MEDIA_CTRL
		elif self.__basepack.TypeId() == sdkproto.pack.GMIS_PROTOCOL_TYPE_MEDIA_DATA:
			self.__streampack.UnPackStream(rbuf[fraglen:])
			return sdkproto.pack.GMIS_PROTOCOL_TYPE_MEDIA_DATA
		else:
			raise SdkSockRecvError('typeid (0x%x) not valid'%(self.__basepack.TypeId()))
		return None

	def GetVInfo(self):
		return self.__streampack.GetVInfo();
	def GetStreamData(self):
		return self.__streampack.GetFrameData()

	def GetStreamIdx(self):
		return self.__streampack.GetFrameIdx()

	def GetStreamPts(self):
		return self.__streampack.GetFramePts()
	def GetStreamId(self):
		return self.__streampack.GetFrameId()