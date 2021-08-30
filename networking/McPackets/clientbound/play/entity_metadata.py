import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket

class EntityMetadata(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		return {
			'entity_id': common.types.common.VarInt,
			'metadata': common.types.complex.EntityMetadata,
		}

	def __init__(self, context):
		super().__init__(context)
		self.entity_id = None
		self.metadata = None

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x39
		if self.context.protocol_version == 47:
			return 0x1C
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")
