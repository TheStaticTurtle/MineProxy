import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket

class BlockChange(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'location': common.types.complex.Position,
		'block_id': common.types.common.VarInt,
	}

	def __init__(self, context):
		super().__init__(context)
		self.location = None
		self.block_id = None

	@property
	def ID(self):
		return 0x23
