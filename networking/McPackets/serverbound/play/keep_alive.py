import common.types.common
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class KeepAlive(SimplePacket.Packet):
	TYPE = McPacketType.ServerBound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		return {
			'keep_alive_id': common.types.common.VarInt,
		}

	def __init__(self, context):
		super().__init__(context)
		self.keep_alive_id = None

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x0B
		if self.context.protocol_version == 47:
			return 0x00
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")
