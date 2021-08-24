import io
from networking.McPackets import SimplePacket
from common import types


class PlayJoinGame(SimplePacket.Packet):
	def __init__(self, id, data_lenght, data):
		SimplePacket.Packet.__init__(self, id, data_lenght, data)
		self.entity_id = None
		self.gamemode = None
		self.dimension = None
		self.difficulty = None
		self.max_players = None
		self.level_type = None
		self.reduced_debug_info = None

	def __repr__(self):
		return f"<ClientBound/PlayJoinGame entity_id={self.entity_id} gamemode={self.gamemode} dimension={self.dimension} difficulty={self.difficulty} max_players={self.max_players} level_type={self.level_type} reduced_debug_info={self.reduced_debug_info}>"

	@staticmethod
	def from_basic_packet(packet, protocol_version):
		stream = io.BytesIO(packet.data)

		new_packet = PlayJoinGame(packet.id, packet.data_lenght, packet.data)
		new_packet.entity_id,_ = types.Integer.read(stream)
		new_packet.gamemode,_ = types.UnsignedByte.read(stream)
		new_packet.dimension,_ = types.Byte.read(stream)
		new_packet.difficulty,_ = types.UnsignedByte.read(stream)
		new_packet.max_players,_ = types.UnsignedByte.read(stream)
		new_packet.level_type,_ = types.String.read(stream)
		new_packet.reduced_debug_info,_ = types.Boolean.read(stream)
		return new_packet
