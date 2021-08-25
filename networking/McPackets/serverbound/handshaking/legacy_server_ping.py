from common.types import McPacketType, McState
from networking.McPackets import SimplePacket
from common import types

class LegacySeverPing(SimplePacket.Packet):
	TYPE = McPacketType.ServerBound
	SUBTYPE = McState.Handshaking
	STRUCTURE = {
		'payload': types.Long,
	}

	def __init__(self, context):
		super().__init__(context)
		self.payload = None

	@property
	def ID(self):
		return 0xFE