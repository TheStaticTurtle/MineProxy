import common.types.common
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class PluginMessage(SimplePacket.Packet):
	TYPE = McPacketType.ServerBound
	SUBTYPE = McState.Login
	STRUCTURE = {
		'channel': common.types.common.String,
		'channel_data': common.types.common.ByteArray,
	}
	# STRUCTURE_REPR_HIDDEN_FIELDS = ["channel_data"]

	def __init__(self, context):
		super().__init__(context)
		self.channel = None
		self.channel_data = None

	@property
	def ID(self):
		return 0x17
