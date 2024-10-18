import binascii, math
Encoding = ' ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnop1234567890~!@#$%^&*()`[{}]:;"\'<>,.?/|\\=+-_'
print(len(Encoding))
def Listify(In):
	out = []
	for i in str(In):
		out.append(str(i))
	return out
def DeListify(In):
	out = ''
	for i in In:
		out += str(i)
	return out
def PassHash(Key, Key2, Len, Index):
	Out = "00000000"
	for i in Key:
		w = 0
		Out = Listify(Out)
		Out2 = []
		Binary = str(bin(Encoding.index(i) % 512)[2:])
		for i in range(8 - len(Binary)):
			Binary = "0" + Binary
		for i in Binary:
			if i == "1":
				if Out[w] == "0":
					Out2.append("1")
				else:
					Out2.append("0")
		Out = Out2
	i = (((math.ceil(Index / Len) * Encoding.index(Key[Index % len(Key)])) % len(Key2)) + Encoding.index(Key[(len(Key2) * Len) % len(Key)]) % 512)
	w = 0
	Binary = str(bin(i)[2:])
	for i in range(8 - len(Binary)):
		Binary = "0" + Binary
	for i in Binary:
		if i == "1":
			if Out[w] == "0":
				Out[w] = "1"
			else:
				Out[w] = "0"
	return DeListify(Out)
def Encrypt(Data, Key, Key2,Method=1):
	y = 0
	conPart = 0
	x = ''
	out = ''
	keyPart = 0
	for i in Data:
		y += 1
		x += str(i)
		if y == 8:
			if Method == 0:
				#Could I have some salt with my fries
				newByte = int(x, 2)
				try:
					newByte = newByte + Encoding.index(Key[keyPart])
				except:
					keyPart = 0
					newByte = newByte + Encoding.index(Key[keyPart])
				try:
					newByte = newByte + Encoding.index(Key2[conPart])
				except:
					conPart = 0
					newByte = newByte + Encoding.index(Key2[conPart])
				newByte = newByte % 256
				#Fuck it up
				binary = bin(newByte)[2:]
				binary = str(binary)
				if len(binary) < 8:
					for i in range(8 - len(binary)):
						binary = '0' + binary
				place = 0
				binary = Listify(binary)
				binary2 = []
				for i in binary:
					if place % 2 == 1:
						if i == '0':
							binary2.append('1')
						else:
							binary2.append('0')
					else:
						binary2.append(i)
					place += 1
				binary = binary2
				place = 0
				binary2 = []
				if Encoding.index(Key[keyPart]) % 2 == 1:
					for i in binary:
						if i == '0':
							binary2.append('1')
						else:
							binary2.append('0')
						place += 1
					binary = binary2
				binary = DeListify(binary)
				out += binary
				binary = 0
				newByte = 0
				place = 0
			keyPart += 1
			conPart += 1
			x = ''
			y = 0
	return out
def Decrypt(Data, Key, Key2, Method=0):
	y = 0
	conPart = 0
	out = ''
	binary = ''
	keyPart = 0
	for i in Data:
		binary += i
		y += 1
		if y == 8:
			if Method == 0:
				dummydata = 200
				try:
					dummydata -= Encoding.index(Key[keyPart])
				except:
					keyPart = 0
					dummydata -= Encoding.index(Key[keyPart])
				try:
					dummydata -= Encoding.index(Key2[conPart])
				except:
					conPart = 0
					dummydata -= Encoding.index(Key2[conPart])
				place = 0
				binary = Listify(binary)
				binary2 = []
				if len(Key) - 1 < keyPart:
					print('the fuck?')
					keyPart = 0
				try:
					Encoding.index(Key[keyPart])
				except:
					keyPart = 0
				if Encoding.index(Key[keyPart]) % 2 == 1:
					for i in binary:
						if str(i) == '0':
							binary2.append('1')
						else:
							binary2.append('0')
						place += 1
					binary = binary2
				place = 0
				binary2 = []
				for i in binary:
					if place % 2 == 1:
						if i == '0':
							binary2.append('1')
						else:
							binary2.append('0')
					else:
						binary2.append(i)
					place += 1
				binary = binary2
				binary = DeListify(binary)
				binary = int(binary, 2)
				try:
					binary -= Encoding.index(Key[keyPart])
				except:
					keyPart = 0
					binary -= Encoding.index(Key[keyPart])
				try:
					binary -= Encoding.index(Key2[conPart])
				except:
					conPart = 0
					binary -= Encoding.index(Key2[conPart])
				while binary < 0:
						binary += 256
				binary = bin(binary)[2:]
				binary = str(binary)
				if len(binary) < 8:
					for i in range(0, 8 - len(binary)):
						binary = '0' + binary
				out += binary
				binary = ''
				keyPart += 1
				conPart += 1
			y = 0
	return out
def ReadBin(file):
	hexcode = binascii.hexlify((file.read())).decode()
	y = 0
	x = ''
	out = []
	for i in hexcode:
		x += str(i)
		if y == 1:
			y = -1
			out.append(str(x))
			x = ''
		y += 1
	place = 0
	tofinish = 0
	finish = ''
	for i in out:
		tofinish = bin(int(str(i), 16))[2:]
		if len(tofinish) < 8:
			for i in range(0, 8 - len(tofinish)):
				tofinish = '0' + tofinish
		finish += tofinish
	return finish
def WriteBin(file, content):
	byteArray = bytearray(int(content, 2).to_bytes((len(content) + 7) // 8, byteorder='big'))
	bytesOut = bytes(byteArray)
	if file == None:
		file = open('Output.txt', 'wb')
	file.write(bytesOut)
print(PassHash("Ok", "Lol", 25, 12))