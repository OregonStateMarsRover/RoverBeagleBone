class RoverPacket:
	start = bytearray([0])
	def __init__(self, addr, content):
		self.addr = bytearray([addr])
		self.content = bytearray(content)
		self.compute_full_message()

	def compute_full_message(self):
		self.length = bytearray([len(self.content)+1]) #length of everything after the length byte
		self.message = self.start + self.addr + self.length + self.content
		self.checksum = bytearray([0xFF ^ (sum(self.message) & 0xFF)])  #bitwise complement of the sum of the other bytes, clipped to a single byte
		self.full_message = self.message + self.checksum

	def append(self, bytes):
		self.content.append(bytes)
		self.compute_full_message()

	def msg(self):
		return self.full_message

	def __str__(self):
		return str(list(self.full_message))

	def __repr__(self):
		return repr(self.full_message)

	def __len__(self):
		return len(self.full_message)

	def __hex__(self):
		return "0x" + "".join(["%.2x"%i for i in self.full_message])

	def __add__(self, other):
		if type(other) != type(self):
			raise TypeError
		return RoverPacket(self.addr[0], self.content + other.content)

class BogiePacket(RoverPacket):
	def __init__(self, addr, speed, turning):
		content = [speed, turning]
		RoverPacket.__init__(self, addr, content)