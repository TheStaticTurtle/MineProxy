from common.types import McPacketType, McState
from networking.McPackets import SimplePacket
from common import types

class PluginMessage(SimplePacket.Packet):
	ID = 0x3F
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'channel': types.String,
		'data': types.ByteArray
	}

	def __init__(self):
		super().__init__()
		self.channel = None
		self.data = None
