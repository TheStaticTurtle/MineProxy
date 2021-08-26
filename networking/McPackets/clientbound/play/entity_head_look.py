import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket

class EntityHeadLook(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'entity_id': common.types.common.VarInt,
		'head_yaw': common.types.complex.Angle,
	}

	def __init__(self, context):
		super().__init__(context)
		self.entity_id = None
		self.head_yaw = None

	@property
	def ID(self):
		return 0x19
