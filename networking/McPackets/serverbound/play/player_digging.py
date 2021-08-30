import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class PlayerDigging(SimplePacket.Packet):
	TYPE = McPacketType.ServerBound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		return {
			'status': common.types.complex.PlayerDiggingStatusEnum,
			'location': common.types.complex.Position,
			'face': common.types.common.Byte,
		}

	def __init__(self, context):
		super().__init__(context)
		self.status = None
		self.location = None
		self.face = None

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x13
		if self.context.protocol_version == 47:
			return 0x07
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")
