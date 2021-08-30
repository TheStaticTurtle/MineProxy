import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class ResourcePackStatus(SimplePacket.Packet):
	TYPE = McPacketType.ServerBound
	SUBTYPE = McState.Play

	@property
	def STRUCTURE(self):
		return {
			'hash': common.types.common.String,
			'result': common.types.complex.ResourcePackStatusResultEnum
		}

	def __init__(self, context):
		super().__init__(context)
		self.hash = None
		self.result = None

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x16
		if self.context.protocol_version == 47:
			return 0x17
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")