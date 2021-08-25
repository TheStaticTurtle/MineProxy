from common.types import McPacketType, McState
from networking.McPackets import SimplePacket
from common import types

class JoinGame(SimplePacket.Packet):
	ID = 0x01
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'entity_id': types.Integer,
		'gamemode': types.UnsignedByte,
		'dimension': types.Byte,
		'difficulty': types.UnsignedByte,
		'max_players': types.UnsignedByte,
		'level_type': types.String,
		'reduced_debug_info': types.Boolean,
	}

	def __init__(self, context):
		super().__init__(context)
		self.entity_id = None
		self.gamemode = None
		self.dimension = None
		self.difficulty = None
		self.max_players = None
		self.level_type = None
		self.reduced_debug_info = None
