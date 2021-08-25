from common.types import McPacketType, McState
from networking.McPackets import SimplePacket
from common import types

class Disconnect(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'reason': types.String,
	}

	def __init__(self, context):
		super().__init__(context)
		self.reason = None

	@property
	def ID(self):
		return 0x40
