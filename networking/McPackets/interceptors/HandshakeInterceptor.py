from common.context import Context
from ..serverbound.handshaking import Handshake
from ..SimplePacketInterceptor import SimplePacketInterceptor

class HandshakeInterceptor(SimplePacketInterceptor):
	NAME = "HandshakeInterceptor"
	packet_class = Handshake

	def __init__(self, context: Context, client_addr, server_addr):
		super().__init__(context)
		self.client_addr = client_addr
		self.server_addr = server_addr

	def _intercept(self, packet: Handshake):
		self.log.info(f"Intercepted {packet}, spoofing original sever ip to: {self.server_addr[0]}")
		packet.server_address =  packet.server_address = self.server_addr[0]

		return packet