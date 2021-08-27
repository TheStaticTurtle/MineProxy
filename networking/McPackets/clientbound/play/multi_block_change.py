import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket

class MultiBlockChange(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'chunk_x': common.types.common.Integer,
		'chunk_z': common.types.common.Integer,
		'records': common.types.complex.ChunkRecordArray,
	}

	def __init__(self, context):
		super().__init__(context)
		self.chunk_x = None
		self.chunk_z = None
		self.records = None

	@property
	def ID(self):
		return 0x22
