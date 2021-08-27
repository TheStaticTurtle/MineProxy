import common.types.common
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class ChatMessage(SimplePacket.Packet):
	TYPE = McPacketType.ServerBound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'message': common.types.common.String,
	}

	def __init__(self, context):
		super().__init__(context)
		self.message = None

	@property
	def ID(self):
		return 0x01