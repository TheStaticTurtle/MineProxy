import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class CreativeInventorAction(SimplePacket.Packet):
	TYPE = McPacketType.ServerBound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'slot': common.types.common.Short,
		'clicked_item': common.types.complex.Slot,
	}

	def __init__(self, context):
		super().__init__(context)
		self.slot = None
		self.clicked_item = None

	@property
	def ID(self):
		return 0x10
