import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket

class UnloadChunk(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		return {
			'chunk_x': common.types.common.Integer,
			'chunk_z': common.types.common.Integer,
		}

	def __init__(self, context):
		super().__init__(context)
		self.chunk_x = None
		self.chunk_z = None

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x1D
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")
