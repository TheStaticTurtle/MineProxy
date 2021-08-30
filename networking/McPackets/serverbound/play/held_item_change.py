import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class HeldItemChange(SimplePacket.Packet):
	TYPE = McPacketType.ServerBound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		return {
			'slot': common.types.common.Short,
		}

	def __init__(self, context):
		super().__init__(context)
		self.slot = None

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x17
		if self.context.protocol_version == 47:
			return 0x09
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")
