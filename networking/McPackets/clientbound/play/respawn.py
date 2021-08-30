import common.types.common
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class Respawn(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		return {
			'dimension': common.types.common.Integer,
			'difficulty': common.types.common.UnsignedByte,
			'gamemode': common.types.common.UnsignedByte,
			'level_type': common.types.common.String,
		}

	def __init__(self, context):
		super().__init__(context)
		self.dimension = None
		self.difficulty = None
		self.gamemode = None
		self.level_type = None

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x33
		if self.context.protocol_version == 47:
			return 0x07
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")
