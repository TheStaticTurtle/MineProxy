from common.types import McPacketType, McState
from networking.McPackets import SimplePacket
from common import types

class SpawnPosition(SimplePacket.Packet):
	ID = 0x05
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'location': types.Position,
	}

	def __init__(self):
		super().__init__()
		self.location = None
