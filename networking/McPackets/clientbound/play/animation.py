import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket

class Animation(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'entity_id': common.types.common.VarInt,
		'animation': common.types.complex.AnimationAnimationEnum,
	}

	def __init__(self, context):
		super().__init__(context)
		self.entity_id = None
		self.animation = None

	@property
	def ID(self):
		return 0x0B