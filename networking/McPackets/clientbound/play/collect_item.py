import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket

class CollectItem(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		return {
			'collected_entity_id': common.types.common.VarInt,
			'collector_location': common.types.common.VarInt,
		}

	def __init__(self, context):
		super().__init__(context)
		self.collected_entity_id = None
		self.collector_location = None

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x49
		if self.context.protocol_version == 47:
			return 0x0D
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")
