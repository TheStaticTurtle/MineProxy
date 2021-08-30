import common.types.common
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class ServerDifficulty(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		return {
			'difficulty': common.types.common.UnsignedByte,
		}

	def __init__(self, context):
		super().__init__(context)
		self.difficulty = None

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x0D
		if self.context.protocol_version == 47:
			return 0x41
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")

