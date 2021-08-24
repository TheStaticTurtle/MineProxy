import io
import json
from networking.McPackets import SimplePacket


class LoginDisconnect(SimplePacket.Packet):
	def __init__(self, id, data_lenght, data):
		SimplePacket.Packet.__init__(self, id, data_lenght, data)
		self.data = {}

	def __repr__(self):
		return f"<ClientBound/LoginDisconnect {json.dumps(self.data)}>"

	@staticmethod
	def from_basic_packet(packet, protocol_version):
		stream = io.BytesIO(packet.data)
		new_packet = LoginDisconnect(packet.id, packet.data_lenght, packet.data)
		# TODO: Parse the Chat type
		return new_packet
