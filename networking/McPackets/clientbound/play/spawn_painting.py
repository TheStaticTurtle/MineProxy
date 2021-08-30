import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from networking.McPackets.Buffer import Buffer
from networking.McPackets.SimplePacket import Packet


class SpawnPainting(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		if self.context.protocol_version >= 107:
			return {
				'entity_id': common.types.common.VarInt,
				'entity_uuid': common.types.common.UUID,
				'title': common.types.common.String,
				'location': common.types.complex.Position,
				'direction': common.types.common.UnsignedByte,
			}
		if self.context.protocol_version == 47:
			return {
				'entity_id': common.types.common.VarInt,
				'title': common.types.common.String,
				'location': common.types.complex.Position,
				'direction': common.types.common.UnsignedByte,
			}

	def __init__(self, context):
		super().__init__(context)
		self.entity_id = None
		if self.context.protocol_version >= 107:
			self.entity_uuid = None
		self.title = None
		self.location = None
		self.direction = None

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x04
		if self.context.protocol_version == 47:
			return 0x10
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")