from common.types import McPacketType, McState
from networking.McPackets import SimplePacket
from common import types

class SetCompression(SimplePacket.Packet):
	ID = 0x03
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Login
	STRUCTURE = {
		'threshold': types.VarInt,
	}

	def __init__(self, context):
		super().__init__(context)
		self.threshold = -1
