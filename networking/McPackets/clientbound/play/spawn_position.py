from common.types import McPacketType, McState
from networking.McPackets import SimplePacket
from common import types

class SpawnPosition(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'location': types.Position,
	}

	def __init__(self, context):
		super().__init__(context)
		self.location = None

	@property
	def ID(self):
		return 0x05
