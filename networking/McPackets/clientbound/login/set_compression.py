from common.types import McPacketType, McState
from networking.McPackets import SimplePacket
from common import types

class SetCompression(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Login
	STRUCTURE = {
		'threshold': types.VarInt,
	}

	def __init__(self, context):
		super().__init__(context)
		self.threshold = -1

	@property
	def ID(self):
		return 0x03
