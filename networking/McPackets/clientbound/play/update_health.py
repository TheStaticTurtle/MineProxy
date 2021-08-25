from common.types import McPacketType, McState
from networking.McPackets import SimplePacket
from common import types

class UpdateHealth(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'health': types.Float,
		'food': types.VarInt,
		'food_saturation': types.Float,
	}

	def __init__(self, context):
		super().__init__(context)
		self.health = None
		self.food = None
		self.food_saturation = None

	@property
	def ID(self):
		return 0x06
