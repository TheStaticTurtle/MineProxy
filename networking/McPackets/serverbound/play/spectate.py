import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class Spectate(SimplePacket.Packet):
	TYPE = McPacketType.ServerBound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		return {
			'target_player': common.types.complex.UUID
		}

	def __init__(self, context):
		super().__init__(context)
		self.target_player = None

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x1B
		if self.context.protocol_version == 47:
			return 0x18
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")