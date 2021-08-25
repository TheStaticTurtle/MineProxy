from common.types import McPacketType, McState
from networking.McPackets import SimplePacket
from common import types

class Respawn(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'dimension': types.Integer,
		'difficulty': types.UnsignedByte,
		'gamemode': types.UnsignedByte,
		'level_type': types.String,
	}

	def __init__(self, context):
		super().__init__(context)
		self.dimension = None
		self.difficulty = None
		self.gamemode = None
		self.level_type = None

	@property
	def ID(self):
		return 0x07
