import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket

class BlockAction(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		return {
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
		if self.context.protocol_version >= 107:
			return 0x0B
		if self.context.protocol_version == 47:
			return 0x24
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")
