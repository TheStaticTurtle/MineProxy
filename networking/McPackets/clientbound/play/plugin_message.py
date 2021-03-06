import common.types.common
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class PluginMessage(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play

	@property
	def STRUCTURE(self):
		return {
			'channel': common.types.common.String,
			'data': common.types.common.ByteArray
		}

	def __init__(self, context):
		super().__init__(context)
		self.channel = None
		self.data = None

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x18
		if self.context.protocol_version == 47:
			return 0x3F
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")
