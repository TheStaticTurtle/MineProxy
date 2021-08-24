from common.types import McPacketType, McState
from networking.McPackets import SimplePacket
from common import types

class ServerDifficulty(SimplePacket.Packet):
	ID = 0x41
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'difficulty': types.UnsignedByte,
	}

	def __init__(self, context):
		super().__init__(context)
		self.difficulty = None
