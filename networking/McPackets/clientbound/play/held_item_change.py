import common.types.common
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class HeldItemChanged(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'slot': common.types.common.Byte,
	}

	def __init__(self, context):
		super().__init__(context)
		self.slot = None

	@property
	def ID(self):
		return 0x09
