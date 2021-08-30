import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class ChatMessage(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		return {
			'data': common.types.complex.JSONString,
			'position': common.types.common.Byte,
		}

	def __init__(self, context):
		super().__init__(context)
		self.data = None
		self.position = None

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x0F
		if self.context.protocol_version == 47:
			return 0x02
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")
