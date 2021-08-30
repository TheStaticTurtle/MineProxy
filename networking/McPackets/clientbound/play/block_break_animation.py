import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket

class BlockBreakAnimation(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play

	@property
	def STRUCTURE(self):
		return {
			'entity_id': common.types.common.VarInt,
			'location': common.types.complex.Position,
			'destroy_stage': common.types.common.Byte,
		}

	def __init__(self, context):
		super().__init__(context)
		self.entity_id = None
		self.location = None
		self.destroy_stage = None

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x08
		if self.context.protocol_version == 47:
			return 0x25
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")
