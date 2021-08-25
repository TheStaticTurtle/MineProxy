from common.types import McPacketType, McState
from networking.McPackets import SimplePacket
from common import types

class PluginMessage(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'channel': types.String,
		'data': types.ByteArray
	}

	def __init__(self, context):
		super().__init__(context)
		self.channel = None
		self.data = None

	@property
	def ID(self):
		return 0x3F
