import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket

class BlockBreakAnimation(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	STRUCTURE = {
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
		return 0x25
