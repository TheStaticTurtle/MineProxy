import common.types.common
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class PluginMessage(SimplePacket.Packet):
	TYPE = McPacketType.ServerBound
	SUBTYPE = McState.Play
	# STRUCTURE_REPR_HIDDEN_FIELDS = ["channel_data"]
	
	@property
	def STRUCTURE(self):
		return {
			'channel': common.types.common.String,
			'channel_data': common.types.common.ByteArray,
		}

	def __init__(self, context):
		super().__init__(context)
		self.channel = None
		self.channel_data = None

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x09
		if self.context.protocol_version == 47:
			return 0x17
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")
