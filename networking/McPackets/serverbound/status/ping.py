from common.types import McPacketType, McState
from networking.McPackets import SimplePacket
from common import types

class Ping(SimplePacket.Packet):
	ID = 0x01
	TYPE = McPacketType.ServerBound
	SUBTYPE = McState.Status
	STRUCTURE = {
		'payload': types.Long,
	}

	def __init__(self, context):
		super().__init__(context)
		self.payload = None