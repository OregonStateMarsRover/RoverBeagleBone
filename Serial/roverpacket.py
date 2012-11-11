class RoverPacket:
	start_byte = 0xCA
	escape_byte = 0x5C
	null_byte = 0x00
	max_byte = 0xFF
	escaped_bytes = {start_byte : 2, escape_byte : 3, null_byte : 4, max_byte : 5}
	def __init__(self, addr, content):
		self.addr = addr
		self.content = bytearray(content)
		self.compute_full_message()

	def compute_full_message(self):
		stuffed_content = bytearray()
		for byte in self.content:
			if byte in self.escaped_bytes.keys():
				stuffed_content.append(escape_byte)
				stuffed_content.append(escaped_bytes[byte])
			else:
				stuffed_content.append(byte)
		self.length = len(stuffed_content)+1 #length of everything after the length byte
		self.message = bytearray([self.start_byte, self.addr, self.length]) + stuffed_content
		self.checksum = 0xFF ^ (sum(self.message) & 0xFF)  #bitwise complement of the sum of the other bytes, clipped to a single byte
		self.full_message = self.message + bytearray([self.checksum])

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
		return RoverPacket(self.addr, self.content + other.content)

class BogiePacket(RoverPacket):
	def __init__(self, addr, speed, turning):
		content = [speed, turning]
		RoverPacket.__init__(self, addr, content)