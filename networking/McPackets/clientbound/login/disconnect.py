from common.types import McPacketType, McState
from networking.McPackets import SimplePacket
from common import types

class Disconnect(SimplePacket.Packet):
	ID = 0x00
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Login
	STRUCTURE = {
		'reason': types.JSONString,
	}

	def __init__(self):
		super().__init__()
		self.reason = None