import common.types.common
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class HeldItemChanged(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		return {
			'slot': common.types.common.Byte,
		}

	def __init__(self, context):
		super().__init__(context)
		self.slot = None

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x37
		if self.context.protocol_version == 47:
			return 0x09
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")
