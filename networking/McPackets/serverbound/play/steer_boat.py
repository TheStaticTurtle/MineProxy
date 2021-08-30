import common.types.common
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class SteerBoat(SimplePacket.Packet):
	TYPE = McPacketType.ServerBound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		return {
			'a': common.types.common.Boolean,
			'b': common.types.common.Boolean,
		}

	def __init__(self, context):
		super().__init__(context)
		self.a = None
		self.b = None

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x11
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")
