import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket

class CollectItem(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'collected_entity_id': common.types.common.VarInt,
		'collector_location': common.types.common.VarInt,
	}

	def __init__(self, context):
		super().__init__(context)
		self.collected_entity_id = None
		self.collector_location = None

	@property
	def ID(self):
		return 0x0D
