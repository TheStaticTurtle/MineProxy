import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket

class SetCooldown(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		return {
			'item_id': common.types.common.VarInt,
			'cooldown_ticks': common.types.common.VarInt,
		}

	def __init__(self, context):
		super().__init__(context)
		self.item_id = None
		self.cooldown_ticks = None

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x17
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")
