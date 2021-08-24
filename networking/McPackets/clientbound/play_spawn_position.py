import io
from networking.McPackets import SimplePacket
from common import types


class PlaySpawnPosition(SimplePacket.Packet):
	def __init__(self, id, data_lenght, data):
		SimplePacket.Packet.__init__(self, id, data_lenght, data)
		self.location = None

	def __repr__(self):
		return f"<ClientBound/PlaySpawnPosition location={self.location}>"

	@staticmethod
	def from_basic_packet(packet, protocol_version):
		stream = io.BytesIO(packet.data)

		new_packet = PlaySpawnPosition(packet.id, packet.data_lenght, packet.data)
		new_packet.location ,_ = types.Location.read(stream)
		return new_packet
