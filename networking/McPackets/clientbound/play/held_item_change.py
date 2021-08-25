from common.types import McPacketType, McState
from networking.McPackets import SimplePacket
from common import types

class HeldItemChanged(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'slot': types.Byte,
	}

	def __init__(self, context):
		super().__init__(context)
		self.slot = None

	@property
	def ID(self):
		return 0x09
