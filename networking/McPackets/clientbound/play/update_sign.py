import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from networking.McPackets.Buffer import Buffer


class UpdateSign(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		return {
			'location': common.types.complex.Position,
			'line1': common.types.complex.JSONString if self.context.protocol_version >= 107 else common.types.common.String,
			'line2': common.types.complex.JSONString if self.context.protocol_version >= 107 else common.types.common.String,
			'line3': common.types.complex.JSONString if self.context.protocol_version >= 107 else common.types.common.String,
			'line4': common.types.complex.JSONString if self.context.protocol_version >= 107 else common.types.common.String,
		}

	def __init__(self, context):
		super().__init__(context)
		self.location = None
		self.line1 = None
		self.line2 = None
		self.line3 = None
		self.line4 = None

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x46
		if self.context.protocol_version == 47:
			return 0x33
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")