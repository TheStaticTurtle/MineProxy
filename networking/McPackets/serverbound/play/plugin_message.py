from common.types import McPacketType, McState
from networking.McPackets import SimplePacket
from common import types

class PluginMessage(SimplePacket.Packet):
	ID = 0x17
	TYPE = McPacketType.ServerBound
	SUBTYPE = McState.Login
	STRUCTURE = {
		'channel': types.String,
		'channel_data': types.ByteArray,
	}
	# STRUCTURE_REPR_HIDDEN_FIELDS = ["channel_data"]

	def __init__(self):
		super().__init__()
		self.channel = None
		self.channel_data = None
