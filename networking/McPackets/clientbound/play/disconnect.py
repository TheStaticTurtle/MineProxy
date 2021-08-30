import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket

class Disconnect(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		return {
			'reason': common.types.complex.JSONString if self.context.protocol_version >= 107 else common.types.complex.String,
		}

	def __init__(self, context):
		super().__init__(context)
		self.reason = None

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x1A
		if self.context.protocol_version == 47:
			return 0x40
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")
