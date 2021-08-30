import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from networking.McPackets.Buffer import Buffer


class PlayerAbilitites(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		return {
			'flags': common.types.common.Byte,
			'flying_speed': common.types.common.Float,
			'fov_modifier': common.types.common.Float,
		}

	def __init__(self, context):
		super().__init__(context)
		self.flags = None
		self.flying_speed = None
		self.fov_modifier = None

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x2B
		if self.context.protocol_version == 47:
			return 0x39
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")