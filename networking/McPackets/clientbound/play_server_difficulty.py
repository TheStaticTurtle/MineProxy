import io
from networking.McPackets import SimplePacket
from common import types


class PlayServerDifficulty(SimplePacket.Packet):
	def __init__(self, id, data_lenght, data):
		SimplePacket.Packet.__init__(self, id, data_lenght, data)
		self.difficulty = None

	def __repr__(self):
		return f"<ClientBound/PlayServerDifficulty difficulty={self.difficulty}>"

	@staticmethod
	def from_basic_packet(packet, protocol_version):
		stream = io.BytesIO(packet.data)

		new_packet = PlayServerDifficulty(packet.id, packet.data_lenght, packet.data)
		new_packet.difficulty,_ = types.UnsignedByte.read(stream)
		return new_packet
