#! python

import xunit.utils.exptel
import xunit.config
import logging

class CfgExpTel:
    def __init__(self):
        self.__tel = None
        return


    def Login(self):
        utcfg = xunit.config.XUnitConfig()
        host = utcfg.GetValue('.telnet','host','')
        port = utcfg.GetValue('.telnet','port','23')
        user = utcfg.GetValue('.telnet','username',None)
        password = utcfg.GetValue('.telnet','password',None)
        loginnote = utcfg.GetValue('.telnet','loginnote','login:')
        passwordnote = utcfg.GetValue('.telnet','passwordnote','assword:')
        cmdnote = utcfg.GetValue('.telnet','cmdnote','# ')
        timeout = utcfg.GetValue('.telnet','timeout','5')
        port = int(port)
        timeout = int(timeout)
        self.__stream = None
        logclass = utcfg.GetValue('.telnet','logclass','none')
        if logclass == 'stdout' :
            logging.info('stdout')
            self.__stream = sys.stdout
        elif logclass == 'stderr':
            logging.info('stderr')
            self.__stream = sys.stderr
        elif logclass.lower() == 'none':
            self.__stream = None
        else:
            self.__stream = ClassLogger(logclass)
        #logging.info('host %s port %s user %s password %s timeout %d loginnote %s passnote %s cmdnote %s\n'%(host,port,user,password,timeout,loginnote,passwordnote,cmdnote))
        self.__tel = xunit.utils.exptel.XUnitTelnet(host,port,user,password,self.__stream,timeout,loginnote,passwordnote,cmdnote)
        return

    def Logout(self):
        if self.__tel:
            del self.__tel
            self.__tel = None
        self.__stream = None
        return

    
    def Execute(self,cmd):
        return self.__tel.Execute(cmd)

    def __del__(self):
        self.Logout()
        return
    def WriteLine(self,line):
        return self.__tel.Writeln(line)

    def ReadImmediate(self):
        return self.__tel.ReadImmediate()
