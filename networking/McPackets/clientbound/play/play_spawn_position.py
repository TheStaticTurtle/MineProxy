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

	def __init__(self, context):
		super().__init__(context)
		self.location = None
