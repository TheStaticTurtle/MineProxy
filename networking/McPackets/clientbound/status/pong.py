import common.types.common
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class Pong(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Status
	STRUCTURE = {
		'payload': common.types.common.Long,
	}

	def __init__(self, context):
		super().__init__(context)
		self.payload = None

	@property
	def ID(self):
		return 0x01