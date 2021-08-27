import common.types.common
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class Player(SimplePacket.Packet):
	TYPE = McPacketType.ServerBound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'on_ground': common.types.common.Boolean,
	}

	def __init__(self, context):
		super().__init__(context)
		self.on_ground = None

	@property
	def ID(self):
		return 0x03
