import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket

class EntityStatus(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		return {
			'entity_id': common.types.common.Integer,
			'entity_status': common.types.common.Byte,
		}

	def __init__(self, context):
		super().__init__(context)
		self.entity_id = None
		self.entity_status = None

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x1B
		if self.context.protocol_version == 47:
			return 0x1A
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")
