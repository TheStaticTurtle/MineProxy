import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket

class SetExperience(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		return {
			'experience_bar': common.types.common.Float,
			'level': common.types.common.VarInt,
			'total_experience': common.types.common.VarInt,
		}

	def __init__(self, context):
		super().__init__(context)
		self.experience_bar = None
		self.level = None
		self.total_experience = None

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x3D
		if self.context.protocol_version == 47:
			return 0x1F
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")
