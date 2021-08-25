from common.types import McPacketType, McState
from networking.McPackets import SimplePacket
from common import types

class Pong(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Status
	STRUCTURE = {
		'payload': types.Long,
	}

	def __init__(self, context):
		super().__init__(context)
		self.payload = None

	@property
	def ID(self):
		return 0x01