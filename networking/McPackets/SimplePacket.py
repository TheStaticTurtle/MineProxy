from common import types


class Packet:
	def __init__(self, id, data_lenght, data):
		self.id = id
		self.data_lenght = data_lenght
		self.data = data

	@staticmethod
	def is_simple_packet(obj):
		return type(obj) == Packet

	@staticmethod
	def from_basic_packet(packet, protocol_version):
		return packet

	def craft(self, protocol_version):
		if self.id is None or self.data is None:
			raise NotImplementedError("Can't craft packet")
		return types.VarInt.write(self.id) + self.data

	def __str__(self):
		return repr(self)

	def __repr__(self):
		return f"<Packet id=0x{self.id:02x} length={self.data_lenght}>"
