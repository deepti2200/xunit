#! python


import socket
import select
import random
import time
import select
import os
import sys
import logging
import re
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))
import xunit.utils.exception
import sdkproto.login
import sdkproto.pack
import sdkproto.stream
import sdkproto.ipinfo
import sdkproto.videocfg
import sdkproto.syscfg
import sdkproto.sysctl
import sdkproto.ptz
import sdkproto.showcfg
import sdkproto.time
import sdkproto.imagine
import sdkproto.netport
import sdkproto.advimagine
import sdkproto.workstate
import sdkproto.userinfo
import sdkproto.audiodual
import xunit.extlib.xDES as xDES

class SdkSockInvalidParam(xunit.utils.exception.XUnitException):
	pass

class SdkSockConnectError(xunit.utils.exception.XUnitException):
	pass

class SdkSockSetoptError(xunit.utils.exception.XUnitException):
	pass

class SdkSockSendError(xunit.utils.exception.XUnitException):
	pass

class SdkSockRecvError(xunit.utils.exception.XUnitException):
	pass

class SdkSockRecvTimeoutError(xunit.utils.exception.XUnitException):
	pass


class SdkSock:
	def __SeqIdInit(self):
		random.seed(time.time())
		self.__seqid = random.randint(0,((1<<16)-1))
		self.__sesid = None
		return

	def IncSeqId(self):
		self.__seqid += 1
		if self.__seqid >= (1<< 16):
			self.__seqid = 0
		return self.__seqid
	def SeqId(self,val=None):
		ov = self.__seqid
		if val is not None:
			self.__seqid = val
		return ov

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

	def RcvBufTimeout(self,size,timeout=3.0,msg=None):
		leftsize = size
		rcved = 0
		rbuf = ''
		stime  = time.time()
		ctime  = stime
		etime  = stime + timeout
		try:
			while leftsize > 0:
				if ctime >= etime:
					raise SdkSockRecvTimeoutError('receive %s timeout(%d)'%(msg,timeout))
				ltime = etime - ctime
				rsock = [self.__sock]
				wsock = []
				xsock = []
				retrsock,retwsock,retxsock = select.select(rsock,wsock,xsock,ltime)
				if len(retrsock)>0:
					cbuf = self.__sock.recv(leftsize)
					rbuf += cbuf
					leftsize -= len(cbuf)
					rcved += len(cbuf)
				ctime = time.time()
		except:
			raise SdkSockRecvTimeoutError('receive %s error'%(msg))
		return rbuf
			
		
	def __init__(self,host=None,port=0):
		if host is None:
			raise SdkSockInvalidParam('host can not be None')
		if port == 0:
			raise SdkSockInvalidParam('port can not be 0')
		self.__host = host
		self.__port = port
		self.__sesid = None
		self.__basepack = sdkproto.pack.SdkProtoPack()
		self.__SeqIdInit()
		try:
			self.__sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			self.__sock.connect((self.__host,self.__port))
		except:
			self.__sock.close()
			self.__sock = None
			raise SdkSockConnectError('can not connect to(%s:%d)'%(self.__host,self.__port))
		return 

		


	def __IsLinuxSystem(self):
		vpat = re.compile('linux',re.I)
		if vpat.search(sys.platform):
			return 1
		else:
			return 0

	def __ReadRMemMax(self):
		cmd = 'cat /proc/sys/net/core/rmem_max'
		sp = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		op = sp.stdout
		ls = op.readlines()
		l = ls[0]
		l = l.rstrip('\r\n')
		return int(l)

	def __SetRMemMax(self,bufdsize):
		cmd = 'sudo su -c \'echo %d >/proc/sys/net/core/rmem_max\''%(bufdsize)
		ret = os.system(cmd)
		if ret != 0:
			raise SdkSockSetoptError('can not run cmd(%s) succ please to set sudo no password running'%(cmd))
		return
	def __SetRcvBuf(self,bufsize):
		# now to set the socket buffer size
		osize = self.__sock.getsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF)
		if (bufsize << 1) > osize:
			# now we set the buffer
			self.__sock.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,bufsize)
			nsize = self.__sock.getsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF)
			if nsize < (bufsize * 2):
				if not self.__IsLinuxSystem():
					raise SdkSockSetoptError('can not reset the rmem_max in platform %s'%(sys.platform))
				self.__SetRMemMax((bufsize << 1))
				self.__sock.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,bufsize)
				nsize = self.__sock.getsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF)
				if nsize < (bufsize << 1):
					raise SdkSockSetoptError('can not expand buffer size   %d'%(bufsize))
		return
	def SetRcvBuffer(self,bufsize):
		if self.__sock is None:
			raise SdkSockConnectError('not connected to(%s:%d)'%(self.__host,self.__port))

		self.__SetRcvBuf(bufsize)
		return

	def CloseSocket(self):
 		if hasattr(self,'__sock') and self.__sock:
 			self.__sock.close()
 		self.__sock = None
 		return

	def __del__(self):
		self.CloseSocket()
		self.__basepack = None
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
		rbuf = self.RcvBuf(sdkproto.pack.GMIS_BASE_LEN,'received login init')

		fraglen,bodylen = packproto.ParseHeader(rbuf)
		if packproto.SeqId() != self.__seqid :
			raise SdkSockRecvError('recv seqid (%d) != seqid (%d)'%(packproto.SeqId(),self.__seqid))

		if packproto.SesId() != 0:
			raise SdkSockRecvError('recv sesid (0x%x) != seqid (0)'%(packproto.SesId()))
		if packproto.TypeId() != 0x80:
			raise SdkSockRecvError('recv typeid (0x%x) != typeid (0x80)'%(packproto.TypeId()))
		rbuf = self.RcvBuf(fraglen + bodylen,'response init login')
		# now we should parse the rbuf for the 
		authcode,deskey = sdklogin.UnPackUnAuthorized(rbuf[fraglen:])
		assert(authcode == 0x4)

		# now we should give the handle
		reqbuf = sdklogin.PackLoginSaltRequest(self.IncSeqId(),authcode,user,password,deskey,900,10)
		sbuf = packproto.Pack(0,self.__seqid,sdkproto.pack.GMIS_PROTOCOL_TYPE_LOGGIN,reqbuf)		
		#logging.info('sending req (%d) %s seqid %d'%(len(reqbuf),repr(reqbuf),self.__seqid))
		self.SendBuf(sbuf,'login check request')

		rbuf = self.RcvBuf(sdkproto.pack.GMIS_BASE_LEN,'login check response')
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
		sbuf = packproto.PackHeartBeat(sesid,self.IncSeqId(),sdkproto.pack.GMIS_PROTOCOL_TYPE_LOGGIN,reqbuf)
		self.SendBuf(sbuf,'session login request')
		rbuf = self.RcvBuf(sdkproto.pack.GMIS_BASE_LEN,'session login response')
		fraglen,bodylen = packproto.ParseHeader(rbuf)
		rbody = self.RcvBuf(fraglen+bodylen,'receive packet')
		if fraglen != 0:
			raise SdkSockRecvError('fraglen %d != 0'%(fraglen))
		if bodylen != 80:
			raise SdkSockRecvError('bodylen %d != 76'%(bodylen))

		if (packproto.Flag() & sdkproto.pack.GSSP_HEADER_FLAG_FHB ) == 0:
			raise SdkSockRecvError('not set heart beat flag')

		if packproto.SeqId() != self.__seqid:
			raise SdkSockRecvError('Recv seqid(%d) != (%d)'%(packproto.SeqId(),self.__seqid))
		#logging.info('at [%d] seqid %d sessionid %d'%(time.time(),self.__seqid,sesid))

		getsesid = sdklogin.UnPackSession(rbody[fraglen:])
		if getsesid != sesid:
			raise SdkSockRecvError('getsesid (%d) != (%d)'%(getsesid,sesid))
		self.__sesid = sesid
		return sesid

	def SessionId(self,val=None):
		ov = self.__sesid
		if val is not None:
			self.__sesid = val
		return ov

	def PackGsspBuf(self,typeid,reqbuf):
		sbuf = self.__basepack.Pack(self.SessionId(),self.IncSeqId(),typeid,reqbuf)
		return sbuf
	def UnPackGsspBuf(self,gssphdr):
		return self.__basepack.ParseHeader(gssphdr)

	def SendAndRecv(self,reqbuf,msg=None):
		sbuf = self.__basepack.Pack(self.SessionId(),self.SeqId(),sdkproto.pack.GMIS_PROTOCOL_TYPE_CONF,reqbuf)
		self.SendBuf(sbuf,'request %s'%(msg and msg or 'Cmd'))
		rbuf = self.RcvBuf(sdkproto.pack.GMIS_BASE_LEN,'response %s'%(msg and msg or 'Cmd'))
		fraglen , bodylen = self.__basepack.ParseHeader(rbuf)
		if fraglen > 0 :
			raise SdkSockRecvError('fraglen (%d) != 0'%(fraglen))
		if self.__basepack.TypeId() != sdkproto.pack.GMIS_PROTOCOL_TYPE_CONF:
			raise SdkSockRecvError('get typeid %d != (%d)'%(self.__basepack.TypeId(),sdkproto.pack.GMIS_PROTOCOL_TYPE_CONF))

		if self.__basepack.SesId() != self.SessionId():
			raise SdkSockRecvError('session id %d != (%d)'%(self.__basepack.SesId(),self.SessionId()))
		if self.__basepack.SeqId() != self.SeqId():
			raise SdkSockRecvError('seq id %d != (%d) (%s)'%(self.__basepack.SeqId(),self.SeqId(),repr(rbuf)))
		rbuf = self.RcvBuf(bodylen,'response body %s'%(msg and msg or 'Cmd'))
		return rbuf


class SdkStreamSock(SdkSock):
	def	__init__(self,host,port):
		SdkSock.__init__(self,host,port)
		self.__streampack = sdkproto.stream.StreamPack()
		self.__basepack = sdkproto.pack.SdkProtoPack()
		return

	def StartStream(self,streamids):
		# now first to pack for the sending
		streamflags = 0
		#logging.info('streamids %s'%(repr(streamids)))
		for i in streamids:
			#logging.info('i %s'%(repr(i)))
			ivalue = (1 << int(i))
			streamflags |= ivalue
		reqbuf = self.__streampack.PackOpenVideo(streamflags)
		sbuf = self.__basepack.Pack(self.SessionId(),self.IncSeqId(),sdkproto.pack.GMIS_PROTOCOL_TYPE_MEDIA_CTRL,reqbuf)
		self.SendBuf(sbuf,'send media ctrl for %s'%(repr(streamids)))
		rbuf = self.RcvBuf(sdkproto.pack.GMIS_BASE_LEN,'receive open video response')
		fraglen,bodylen = self.__basepack.ParseHeader(rbuf)
		if self.__basepack.SeqId() != self.SeqId():
			raise SdkSockRecvError('get seqid (%d) != (%d)'%(self.__basepack.SeqId(),self.SeqId()))
		#logging.info('seqid (%d)'%(self.SeqId()))
		rbuf = self.RcvBuf(fraglen+bodylen,'Receive video response')
		count = self.__streampack.UnPackCtrl(rbuf[fraglen:])

		if count == 0 :
			raise SdkSockRecvError('parse response with 0 count')
		
		return

	def StopStream(self):
		return

	def GetStreamPacket(self):
		rbuf = self.RcvBuf(sdkproto.pack.GMIS_BASE_LEN,'')
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
		return self.__streampack.GetVInfo()

	def GetAInfo(self):
		return self.__streampack.GetAInfo()
	
	def GetStreamData(self):
		return self.__streampack.GetFrameData()

	def GetStreamIdx(self):
		return self.__streampack.GetFrameIdx()

	def GetStreamPts(self):
		return self.__streampack.GetFramePts()
	def GetStreamId(self):
		return self.__streampack.GetFrameId()

	def GetStreamType(self):
		return self.__streampack.GetFrameType()

	def GetCtrlCode(self):
		return self.__streampack.GetCtrlCode()


class SdkIpInfoSock(SdkSock):
	def	__init__(self,host,port):
		SdkSock.__init__(self,host,port)
		self.__ipinfopack = sdkproto.ipinfo.SdkIpInfo()
		return

	
	def GetIpInfo(self):
		# now first to pack for the info
		reqbuf = self.__ipinfopack.FormatQueryInfo(self.IncSeqId(),self.SessionId())
		rbuf = self.SendAndRecv(reqbuf,'GetIpInfo')
		return self.__ipinfopack.ParseQueryInfo(rbuf)



	def SetInfo(self,netinfo):
		reqbuf = self.__ipinfopack.FormatSetIpInfo(netinfo,self.SessionId(),self.IncSeqId())
		rbuf = self.SendAndRecv(reqbuf,'SetIpInfo')
		self.__ipinfopack.ParseSetIpInfoResp(rbuf)
		return

class SdkSysCtlSock(SdkSock):
	def	__init__(self,host,port):
		SdkSock.__init__(self,host,port)
		self.__sysctlpack = sdkproto.sysctl.SdkSysCtl()
		return


	def Reboot(self):
		reqbuf = self.__sysctlpack.RebootReq(self.SessionId(),self.IncSeqId())
		rbuf = self.SendAndRecv(reqbuf,'Reboot')
		self.__sysctlpack.RebootResp(rbuf)
		return

	def ResetHard(self):
		reqbuf = self.__sysctlpack.ResetHardReq(self.SessionId(),self.IncSeqId())
		rbuf = self.SendAndRecv(reqbuf,'Reboot')
		self.__sysctlpack.ResetHardResp(rbuf)
		return


class SdkVideoCfgSock(SdkSock):
	def	__init__(self,host,port):
		SdkSock.__init__(self,host,port)
		self.__sysvcpack = sdkproto.videocfg.SdkVideoCfg()
		return


	def GetVideoCfg(self):
		reqbuf = self.__sysvcpack.FormatQuery(self.SessionId(),self.IncSeqId())
		rbuf = self.SendAndRecv(reqbuf,'GetVideoCfg')		
		self.__sysvcpack.ParseQuery(rbuf)
		return self.__sysvcpack.VideoCfg()

	def SetVideoCfg(self,vcfg):
		reqbuf = self.__sysvcpack.FormatSetVideoCfg(vcfg,self.SessionId(),self.IncSeqId())
		rbuf = self.SendAndRecv(reqbuf,'SetVideoCfg')
		self.__sysvcpack.ParseSetVideoCfg(rbuf)
		return 


class SdkSysCfgSock(SdkSock):
	def	__init__(self,host,port):
		SdkSock.__init__(self,host,port)
		self.__sysscpack = sdkproto.syscfg.SdkSysCfg()
		return


	def GetSysCfg(self):
		reqbuf = self.__sysscpack.FormatQuery(self.SessionId(),self.IncSeqId())
		rbuf = self.SendAndRecv(reqbuf,'GetSysCfg')		
		return 	self.__sysscpack.ParseQuerySysCfgResp(rbuf)


	def SetSysCfg(self,scfg):
		reqbuf = self.__sysscpack.FormatSet(scfg,self.SessionId(),self.IncSeqId())
		rbuf = self.SendAndRecv(reqbuf,'SetSysCfg')
		self.__sysscpack.ParseSetSysCfgResp(rbuf)
		return 

class SdkPtzSock(SdkSock):
	def	__init__(self,host,port):
		SdkSock.__init__(self,host,port)
		self.__sysptzpack = sdkproto.ptz.SdkPtz()
		return


	def __HandleCmd(self,reqbuf,msg='PtzCmd'):
		rbuf = self.SendAndRecv(reqbuf,msg)
		self.__sysptzpack.PtzCtrlResp(rbuf)
		return
		


	def StopCmd(self):
		reqbuf = self.__sysptzpack.StopPtz(1,self.SessionId(),self.IncSeqId())
		self.__HandleCmd(reqbuf,'StopCmd')
		return

	def UpCmd(self,speed):
		reqbuf = self.__sysptzpack.UpPtz(1,speed,self.SessionId(),self.IncSeqId())
		self.__HandleCmd(reqbuf,'UpCmd')
		return

	def DownCmd(self,speed):
		reqbuf = self.__sysptzpack.DownPtz(1,speed,self.SessionId(),self.IncSeqId())
		self.__HandleCmd(reqbuf,'DownCmd')
		return
		
	def RightCmd(self,speed):
		reqbuf = self.__sysptzpack.RightPtz(1,speed,self.SessionId(),self.IncSeqId())
		self.__HandleCmd(reqbuf,'RightCmd')
		return

	def LeftCmd(self,speed):
		reqbuf = self.__sysptzpack.LeftPtz(1,speed,self.SessionId(),self.IncSeqId())
		self.__HandleCmd(reqbuf,'LeftCmd')
		return


	def UpRightCmd(self,speed):
		reqbuf = self.__sysptzpack.UpRightPtz(1,speed,self.SessionId(),self.IncSeqId())
		self.__HandleCmd(reqbuf,'UpRightCmd')
		return

	def UpLeftCmd(self,speed):
		reqbuf = self.__sysptzpack.UpLeftPtz(1,speed,self.SessionId(),self.IncSeqId())
		self.__HandleCmd(reqbuf,'UpLeftCmd')
		return

	def DownLeftCmd(self,speed):
		reqbuf = self.__sysptzpack.DownLeftPtz(1,speed,self.SessionId(),self.IncSeqId())
		self.__HandleCmd(reqbuf,'DownLeftCmd')
		return
		
	def DownRightCmd(self,speed):
		reqbuf = self.__sysptzpack.DownRightPtz(1,speed,self.SessionId(),self.IncSeqId())
		self.__HandleCmd(reqbuf,'DownRightCmd')
		return

	def SetPresetCmd(self,presetidx):
		reqbuf = self.__sysptzpack.SetPresetPtz(1,presetidx,self.SessionId(),self.IncSeqId())
		self.__HandleCmd(reqbuf,'SetPresetCmd')
		
	def GotoPresetCmd(self,presetidx):
		reqbuf = self.__sysptzpack.GotoPresetPtz(1,presetidx,self.SessionId(),self.IncSeqId())
		self.__HandleCmd(reqbuf,'GotoPresetCmd')

	def ClearPresetCmd(self,presetidx):
		reqbuf = self.__sysptzpack.ClearPresetPtz(1,presetidx,self.SessionId(),self.IncSeqId())
		self.__HandleCmd(reqbuf,'ClearPresetCmd')


	def GetPresetInfoCmd(self):
		reqbuf = self.__sysptzpack.PtzPresetGetReq(1,self.SessionId(),self.IncSeqId())
		rbuf = self.SendAndRecv(reqbuf,'GetPreset Info')
		return self.__sysptzpack.PtzPresetGetResp(rbuf)

	def SetPresetInfoCmd(self,ptzpreset):
		reqbuf = self.__sysptzpack.PtzPresetSetReq(ptzpreset,self.SessionId(),self.IncSeqId())
		rbuf = self.SendAndRecv(reqbuf,'SetPreset Info')
		return self.__sysptzpack.PtzPresetSetResp(rbuf)



class SdkShowCfgSock(SdkSock):
	def	__init__(self,host,port):
		SdkSock.__init__(self,host,port)
		self.__sysshowcfgpack = sdkproto.showcfg.SdkShowCfg()
		return


	def GetShowCfg(self):
		reqbuf = self.__sysshowcfgpack.FormGetReq(self.SessionId(),self.IncSeqId())
		rbuf = self.SendAndRecv(reqbuf,'GetShowCfgCmd')
		return self.__sysshowcfgpack.ParseGetRsp(rbuf)

	def SetShowCfg(self,showcfg):
		reqbuf = self.__sysshowcfgpack.FormSetReq(showcfg,self.SessionId(),self.IncSeqId())
		rbuf = self.SendAndRecv(reqbuf,'SetShowCfgCmd')
		return self.__sysshowcfgpack.ParseSetRsp(rbuf)

class SdkTimeSock(SdkSock):
	def	__init__(self,host,port):
		SdkSock.__init__(self,host,port)
		self.__systimepack = sdkproto.time.SdkTime()
		return


	def GetTimeCfg(self):
		reqbuf = self.__systimepack.FormGetTimeReq(self.SessionId(),self.IncSeqId())
		rbuf = self.SendAndRecv(reqbuf,'GetTimeCmd')
		return self.__systimepack.ParseGetTimeResp(rbuf)

	def SetTimeCfg(self,timetype,systime,ntpserver,timezone):
		reqbuf = self.__systimepack.FormSetTimeReq(timetype,systime,ntpserver,timezone,self.SessionId(),self.IncSeqId())
		rbuf = self.SendAndRecv(reqbuf,'SetTimeZoneCmd')
		return self.__systimepack.ParseSetTimeResp(rbuf)
		

	def SetTimeZoneCfg(self,timezone):
		reqbuf = self.__systimepack.FormSetTimeReq(None,None,None,timezone,self.SessionId(),self.IncSeqId())
		rbuf = self.SendAndRecv(reqbuf,'SetTimeZoneCmd')
		return self.__systimepack.ParseSetTimeResp(rbuf)

	def SetTimeTypeCfg(self,timetype):
		reqbuf = self.__systimepack.FormSetTimeReq(timetype,None,None,None,self.SessionId(),self.IncSeqId())
		rbuf = self.SendAndRecv(reqbuf,'SetTimeTypeCmd')
		return self.__systimepack.ParseSetTimeResp(rbuf)

	def SetNtpServerCfg(self,ntpserver):
		reqbuf = self.__systimepack.FormSetTimeReq(None,None,ntpserver,None,self.SessionId(),self.IncSeqId())
		rbuf = self.SendAndRecv(reqbuf,'NtpServerCmd')
		return self.__systimepack.ParseSetTimeResp(rbuf)


	def SetSysTimeCfg(self,systime):
		reqbuf = self.__systimepack.FormSetTimeReq(None,systime,None,None,self.SessionId(),self.IncSeqId())
		rbuf = self.SendAndRecv(reqbuf,'SysTimeCmd')
		return self.__systimepack.ParseSetTimeResp(rbuf)


class SdkImagineSock(SdkSock):
	def	__init__(self,host,port):
		SdkSock.__init__(self,host,port)
		self.__sysimgpack = sdkproto.imagine.SdkImagine()
		return


	def GetImagine(self):
		reqbuf = self.__sysimgpack.FormGetReq(self.SessionId(),self.IncSeqId())
		rbuf = self.SendAndRecv(reqbuf,'GetImagineCmd')
		return self.__sysimgpack.ParseGetRsp(rbuf)

	def SetImagine(self,imagine):
		reqbuf = self.__sysimgpack.FormSetReq(imagine,self.SessionId(),self.IncSeqId())
		rbuf = self.SendAndRecv(reqbuf,'SetImagineCmd')
		return self.__sysimgpack.ParseSetRsp(rbuf)
		
class SdkUserInfoSock(SdkIpInfoSock):
	def	__init__(self,host,port):
		SdkIpInfoSock.__init__(self,host,port)
		self.__userinfopack = sdkproto.userinfo.SdkUserInfo()
		return

	def __del__(self):
		SdkIpInfoSock.__del__(self)
		self.__userinfopack = None
		return

	def __GetPassKey(self,hwaddr):
		sa = hwaddr.split(':')
		passkey = ''
		for s in sa:
			n = int(s,16)
			passkey += chr(n)

		if len(passkey) < 8 :
			passkey += '\0' * (8-len(passkey))
		else:
			passkey = passkey[:8]
		return passkey
		


	def GetUserInfo(self):
		# now first to get the hw address
		ipinfos = self.GetIpInfo()
		hwaddr = ipinfos[0].HwAddr()
		passkey = self.__GetPassKey(hwaddr)
		# now we should format passkey
		reqbuf = self.__userinfopack.FormatUserInfoGetReq(self.SessionId(),self.IncSeqId())
		rbuf = self.SendAndRecv(reqbuf,'GetUserInfoReq')
		return self.__userinfopack.ParseUserInfoGetRsp(rbuf,passkey)

	def SetUserInfo(self,userinfo):
		reqbuf = self.__userinfopack.FormatUserInfoSetReq(userinfo,self.SessionId(),self.IncSeqId())
		rbuf = self.SendAndRecv(reqbuf,'SetUserInfoReq')
		return self.__userinfopack.ParseUserInfoSetRsp(rbuf)

	def DelUserInfo(self,userinfo):
		reqbuf = self.__userinfopack.FormatUserInfoDelReq(userinfo,self.SessionId(),self.IncSeqId())
		rbuf = self.SendAndRecv(reqbuf,'DelUserInfoReq')
		return self.__userinfopack.ParseUserInfoDelRsp(rbuf)

class SdkCapProtoSock(SdkSock):
	def	__init__(self,host,port):
		SdkSock.__init__(self,host,port)
		self.__capprotopack = sdkproto.capproto.SdkCapProto()
		return

	def __del__(self):
		SdkSock.__del__(self)
		self.__capprotopack = None
		return

	def GetCapProto(self,val=0):
		reqbuf = self.__capprotopack.FormatCapProtoGetReq(val,self.SessionId(),self.IncSeqId())
		#logging.info('reqbuf (%s)(%d)'%(repr(reqbuf),len(reqbuf)))
		rbuf = self.SendAndRecv(reqbuf,'GetCapProto')
		#logging.info('rbuf (%s)(%d)'%(repr(rbuf),len(rbuf)))
		return self.__capprotopack.ParseCapProtoGetRsp(rbuf)


class SdkNetworkPortSock(SdkSock):
	def	__init__(self,host,port):
		SdkSock.__init__(self,host,port)
		self.__netportpack = sdkproto.netport.SdkNetworkPort()
		return

	def __del__(self):
		SdkSock.__del__(self)
		self.__netportpack = None
		return

	def GetNetworkPort(self):
		reqbuf = self.__netportpack.FormatGetNetworkportReq(self.SessionId(),self.IncSeqId())
		rbuf = self.SendAndRecv(reqbuf,'GetNetworkPort')
		return self.__netportpack.ParseGetNetworkPortRsp(rbuf)

	def SetNetworkPort(self,netport):
		reqbuf = self.__netportpack.FormatSetNetworkPortReq(netport,self.SessionId(),self.IncSeqId())
		rbuf = self.SendAndRecv(reqbuf,'SetNetworkPort')
		return self.__netportpack.ParseSetNetworkPortRsp(rbuf)
		

class SdkWorkStateSock(SdkSock):
	def	__init__(self,host,port):
		SdkSock.__init__(self,host,port)
		self.__workstatepack = sdkproto.workstate.SdkWorkState()
		return

	def __del__(self):
		SdkSock.__del__(self)
		self.__workstatepack = None
		return

	def GetWorkState(self):
		reqbuf = self.__workstatepack.FormGetWorkStateReq(self.SessionId(),self.IncSeqId())
		rbuf = self.SendAndRecv(reqbuf,'GetWorkState')
		return self.__workstatepack.ParseGetWorkStateRsp(rbuf)


class SdkAdvImagineSock(SdkSock):
	def	__init__(self,host,port):
		SdkSock.__init__(self,host,port)
		self.__advimaginepack = sdkproto.advimagine.SdkAdvImage()
		return

	def __del__(self):
		SdkSock.__del__(self)
		self.__advimaginepack = None
		return

	def GetAdvImagine(self):
		reqbuf = self.__advimaginepack.FormGetReq(self.SessionId(),self.IncSeqId())
		rbuf = self.SendAndRecv(reqbuf,'GetAdvImagine')
		return self.__advimaginepack.ParseGetRsp(rbuf)

	def SetAdvImagine(self,advimagine):
		reqbuf = self.__advimaginepack.FormSetReq(advimagine,self.SessionId(),self.IncSeqId())
		rbuf = self.SendAndRecv(reqbuf,'SetNetworkPort')
		return self.__advimaginepack.ParseSetRsp(rbuf)


class SdkAudioDualSock(SdkSock):	
	def __init__(self,host,port):
		SdkSock.__init__(self,host,port)
		self.__audiooutpack = sdkproto.audiodual.AudioOutPack()
		self.__audioinpack = sdkproto.audiodual.AudioInPack()
		return

	def __del__(self):
		SdkSock.__del__(self)
		self.__audiooutpack = None
		self.__audioinpack = None
		return

	def SendData(self,framepack,data):
		if self.__audiooutpack is None:
			self.__audiooutpack = sdkproto.audiodual.AudioOutPack()
		reqbuf = self.__audiooutpack.PackStream(framepack,data)
		# now we should send buffer 
		self.SendBuf(self.PackGsspBuf(sdkproto.pack.GMIS_PROTOCOL_TYPE_MEDIA_DATA,reqbuf),'Send Data')
		return 

	def ReceiveData(self,timeout=10):
		gssphdr = self.RcvBufTimeout(sdkproto.pack.GMIS_BASE_LEN,timeout,'receive audio buffer header')
		fraglen , bodylen = self.UnPackGsspBuf(gssphdr)
		if fraglen > 0 :
			raise SdkSockRecvError('receive pack fraglen (%d)(%s)'%(fraglen,repr(gssphdr)))

		body = self.RcvBufTimeout(bodylen,timeout,'receive audio buffer')
		if self.__audioinpack is None:
			self.__audioinpack = sdkproto.audiodual.AudioInPack()
		return self.__audioinpack.UnPackStream(body)

	def GetReceiveHdr(self):
		if self.__audioinpack is None:
			raise SdkSockInvalidParam('not receive data yet')
		return self.__audioinpack.FramePack()

	def GetReceiveData(self):
		if self.__audioinpack is None:
			raise SdkSockInvalidParam('not receive data yet')
		return self.__audioinpack.FrameData()

	def StartAudioDual(self,starttalkreq):
		if not isinstance(starttalkreq,sdkproto.audiodual.StartTalkRequest):
			raise SdkSockInvalidParam('starttalkreq is not sdkproto.audiodual.StartTalkRequest')
		logging.info('\n')
		# now we form the pack
		reqbuf = starttalkreq.FormatBuf()
		sbuf = self.PackGsspBuf(sdkproto.pack.GMIS_PROTOCOL_TYPE_MEDIA_CTRL,reqbuf)
		self.SendBuf(sbuf,'StartAudioDual')
		gssphdr = self.RcvBuf(sdkproto.pack.GMIS_BASE_LEN,'Wait StartAudioDual')
		logging.info('\n')
		fraglen,bodylen = self.UnPackGsspBuf(gssphdr)
		if fraglen != 0:
			raise SdkSockInvalidParam('receive StartAudioDual len(%d) != 0'%(fraglen))
		rbuf = self.RcvBufTimeout(bodylen,3.0,'StartAudioDual ok')
		# now we should do the stream pack job
		logging.info('\n')
		starttalkresp = sdkproto.audiodual.StartTalkResponse()
		logging.info('\n')
		starttalkresp.ParseBuf(rbuf)
		logging.info('\n')
		return starttalkresp
	
