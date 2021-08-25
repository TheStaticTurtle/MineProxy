import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class ChatMessage(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'data': common.types.complex.JSONString,
		'position': common.types.common.Byte,
	}

	def __init__(self, context):
		super().__init__(context)
		self.data = None
		self.position = None

	@property
	def ID(self):
		return 0x02
