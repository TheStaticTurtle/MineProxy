from common.types import McPacketType, McState
from networking.McPackets import SimplePacket
from common import types

class Pong(SimplePacket.Packet):
	ID = 0x01
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Status
	STRUCTURE = {
		'payload': types.Long,
	}

	def __init__(self):
		super().__init__()
		self.payload = None