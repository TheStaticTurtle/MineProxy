import common.types.common
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class JoinGame(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		return {
			'entity_id': common.types.common.Integer,
			'gamemode': common.types.common.UnsignedByte,
			'dimension': common.types.common.Byte,
			'difficulty': common.types.common.UnsignedByte,
			'max_players': common.types.common.UnsignedByte,
			'level_type': common.types.common.String,
			'reduced_debug_info': common.types.common.Boolean,
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

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x23
		if self.context.protocol_version == 47:
			return 0x01
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")
