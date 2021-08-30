import common.types.common
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class ChatMessage(SimplePacket.Packet):
	TYPE = McPacketType.ServerBound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		return {
			'message': common.types.common.String,
		}

	def __init__(self, context):
		super().__init__(context)
		self.message = None

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x02
		if self.context.protocol_version == 47:
			return 0x01
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")