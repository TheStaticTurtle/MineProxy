import common.types.common
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class SetCompression(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Login
	STRUCTURE = {
		'threshold': common.types.common.VarInt,
	}

	def __init__(self, context):
		super().__init__(context)
		self.threshold = -1

	@property
	def ID(self):
		return 0x03
