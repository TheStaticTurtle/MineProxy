import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket

class ChunkData(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'chunk_x': common.types.common.Integer,
		'chunk_z': common.types.common.Integer,
		'ground_up_continuous': common.types.common.Boolean,
		'primary_bit_mask': common.types.common.UnsignedShort,
		'data': common.types.common.VarIntPrefixedByteArray,
	}
	STRUCTURE_REPR_HIDDEN_FIELDS = ["data"]

	def __init__(self, context):
		super().__init__(context)
		self.chunk_x = None
		self.chunk_z = None
		self.ground_up_continuous = None
		self.primary_bit_mask = None
		self.data = None

	@property
	def ID(self):
		return 0x21
