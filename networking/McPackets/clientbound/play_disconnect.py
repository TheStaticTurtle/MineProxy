import io
from networking.McPackets import SimplePacket
from common import types


class PlayDisconnect(SimplePacket.Packet):
	def __init__(self, id, data_lenght, data):
		SimplePacket.Packet.__init__(self, id, data_lenght, data)
		self.reason = None

	def __repr__(self):
		return f"<ClientBound/Disconnect reason={self.reason}>"

	@staticmethod
	def from_basic_packet(packet, protocol_version):
		stream = io.BytesIO(packet.data)

		new_packet = PlayDisconnect(packet.id, packet.data_lenght, packet.data)
		new_packet.reason ,_ = types.String.read(stream)
		return new_packet
