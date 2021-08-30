import common.types.common
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class UpdateHealth(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		return {
		'health': common.types.common.Float,
		'food': common.types.common.VarInt,
		'food_saturation': common.types.common.Float,
	}

	def __init__(self, context):
		super().__init__(context)
		self.health = None
		self.food = None
		self.food_saturation = None

	@property
	def ID(self):
		return 0x06
