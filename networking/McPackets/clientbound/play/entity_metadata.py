import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket

class EntityMetadata(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'entity_id': common.types.common.VarInt,
		'metadata': common.types.complex.EntityMetadata,
	}

	def __init__(self, context):
		super().__init__(context)
		self.entity_id = None
		self.metadata = None

	@property
	def ID(self):
		return 0x1C
