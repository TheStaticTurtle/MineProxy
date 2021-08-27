import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket

class BlockAction(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'location': common.types.complex.Position,
		'byte_1': common.types.common.UnsignedByte,
		'byte_2': common.types.common.UnsignedByte,
		'block_type': common.types.common.VarInt,
	}

	def __init__(self, context):
		super().__init__(context)
		self.location = None
		self.byte_1 = None
		self.byte_2 = None
		self.block_type = None

	@property
	def ID(self):
		return 0x24
