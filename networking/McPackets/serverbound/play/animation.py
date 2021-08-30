import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class Animation(SimplePacket.Packet):
	TYPE = McPacketType.ServerBound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		out = {
		}
		if self.context.protocol_version >= 107:
			out["hand"] = common.types.complex.UseEntityHandEnum
		return out

	def __init__(self, context):
		super().__init__(context)
		self.hand = None

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x1A
		if self.context.protocol_version == 47:
			return 0x0A
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")
