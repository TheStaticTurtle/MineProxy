from . import SimplePacket

class SimplePacketInterceptor:
	NAME = "SimplePacketInterceptor"
	packet_class = None

	def __init__(self):
		self.compression_threshold = None
		self.protocol_version = None

	def set_compression_threshold(self, value):
		self.compression_threshold = value

	def set_protocol_version(self, value):
		self.protocol_version = value

	def intercept(self, packet: SimplePacket):
		"""Intercept function
		Returns a tuple of:
			- None, orginal or a modified packet
		"""
		if isinstance(packet, self.packet_class):
			return self._intercept(packet)
		if self.packet_class is None:
			return self._intercept(packet)

	def _intercept(self, packet: SimplePacket):
		return packet


	def __str__(self):
		return repr(self)

	def __repr__(self):
		return f"<{self.NAME} intercept: {self.packet_class}>"
