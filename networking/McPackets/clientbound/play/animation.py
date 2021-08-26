import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket

class Animation(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'entity_id': common.types.common.VarInt,
		'_animation': common.types.common.UnsignedByte,
	}

	def __init__(self, context):
		super().__init__(context)
		self.entity_id = None
		self._animation = None

	@property
	def ID(self):
		return 0x0B

	@property
	def animation(self):
		return McState(int(self._animation))

	@animation.setter
	def animation(self, value: common.types.enums.Animation):
		self._animation = value.value
