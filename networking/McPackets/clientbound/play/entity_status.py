import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket

class EntityStatus(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'entity_id': common.types.common.Integer,
		'entity_status': common.types.common.Byte,
	}

	def __init__(self, context):
		super().__init__(context)
		self.entity_id = None
		self.entity_status = None

	@property
	def ID(self):
		return 0x1A
