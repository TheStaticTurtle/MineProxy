from ..serverbound import Handshake
from ..SimplePacketInterceptor import SimplePacketInterceptor

class HandshakeInterceptor(SimplePacketInterceptor):
	NAME = "HandshakeInterceptor"
	packet_class = Handshake

	def __init__(self, client_addr, server_addr):
		super().__init__()
		self.client_addr = client_addr
		self.server_addr = server_addr

	def _intercept(self, packet: Handshake):
		print(f"[HANDSHAKE] Intercepted {packet} spoofing sever ip to: {self.server_addr[0]}")
		packet.server_address =  packet.server_address = self.server_addr[0]

		return packet