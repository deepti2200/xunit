#! python


import socket
import select
import random
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))
import xunit.utils.exception
import sdkproto.login
import sdkproto.pack


class SdkSockInvalidParam(xunit.utils.exception):
	pass

class SdkSockConnectError(xunit.utils.exception):
	pass


class SdkSockSendError(xunit.utils.exception):
	pass

class SdkSockRecvError(xunit.utils.exception):
	pass

class SdkSock:
	def __SeqIdInit(self):
		random.seed(time.time())
		self.__seqid = random.randint(((1<<16)-1))
		return

	def __IncSeqId(self):
		self.__seqid += 1
		if self.__seqid >= (1<< 16):
			self.__seqid = 0
		return self.__seqid

	def __SendBuf(self,buf,msg=None):
		try:
			self.__sock.send(buf)
		except:
			raise SdkSockSendError('could not send %d (%s)'%(len(buf),msg))
		return

	def __RcvBuf(self,size,msg=None):
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
		self.__SeqIdInit()
		try:
			self.__sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			self.__sock.connect(self.__host,self.__port)
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
		sbuf = packproto.Pack(0,self.__IncSeqId(),0x80,reqbuf)
		self.__SendBuf(sbuf,'login init')
		rbuf = self.__RcvBuf(20,'received login init')

		fraglen,bodylen = packproto.ParseHeader(rbuf)
		if packproto.SeqId() != self.__seqid :
			raise SdkSockRecvError('recv seqid (%d) != seqid (%d)'%(packproto.SeqId(),self.__seqid))

		if packproto.SesId() != 0x80:
			raise SdkSockRecvError('recv sesid (0x%x) != seqid (0x80)'%(packproto.SesId()))
		rbuf = self.__RcvBuf(fraglen + bodylen,'response init login')
		# now we should parse the rbuf for the 
		authcode,md5check = sdklogin.UnPackUnAuthorized(rbuf[fraglen:])
		assert(authcode == 0x2)

		# now we should give the handle
		reqbuf = sdklogin.PackLoginSaltRequest(self.__IncSeqId(),authcode,user,password,md5check,900,10)
		sbuf = packproto.Pack(0,self.__seqid,0x80,reqbuf)
		self.__SendBuf(sbuf,'login check request')

		rbuf = self.__RcvBuf(20,'login chech response')
		fraglen,bodylen = packproto.ParseHeader(rbuf)
		if packproto.SeqId() != self.__seqid :
			raise SdkSockRecvError('recv seqid (%d) != seqid (%d)'%(packproto.SeqId(),self.__seqid))

		if packproto.SesId() != 0x80:
			raise SdkSockRecvError('recv sesid (0x%x) != seqid (0x80)'%(packproto.SesId()))
		rbuf = self.__RcvBuf(fraglen + bodylen,'response init login')

		return sdklogin.UnPackSession(rbuf[fraglen:])			
		
		

	def LoginSessionId(self,sesid):
		pass

		
