import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket

class UseBed(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		return {
			'entity_id': common.types.common.VarInt,
			'location': common.types.complex.Position,
		}

	def __init__(self, context):
		super().__init__(context)
		self.entity_id = None
		self.location = None

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x2F
		if self.context.protocol_version == 47:
			return 0x0A
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")
