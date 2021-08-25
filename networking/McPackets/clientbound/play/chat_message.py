from common.types import McPacketType, McState
from networking.McPackets import SimplePacket
from common import types

class ChatMessage(SimplePacket.Packet):
	ID = 0x02
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'data': types.JSONString,
		'position': types.Byte,
	}

	def __init__(self, context):
		super().__init__(context)
		self.data = None
		self.position = None
