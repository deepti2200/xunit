#! python

'''
this is the DES python file
'''

import logging

class DES:
	# Permutation and translation tables for DES
	__pc1 = [56, 48, 40, 32, 24, 16,  8,
		  0, 57, 49, 41, 33, 25, 17,
		  9,  1, 58, 50, 42, 34, 26,
		 18, 10,  2, 59, 51, 43, 35,
		 62, 54, 46, 38, 30, 22, 14,
		  6, 61, 53, 45, 37, 29, 21,
		 13,  5, 60, 52, 44, 36, 28,
		 20, 12,  4, 27, 19, 11,  3
	]

	# number left rotations of pc1
	MOVE_TIMES = [
		1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1
	]

	# permuted choice key (table 2)
	__pc2 = [
		13, 16, 10, 23,  0,  4,
		 2, 27, 14,  5, 20,  9,
		22, 18, 11,  3, 25,  7,
		15,  6, 26, 19, 12,  1,
		40, 51, 30, 36, 46, 54,
		29, 39, 50, 44, 32, 46,
		43, 48, 38, 55, 33, 52,
		45, 41, 49, 35, 28, 31
	]

	# initial permutation IP
	__ip = [57, 49, 41, 33, 25, 17, 9,  1,
		59, 51, 43, 35, 27, 19, 11, 3,
		61, 53, 45, 37, 29, 21, 13, 5,
		63, 55, 47, 39, 31, 23, 15, 7,
		56, 48, 40, 32, 24, 16, 8,  0,
		58, 50, 42, 34, 26, 18, 10, 2,
		60, 52, 44, 36, 28, 20, 12, 4,
		62, 54, 46, 38, 30, 22, 14, 6
	]

	# Expansion table for turning 32 bit blocks into 48 bits
	__expansion_table = [
		31,  0,  1,  2,  3,  4,
		 3,  4,  5,  6,  7,  8,
		 7,  8,  9, 10, 11, 12,
		11, 12, 13, 14, 15, 16,
		15, 16, 17, 18, 19, 20,
		19, 20, 21, 22, 23, 24,
		23, 24, 25, 26, 27, 28,
		27, 28, 29, 30, 31,  0
	]

	# The (in)famous S-boxes
	__sbox = [
		# S1
		[
			[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
			[0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
			[4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
			[15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
		],

		# S2
		[
			[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
			[3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
			[0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
			[13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
		],

		# S3
		[
			[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
			[13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
			[13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
			[1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
		],

		# S4
		[
			[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
			[13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
			[10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
			[3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
		],

		# S5
		[
			[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
			[14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
			[4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
			[11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
		],

		# S6
		[
			[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
			[10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
			[9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
			[4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
		],

		# S7
		[
			[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
			[13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
			[1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
			[6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
		],

		# S8
		[
			[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
			[1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
			[7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
			[2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
		]
	]


	# 32-bit permutation function P used on the output of the S-boxes
	__p = [
		15, 6, 19, 20, 28, 11,
		27, 16, 0, 14, 22, 25,
		4, 17, 30, 9, 1, 7,
		23,13, 31, 26, 2, 8,
		18, 12, 29, 5, 21, 10,
		3, 24
	]

	# final permutation IP^-1
	IP_1_Table = [
		39,  7, 47, 15, 55, 23, 63, 31,
		38,  6, 46, 14, 54, 22, 62, 30,
		37,  5, 45, 13, 53, 21, 61, 29,
		36,  4, 44, 12, 52, 20, 60, 28,
		35,  3, 43, 11, 51, 19, 59, 27,
		34,  2, 42, 10, 50, 18, 58, 26,
		33,  1, 41,  9, 49, 17, 57, 25,
		32,  0, 40,  8, 48, 16, 56, 24
	]


	def __DES_PC1_Transform(self,keybits):
		cnt = 0
		tempbts = []
		while cnt < 56:
			t = keybits[self.__pc1[cnt]]
			tempbts.append(t)
			cnt +=1
		return tempbts

	def __DES_ROL(self,tempbts,times):
		newtempbits = tempbts
		temp = []
		# first copy times
		i = 0
		while i < times:
			temp.append(newtempbits[i])
			i += 1

		i = 0
		while i < (times ):
			temp.append(newtempbits[i+28])
			i += 1

		# now change the 28 bytes
		i = 0
		while i < (28 - times):
			newtempbits[i] = newtempbits[i+times]
			i += 1

		i = 0
		while i < times:
			newtempbits[28-times+i]=temp[i]
			i += 1


		# now later shift
		i = 0
		while i < (28-times):
			newtempbits[28+i] = newtempbits[28+i+times]
			i +=1

		i = 0
		while i < times:
			newtempbits[56-times+i] = temp[times+i]
			i+=1
		self.__tempbts = newtempbits
		return newtempbits
			

	def __DES_PC2_Transform(self,key):
		cnt = 0
		assert(len(key) == 56)
		newtempbts = []
		while cnt < 48:
			t = key[self.__pc2[cnt]]
			newtempbts.append(t)
			cnt += 1
		return newtempbts
		

	def __DES_MakeSubKeys(self,keybits):
		tempbts = self.__DES_PC1_Transform(keybits)
		self.__tempbts = tempbts
		self.__subkeys = []
		cnt = 0
		while cnt < 16:
			tempbts = self.__DES_ROL(tempbts,self.MOVE_TIMES[cnt])
			subkeys = self.__DES_PC2_Transform(tempbts)
			self.__subkeys.append(subkeys)
			cnt += 1
		return self.__subkeys
		

	def __init__(self,key):
		if len(key) != 8:
			raise Exception('key must 8 bytes length')
		keybits = self.__Char8ToBit64(key)
		self.__DES_MakeSubKeys(keybits)
		return

	def __del__(self):
		self.__subkeys = []
		return

	def __ByteToBit(self,inchar):
		dto = []
		cnt = 0
		cchar = ord(inchar)
		while cnt < 8:
			if cchar & 1:
				dto.append(1)
			else:
				dto.append(0)
			cnt += 1
			cchar = cchar >> 1
		#logging.info('char[%d] %s'%(ord(inchar),repr(dto)))
		return dto

	def __Char8ToBit64(self,datain):
		assert(len(datain) == 8)
		cnt = 0
		dataout = []
		while cnt < 8 :
			dto = self.__ByteToBit(datain[cnt])
			dataout.extend(dto)
			cnt += 1
		return dataout

	def __DES_IP_Transform(self,datainbits):
		assert(len(datainbits) == 64)
		rdatabits = []		
		cnt = 0
		while cnt < 64:
			t = datainbits[self.__ip[cnt]]
			rdatabits.append(t)
			cnt += 1
		return rdatabits

	def __DES_E_Transform(self,datain):
		dataout = []
		cnt = 0
		while cnt < 48:
			t = datain[self.__expansion_table[cnt]]
			dataout.append(t)
			cnt += 1
		return dataout

	def __DES_XOR(self,datain,subkey,times):
		dataout = []
		cnt = 0
		while cnt < times:
			t = datain[cnt]
			t = t ^ subkey[cnt]
			dataout.append(t)
			cnt += 1
		return dataout

	def __DES_SBOX(self,datain):
		cnt = 0
		cur1= 0
		cur2 = 0
		dataout = datain
		while cnt < 8:
			cur1 = cnt * 6
			cur2 = cnt << 2
			line = (dataout[cur1]<<1)  + dataout[cur1+5]
			row = (dataout[cur1+1]<<3) + (dataout[cur1+2]<<2) + (dataout[cur1+3]<<1) + dataout[cur1+4]
			output = self.__sbox[cnt][line][row]
			dataout[cur2] = (output & 0x8) >> 3
			dataout[cur2+1] = (output & 0x4) >> 2
			dataout[cur2+2] = (output & 0x2) >> 1
			dataout[cur2+3] = (output & 0x1)
			cnt += 1
		return dataout

	def __DES_P_Transform(self,datain):
		assert(len(datain) >= 32)
		pend = datain[32:]
		dataout = []
		cnt = 0
		while cnt < 32:
			t = datain[self.__p[cnt]]
			dataout.append(t)
			cnt += 1
		dataout.extend(pend)
		return dataout

	def __DES_Swap(self,L,R):
		outL=[]
		outR=[]
		outL = R
		outR = L
		return outL,outR

	def __DES_IP_1_Transform(self,datain):
		assert(len(datain) >= 64)
		dataout = []
		cnt = 0
		while cnt < 64:
			t = datain[self.IP_1_Table[cnt]]
			dataout.append(t)
			cnt += 1

		return dataout

	def __BitToByte(self,bits):
		assert(len(bits) == 8)
		cnt = 0
		c = 0
		while cnt < 8:
			if (bits[cnt]):
				c += (1 << cnt)
			cnt += 1
		return chr(c)

	def __Bit64ToChar8(self,databitsin):
		dataoutchar = ''
		cnt = 0
		while cnt < 8:
			datapartbits = databitsin[8*cnt:8*(cnt+1)]
			c = self.__BitToByte(datapartbits)
			cnt += 1
			dataoutchar += c
		return dataoutchar
			

	def DES_EncryptBlock(self,datain):
		if len(datain) != 8:
			raise Exception('datain must be 8 bytes')
		blockbits = self.__Char8ToBit64(datain)
		#logging.info('blockbits\t%s'%(repr(blockbits)))
		blockbits = self.__DES_IP_Transform(blockbits)
		#logging.info('IP_Transform\t%s'%(repr(blockbits)))

		cnt = 0
		while cnt < 16:
			R = blockbits[32:]
			L = blockbits[:32]
			#logging.info('blockbits\t%s'%(repr(blockbits)))
			#logging.info('Left\t%s'%(repr(L)))
			#logging.info('Right\t%s'%(repr(R)))
			R = self.__DES_E_Transform(R)
			#logging.info('Right\t%s'%(repr(R)))
			R = self.__DES_XOR(R,self.__subkeys[cnt],48)
			#logging.info('Right\t%s'%(repr(R)))
			R = self.__DES_SBOX(R)
			#logging.info('Right\t%s'%(repr(R)))
			R = self.__DES_P_Transform(R)
			#logging.info('Right\t%s'%(repr(R)))
			L = self.__DES_XOR(L,R,32)
			#logging.info('Left\t%s'%(repr(L)))
			tempR = blockbits[32:]
			blockbits = L + tempR
			#logging.info('Before Swap\t%s'%(repr(blockbits)))
			if cnt != 15:
				tempR = blockbits[32:]
				blockbits = L+tempR
				L,tempR = self.__DES_Swap(L,tempR)
				blockbits = L + tempR
			cnt += 1
		blockbits = self.__DES_IP_1_Transform(blockbits)
		#logging.info('blockbits final\t%s'%(repr(blockbits)))
		dataout =  self.__Bit64ToChar8(blockbits)		
		da = []
		for c in dataout:
			da.append(ord(c))
		#logging.info('Encryption\t%s'%(repr(da)))
		return dataout

	def DES_DecryptBlock(self,datain):
		if len(datain) != 8:
			raise Exception('datain must be 8 bytes')
		blockbits = self.__Char8ToBit64(datain)
		blockbits = self.__DES_IP_Transform(blockbits)
		cnt = 15
		while cnt >= 0:
			L = blockbits[:32]
			R = blockbits[32:]
			R = self.__DES_E_Transform(R)
			R = self.__DES_XOR(R,self.__subkeys[cnt],48)
			R = self.__DES_SBOX(R)
			R = self.__DES_P_Transform(R)

			L = self.__DES_XOR(L,R,32)
			blockbits = L + blockbits[32:]
			if cnt != 0:
				tempR = blockbits[32:]
				L,tempR = self.__DES_Swap(L,tempR)
				blockbits = L + tempR
			cnt -= 1
		blockbits = self.__DES_IP_1_Transform(blockbits)
		return self.__Bit64ToChar8(blockbits)

	def Encrypt(self,datain):
		tlen = len(datain)
		atlen = int((tlen+7)/8)*8
		dataalignin = datain
		if atlen > tlen:
			dataalignin += '\0' * (atlen - tlen)

		encsize = 0
		dataout = ''
		while encsize < atlen:
			curin = dataalignin[encsize:encsize+8]
			curout = self.DES_EncryptBlock(curin)
			dataout += curout
			encsize += 8
		return dataout

	def Decrypt(self,datain):
		if (len(datain) % 8) != 0:
			raise Exception('decrypt datain must be 8 bytes align')
		decsize = 0
		dataout = ''
		while decsize < len(datain):
			curin = datain[decsize:decsize+8]
			curout = self.DES_DecryptBlock(curin)
			dataout += curout
			decsize += 8
		return dataout

if __name__ == '__main__':
	import sys
	if len(sys.argv[1:]) < 1:
		sys.stderr.write('%s string key\n'%(__file__))
		sys.exit(3)
	try:
		inbuf = str(eval(sys.argv[1]))
	except:
		inbuf = str(sys.argv[1])
	enckey = '\x00\x00\x00\x00\x00\x00\x00\x00'
	if len(sys.argv[1:]) >= 2:
		try:
			enckey = str(eval(sys.argv[2]))
		except:
			enckey = str(sys.argv[2])
	if len(enckey) < 8:
		enckey += '\0' * (8 - len(enckey))
	if len(enckey) > 8:
		enckey = enckey[:8]

	
	#logging.basicConfig(level=logging.INFO,format="%(levelname)-8s [%(filename)-10s:%(funcName)-20s:%(lineno)-5s] %(message)s")
	#logging.basicConfig(level=logging.INFO,format="%(message)s")
	desk = DES(enckey)
	ilen = len(inbuf)
	ailen = int((ilen + 7)/8) * 8
	if ailen != ilen:
		inbuf += '\0' * (ailen - ilen)	
	encbuf = desk.Encrypt(inbuf)
	outbuf = desk.Decrypt(encbuf)
	assert(outbuf == inbuf)
	sys.stdout.write('%s key %s\n'%(repr(inbuf),repr(enckey)))
	sys.stdout.write('encbuf\t[')
	i = 0
	while i < len(encbuf) :
		c = encbuf[i]
		if i == 0:
			sys.stdout.write('0x%02x,'%(ord(c)))
		elif i == (len(encbuf) - 1):
			sys.stdout.write(' 0x%02x'%(ord(c)))
		else:
			sys.stdout.write(' 0x%02x,'%(ord(c)))
		i += 1
	sys.stdout.write(']\n')
	sys.stdout.write('decoutbuf\t[')
	i = 0
	while i < len(outbuf) :
		c = outbuf[i]
		if i == 0:
			sys.stdout.write('0x%02x,'%(ord(c)))
		elif i == (len(outbuf) - 1):
			sys.stdout.write(' 0x%02x'%(ord(c)))
		else:
			sys.stdout.write(' 0x%02x,'%(ord(c)))
		i += 1
	sys.stdout.write(']\n')
