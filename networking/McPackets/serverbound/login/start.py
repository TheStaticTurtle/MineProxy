from common.types import McPacketType, McState
from networking.McPackets import SimplePacket
from common import types

class Start(SimplePacket.Packet):
	ID = 0x00
	TYPE = McPacketType.ServerBound
	SUBTYPE = McState.Login
	STRUCTURE = {
		'name': types.String,
	}

	def __init__(self):
		super().__init__()
		self.name = None