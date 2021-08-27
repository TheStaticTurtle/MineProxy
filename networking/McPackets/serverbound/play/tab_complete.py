import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class TabComplete(SimplePacket.Packet):
	TYPE = McPacketType.ServerBound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'text': common.types.common.String,
		'looked_at_block': common.types.complex.OptionalPosition,
	}

	def __init__(self, context):
		super().__init__(context)
		self.text = None
		self.looked_at_block = None

	@property
	def ID(self):
		return 0x14
