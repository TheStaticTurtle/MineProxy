import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket

class AttachEntity(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		if self.context.protocol_version >= 107:
			return {
				'entity_id': common.types.common.Integer,
				'holding_entity_id': common.types.common.Integer,
			}
		if self.context.protocol_version == 47:
			return {
				'entity_id': common.types.common.Integer,
				'vehicle_id': common.types.common.Integer,
				'leash': common.types.common.Boolean,
			}


	def __init__(self, context):
		super().__init__(context)
		if self.context.protocol_version >= 107:
			self.entity_id = None
			self.holding_entity_id = None
		if self.context.protocol_version == 47:
			self.entity_id = None
			self.vehicle_id = None
			self.leash = None

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x3A
		if self.context.protocol_version == 47:
			return 0x1B
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")
