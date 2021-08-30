import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class UpdateSign(SimplePacket.Packet):
	TYPE = McPacketType.ServerBound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		if self.context.protocol_version >= 107:
			return {
				'location': common.types.complex.Position,
				'line1': common.types.complex.String,
				'line2': common.types.complex.String,
				'line3': common.types.complex.String,
				'line4': common.types.complex.String,
			}
		if self.context.protocol_version == 47:
			return {
				'location': common.types.complex.Position,
				'line1': common.types.complex.JSONString,
				'line2': common.types.complex.JSONString,
				'line3': common.types.complex.JSONString,
				'line4': common.types.complex.JSONString,
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
			return 0x19
		if self.context.protocol_version == 47:
			return 0x12
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")
