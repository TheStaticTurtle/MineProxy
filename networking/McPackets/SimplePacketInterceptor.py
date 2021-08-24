import logging

from . import SimplePacket
from common.context import Context

class SimplePacketInterceptor:
	NAME = "SimplePacketInterceptor"
	packet_class = None

	def __init__(self, context: Context):
		self.log = logging.getLogger(self.NAME)
		self.context = context

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
