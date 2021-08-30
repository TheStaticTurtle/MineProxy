import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class PlayerAbilities(SimplePacket.Packet):
	TYPE = McPacketType.ServerBound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		return {
			'flags': common.types.common.Byte,
			'flying_speed': common.types.common.Float,
			'walking_speed': common.types.common.Float,
		}

	def __init__(self, context):
		super().__init__(context)
		self.location = None
		self.flying_speed = None
		self.walking_speed = None

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x12
		if self.context.protocol_version == 47:
			return 0x13
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")
