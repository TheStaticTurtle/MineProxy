import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class EnchantItem(SimplePacket.Packet):
	TYPE = McPacketType.ServerBound
	SUBTYPE = McState.Play

	@property
	def STRUCTURE(self):
		return {
			'window_id': common.types.common.Byte,
			'enchantment': common.types.common.Byte,
		}

	def __init__(self, context):
		super().__init__(context)
		self.window_id = None
		self.enchantment = None

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x06
		if self.context.protocol_version == 47:
			return 0x11
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")
